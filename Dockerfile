FROM python:3.12

WORKDIR /app

COPY . /app

EXPOSE 3000

CMD ["python", "main.py"]
