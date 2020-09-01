FROM python:3.8
ENV APP_ENV_CONFIG configuration.DevelopmentConfig

RUN apt-get -y update && \
    apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -y build-essential

RUN pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ADD ./api /var/www/api

WORKDIR /var/www/api/
EXPOSE 5000

CMD [ "uwsgi", "--http-socket",  " :5000" , "--module", "app:app" ]
