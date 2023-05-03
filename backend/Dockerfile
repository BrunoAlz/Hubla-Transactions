FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /api
COPY requirements.txt /api/requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000



# CMD python manage.py wait_for_db && python manage.py runserver 0.0.0.0:8000