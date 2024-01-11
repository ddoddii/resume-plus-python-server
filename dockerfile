FROM python:3.10

WORKDIR /app/

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

VOLUME /app/resume-db

COPY . /app/

CMD uvicorn --host=0.0.0.0 --port 8000 main:app
