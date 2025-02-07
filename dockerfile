FROM python:3.9

WORKDIR /app

COPY api_gateway/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY api_gateway/ .

EXPOSE 5000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
