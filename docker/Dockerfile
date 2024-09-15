FROM python:3.11

RUN apt-get update -y
RUN apt-get upgrade -y

RUN mkdir -p /app

COPY src/ /app/
WORKDIR /app
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

#Set timezone
ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


CMD [ "python", "/app/main.py" ]
