FROM python:3.12

ENV APP_HOME=/app

WORKDIR $APP_HOME

COPY contacts_project/ $APP_HOME

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]