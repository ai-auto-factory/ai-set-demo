FROM python:3.8-buster

RUN apt-get update -y

RUN mkdir /app

COPY . /app/

RUN pip install --no-cache --upgrade pip
RUN pip install --timeout=120 -r /app/requirements.txt

WORKDIR /app

EXPOSE 8502


CMD ["python", "-m","streamlit","run","app.py"]