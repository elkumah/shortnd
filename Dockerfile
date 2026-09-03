FROM python:3.14-slim
WORKDIR /app
COPY api/requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip "setuptools>=78.1.1" && \
    python -m pip install --no-cache-dir -r requirements.txt
COPY api/app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]