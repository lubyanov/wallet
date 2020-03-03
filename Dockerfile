FROM python:3.7.2-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install pipenv holdup && pipenv install --system --deploy

CMD holdup tcp://$POSTGRES_HOST:$POSTGRES_PORT -- python manage.py migrate \
    && gunicorn -b 0.0.0.0:8080 app.wsgi:application --access-logfile '-' --log-level $GUNICORN_DEBUG_LEVEL