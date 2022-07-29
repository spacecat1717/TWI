FROM python:3.9
WORKDIR /twi
COPY ./ /twi
RUN apk update && pip install -r /twi/requirements.txt --no-cache-dir
EXPOSE 8000
CWD ["python", "manage.py", "runserver", "0.0.0.0:8000"]