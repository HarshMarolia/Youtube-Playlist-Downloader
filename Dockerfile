FROM python:3.8-slim

WORKDIR /app

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . .

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]