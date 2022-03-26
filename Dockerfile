FROM python:3.8.3



ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get install netcat -y
RUN apt-get upgrade --fix-missing -y && apt-get install postgresql gcc python3-dev musl-dev nano -y


COPY . /usr/src/app
RUN mkdir /env
RUN chmod -R 777 /env
RUN python -m venv /env
RUN /env/bin/pip install --upgrade pip

RUN /env/bin/pip install --no-cache-dir -r /usr/src/app/requirements.txt


WORKDIR /usr/src/app/gradko


ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
CMD exec python /usr/src/app/gradko/manage.py migrate


EXPOSE 8888

CMD exec gunicorn --bind :8888 --workers 3 testDjango.wsgi
#CMD exec python /usr/src/app/gradko/manage.py runserver 0.0.0.0:8001
