FROM python:3.12
WORKDIR /app

RUN pip install --no-cache-dir telebot aiohttp psutil

COPY src /app
ENTRYPOINT ["python", "/app/main.py"]