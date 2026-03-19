FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_RETRIES=10

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir \
    --index-url https://pypi.org/simple \
    --timeout 100 \
    --retries 10 \
    --upgrade pip \
 && python -m pip install --no-cache-dir \
    --index-url https://pypi.org/simple \
    --timeout 100 \
    --retries 10 \
    -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]