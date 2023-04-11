FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/app

COPY . /usr/app

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["gunicorn", "core.wsgi", "0:80"]