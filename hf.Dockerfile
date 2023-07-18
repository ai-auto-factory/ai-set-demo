FROM python:3.9-buster

RUN #apt-get update -y

RUN apt-get install -y git


RUN mkdir /app
RUN git clone https://github.com/ai-auto-factory/ai-set-demo.git && mv ai-set-demo/* /app/

RUN pip install --no-cache --upgrade pip
RUN pip install --timeout=120 -r /app/requirements.txt

WORKDIR /app
EXPOSE 7860


CMD ["python", "-m","streamlit","run","app.py","--server.port","7860"]