FROM python:3.10.11

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8081

CMD ["python", "main.py"]