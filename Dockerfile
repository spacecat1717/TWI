FROM python:3.9
WORKDIR /twi
COPY ./ /twi
RUN apk update && pip install -r /twi/requirements.txt --no-cache-dir
EXPOSE 8000
