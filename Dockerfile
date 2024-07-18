FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate

RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "chess_tournament.wsgi:application", "--bind", "0.0.0.0:8000"]