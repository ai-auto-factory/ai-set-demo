FROM python:3.9-buster

RUN apt-get update -y

RUN mkdir /app

COPY . /app/

RUN pip install --no-cache --upgrade pip
RUN pip install --timeout=120 -r /app/requirements.txt

WORKDIR /app
RUN chmod 777 /app/_secret_auth_.json

EXPOSE 7860


CMD ["python", "-m","streamlit","run","app.py","--server.port","7860","--server.address","0.0.0.0"]