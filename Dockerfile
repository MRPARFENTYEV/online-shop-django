
FROM python:3.12
RUN mkdir /code
WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt
RUN python manage.py migrate
EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


