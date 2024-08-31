FROM python:3.9

RUN apt-get update -y
RUN apt-get upgrade -y

RUN mkdir -p /app/

COPY . /app/my_wellness_connector
WORKDIR /app
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

CMD [ "python", "/app/main.py" ]