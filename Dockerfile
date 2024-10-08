FROM python:3.11.4-slim-buster

ENV PYTHONUNBUFFERED 1


WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY .. .

RUN mkdir -p /vol/web/media

RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

RUN chown -R django-user:django-user /vol/
RUN chmod -R 755 /vol/web/


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
