FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt

COPY . /app /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]