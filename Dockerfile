# Dockerfile per TokIntel API
FROM python:3.11-slim

WORKDIR /app

COPY TokIntel_v2_workspace/ ./

RUN pip install --upgrade pip \
    && pip install fastapi uvicorn[standard] pydantic requests openpyxl reportlab pytest pytest-cov

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 