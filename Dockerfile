FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["fastapi", "run", "api_main.py", "--port", "8000"]