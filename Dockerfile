# Our Node base image
FROM python:3.9-alpine3.16

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 80

COPY assets_manager .
COPY start.sh .

CMD ["bash", "start.sh"]
