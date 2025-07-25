#!/usr/bin/env python3
"""
TokIntel v2 - Synthesis Agent
Generates summaries from transcript and OCR text using LLM
"""

from typing import Dict, List, Any, Optional
import requests
import time
import json
from core.logger import LoggerMixin
from core.exceptions import LLMError
from llm.prompts import PromptManager

class SynthesisAgent(LoggerMixin):
    """Agent responsible for generating summaries using LLM"""
    
    def __init__(self, model: str = "gpt-4", endpoint: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize synthesis agent"""
        super().__init__()
        self.model = model
        self.endpoint = endpoint
        self.api_key = api_key
        self.prompt_manager = PromptManager()
        self.log_info("SynthesisAgent initialized with prompt manager")
    
    def summarize(self, transcript: str, ocr_text: str, config: Dict[str, Any]) -> str:
        """Generate summary from transcript and OCR text"""
        try:
            self.log_info("Generating summary from transcript and OCR text")
            start_time = time.time()
            
            # Build prompt using prompt manager
            prompt = self.prompt_manager.get_prompt("summary", transcript=transcript, ocr_text=ocr_text)
            
            # Get model configuration
            model_config = config.get("llm_config", {})
            model = model_config.get("model", self.model)
            endpoint = model_config.get("endpoint", self.endpoint)
            api_key = model_config.get("api_key", self.api_key)
            
            # Generate summary
            if endpoint and "localhost" in endpoint:
                summary = self._call_local_llm(prompt, endpoint, model)
            else:
                summary = self._call_openai_llm(prompt, model, api_key)
            
            if not summary:
                self.log_warning("Empty summary generated")
                return "Nessuna sintesi generata"
            
            processing_time = time.time() - start_time
            self.log_info(f"Summary generated: {len(summary)} characters in {processing_time:.2f}s")
            return summary
            
        except Exception as e:
            self.log_error(f"Summary generation failed: {e}")
            raise LLMError(f"Summary generation failed: {e}")
    
    def _build_summary_prompt(self, transcript: str, ocr_text: str) -> str:
        """Build the summary prompt (deprecated - use prompt manager)"""
        return self.prompt_manager.get_prompt("summary", transcript=transcript, ocr_text=ocr_text)
    
    def _call_openai_llm(self, prompt: str, model: str, api_key: Optional[str] = None) -> str:
        """Call OpenAI API"""
        try:
            from openai import OpenAI
            
            self.log_debug(f"Calling OpenAI API with model: {model}")
            start_time = time.time()
            
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            summary = response.choices[0].message.content.strip()
            api_time = time.time() - start_time
            self.log_debug(f"OpenAI API call successful in {api_time:.2f}s")
            return summary
            
        except ImportError:
            self.log_error("OpenAI library not installed. Install with: pip install openai")
            raise LLMError("OpenAI library not available")
        except Exception as e:
            self.log_error(f"OpenAI API call failed: {e}")
            raise LLMError(f"OpenAI API call failed: {e}")
    
    def _call_local_llm(self, prompt: str, endpoint: str, model: str) -> str:
        """Call local LLM (e.g., LM Studio)"""
        try:
            self.log_debug(f"Calling local LLM at: {endpoint}")
            start_time = time.time()
            
            response = requests.post(
                endpoint,
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 500
                },
                timeout=30
            )
            
            if response.status_code != 200:
                raise LLMError(f"Local LLM API error: {response.status_code} - {response.text}")
            
            data = response.json()
            summary = data["choices"][0]["message"]["content"].strip()
            
            api_time = time.time() - start_time
            self.log_debug(f"Local LLM call successful in {api_time:.2f}s")
            return summary
            
        except requests.exceptions.RequestException as e:
            self.log_error(f"Local LLM request failed: {e}")
            raise LLMError(f"Local LLM request failed: {e}")
        except Exception as e:
            self.log_error(f"Local LLM call failed: {e}")
            raise LLMError(f"Local LLM call failed: {e}")
    
    def analyze_engagement_factors(self, transcript: str, ocr_text: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze engagement factors in the content"""
        try:
            self.log_info("Analyzing engagement factors")
            start_time = time.time()
            
            prompt = self.prompt_manager.get_prompt("engagement", transcript=transcript, ocr_text=ocr_text)
            
            # Get model configuration
            model_config = config.get("llm_config", {})
            model = model_config.get("model", self.model)
            endpoint = model_config.get("endpoint", self.endpoint)
            
            # Generate analysis
            if endpoint and "localhost" in endpoint:
                analysis = self._call_local_llm(prompt, endpoint, model)
            else:
                analysis = self._call_openai_llm(prompt, model)
            
            processing_time = time.time() - start_time
            self.log_info(f"Engagement analysis completed in {processing_time:.2f}s")
            
            # Parse JSON response (basic parsing)
            try:
                # Extract JSON from response if needed
                if "{" in analysis and "}" in analysis:
                    start = analysis.find("{")
                    end = analysis.rfind("}") + 1
                    json_str = analysis[start:end]
                    return json.loads(json_str)
                else:
                    return {"analysis": analysis}
            except (json.JSONDecodeError, ValueError):
                return {"analysis": analysis}
            
        except Exception as e:
            self.log_error(f"Engagement analysis failed: {e}")
            raise LLMError(f"Engagement analysis failed: {e}")
    
    def set_model(self, model: str):
        """Set LLM model"""
        self.model = model
        self.log_info(f"LLM model set to: {model}")
    
    def set_endpoint(self, endpoint: str):
        """Set LLM endpoint"""
        self.endpoint = endpoint
        self.log_info(f"LLM endpoint set to: {endpoint}")
    
    def set_api_key(self, api_key: str):
        """Set API key"""
        self.api_key = api_key
        self.log_info("API key set")
