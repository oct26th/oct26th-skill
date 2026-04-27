FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV ENTRY=telegram_bot.py
CMD ["sh", "-c", "python3 ${ENTRY}"]
