FROM python:3.12.2

WORKDIR /usr/src/app/taskmgmt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./req.txt /usr/src/app
RUN pip install --no-cache-dir -r /usr/src/app/req.txt

COPY . /usr/src/app/

RUN python manage.py collectstatic --noinput

RUN apt-get update && apt-get install -y nginx

COPY ./taskmgmt/nginx/nginx.conf /etc/nginx/nginx.conf

RUN python manage.py migrate

CMD service nginx start && gunicorn taskmgmt.wsgi:application --bind 0.0.0.0:8000 --workers 3