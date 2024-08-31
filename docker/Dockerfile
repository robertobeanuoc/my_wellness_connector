FROM python:3.9:latest 


RUN apt-get update -y
RUN apt-get upgrade -y

RUN mkdir -p /app/

COPY ./food_recognition_model/src /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

CMD [ "python", "/app/main.py" ]