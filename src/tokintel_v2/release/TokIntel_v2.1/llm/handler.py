"""
LLM Handler Module
Centralized LLM call management with retries, timeouts, and model switching
"""

from typing import Dict, List, Any, Optional
import logging
logger = logging.getLogger(__name__)
import asyncio
import time
import json
import requests
from core.logger import setup_logger
from core.exceptions import LLMError

# Try to import OpenAI for async support
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    AsyncOpenAI = None

logger = setup_logger(__name__)

def async_retry(max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
    """Decorator for async retry logic with exponential backoff"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            delay = base_delay
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(f"LLM call attempt {attempt + 1} failed: {e}. Retrying in {delay:.1f}s...")
                        await asyncio.sleep(delay)
                        delay = min(delay * 2, max_delay)
                    else:
                        logger.error(f"LLM call failed after {max_retries + 1} attempts: {e}")
                        raise last_exception
            return await func(*args, **kwargs)
        return wrapper
    return decorator

class LLMHandler:
    """Centralized LLM call handler with retry logic and timeout management"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize LLM handler with configuration"""
        self.config = config
        self.model = config.get("model", "gpt-4")
        self.endpoint = config.get("endpoint", None)
        self.api_key = config.get("api_key", None)
        self.timeout = config.get("timeout", 30)
        self.max_retries = config.get("max_retries", 3)
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 500)
        
        logger.info(f"LLM Handler initialized with model: {self.model}")
    
    @async_retry(max_retries=3)
    async def call_llm(self, prompt: str, model: Optional[str] = None, **kwargs) -> str:
        """Make LLM call with automatic model selection and retry logic"""
        start_time = time.time()
        
        # Use provided model or default
        target_model = model or self.model
        
        try:
            logger.debug(f"Making LLM call with model: {target_model}")
            
            # Determine if local or remote
            if self._is_local_model(target_model):
                result = await self._call_local_llm(prompt, target_model, **kwargs)
            else:
                result = await self._call_openai_llm(prompt, target_model, **kwargs)
            
            processing_time = time.time() - start_time
            logger.debug(f"LLM call completed in {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"LLM call failed after {processing_time:.2f}s: {e}")
            raise LLMError(f"LLM call failed: {e}")
    
    def _is_local_model(self, model: str) -> bool:
        """Check if model should be called locally"""
        local_indicators = ["localhost", "127.0.0.1", "local", "ollama", "lmstudio"]
        return any(indicator in model.lower() for indicator in local_indicators) or self.endpoint
    
    async def _call_openai_llm(self, prompt: str, model: str, **kwargs) -> str:
        """Call OpenAI API asynchronously"""
        try:
            if not OPENAI_AVAILABLE:
                raise LLMError("OpenAI library not installed. Install with: pip install openai")
            
            logger.debug(f"Calling OpenAI API with model: {model}")
            
            client = AsyncOpenAI(api_key=self.api_key)
            
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", self.temperature),
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                timeout=kwargs.get("timeout", self.timeout)
            )
            
            result = response.choices[0].message.content.strip()
            logger.debug("OpenAI API call successful")
            return result
            
        except ImportError:
            logger.error("OpenAI library not installed. Install with: pip install openai")
            raise LLMError("OpenAI library not available")
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise LLMError(f"OpenAI API call failed: {e}")
    
    async def _call_local_llm(self, prompt: str, model: str, **kwargs) -> str:
        """Call local LLM asynchronously"""
        try:
            endpoint = kwargs.get("endpoint", self.endpoint)
            if not endpoint:
                raise LLMError("No local endpoint configured")
            
            logger.debug(f"Calling local LLM at: {endpoint}")
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None,
                self._call_local_llm_sync,
                prompt,
                endpoint,
                model,
                kwargs
            )
            
            logger.debug("Local LLM call successful")
            return result
            
        except Exception as e:
            logger.error(f"Local LLM call failed: {e}")
            raise LLMError(f"Local LLM call failed: {e}")
    
    def _call_local_llm_sync(self, prompt: str, endpoint: str, model: str, kwargs: Dict[str, Any]) -> str:
        """Synchronous local LLM call (runs in thread pool)"""
        try:
            response = requests.post(
                endpoint,
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": kwargs.get("temperature", self.temperature),
                    "max_tokens": kwargs.get("max_tokens", self.max_tokens)
                },
                timeout=kwargs.get("timeout", self.timeout)
            )
            
            if response.status_code != 200:
                raise LLMError(f"Local LLM API error: {response.status_code} - {response.text}")
            
            data = response.json()
            result = data["choices"][0]["message"]["content"].strip()
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise LLMError(f"Local LLM request failed: {e}")
        except Exception as e:
            raise LLMError(f"Local LLM call failed: {e}")
    
    async def batch_call_llm(self, prompts: list, model: Optional[str] = None, **kwargs) -> list:
        """Make multiple LLM calls concurrently"""
        logger.info(f"Making batch LLM calls for {len(prompts)} prompts")
        start_time = time.time()
        
        try:
            # Create tasks for concurrent execution
            tasks = [
                self.call_llm(prompt, model, **kwargs) 
                for prompt in prompts
            ]
            
            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            successful_results = []
            failed_results = []
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    failed_results.append((i, str(result)))
                    logger.error(f"Prompt {i} failed: {result}")
                else:
                    successful_results.append(result)
            
            processing_time = time.time() - start_time
            logger.info(f"Batch LLM calls completed in {processing_time:.2f}s: {len(successful_results)} successful, {len(failed_results)} failed")
            
            return results
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Batch LLM calls failed after {processing_time:.2f}s: {e}")
            raise LLMError(f"Batch LLM calls failed: {e}")
    
    def update_config(self, updates: Dict[str, Any]):
        """Update handler configuration"""
        self.config.update(updates)
        
        # Update instance variables
        if "model" in updates:
            self.model = updates["model"]
        if "endpoint" in updates:
            self.endpoint = updates["endpoint"]
        if "api_key" in updates:
            self.api_key = updates["api_key"]
        if "timeout" in updates:
            self.timeout = updates["timeout"]
        if "max_retries" in updates:
            self.max_retries = updates["max_retries"]
        if "temperature" in updates:
            self.temperature = updates["temperature"]
        if "max_tokens" in updates:
            self.max_tokens = updates["max_tokens"]
        
        logger.info("LLM Handler configuration updated")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get handler statistics"""
        return {
            "model": self.model,
            "endpoint": self.endpoint,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

class LLMFactory:
    """Factory for creating LLM handlers with different configurations"""
    
    @staticmethod
    def create_handler(config: Dict[str, Any]) -> LLMHandler:
        """Create LLM handler with configuration"""
        return LLMHandler(config)
    
    @staticmethod
    def create_openai_handler(api_key: str, model: str = "gpt-4", **kwargs) -> LLMHandler:
        """Create OpenAI-specific handler"""
        config = {
            "model": model,
            "api_key": api_key,
            **kwargs
        }
        return LLMHandler(config)
    
    @staticmethod
    def create_local_handler(endpoint: str, model: str = "local", **kwargs) -> LLMHandler:
        """Create local LLM handler"""
        config = {
            "model": model,
            "endpoint": endpoint,
            **kwargs
        }
        return LLMHandler(config) 