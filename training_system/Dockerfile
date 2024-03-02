FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN apt-get update && pip install --upgrade pip && pip install -r /app/requirements.txt --no-cache-dir

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
