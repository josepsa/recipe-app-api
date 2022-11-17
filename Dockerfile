#The Dockerfile is used to build our image, which contains a mini Linux Operating System 
#with all the dependencies needed to run our project.

#'docker build .' command will use this file
#Base image which loads from docker hub
FROM python:3.9-alpine3.13

LABEL maintainer="Sajan"

#this will print python output to console
ENV PYTHONUNBUFFERED 1

#copy from localhost to dockerimage
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

#setting argument DEV as false as default, it is overridden in docker-compose,
#it will run as dev=true when you run docker-compose 
ARG DEV=false
# '&& \' for executing multiple commands using single run command. 
#if user is not created then it will run as root
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    #installing postgres-client dependecy inside alpine python alpine image inorder to install psycopg2
    #which connects to postgres db from python.without this pip will throw error.
    apk add --update --no-cache postgresql-client && \   
    #installing dependenices for psycoph2 and storing them in .tmp to remove later.
    #only postgres-client required for using psycopg2, so remaining dependenices are removing
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    #removing temporary dependencies used to install psycopg2
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

#setting enviornment path instead of using full path during command execution
ENV PATH="/py/bin:$PATH"

#switching user, till now it was running as root
USER django-user