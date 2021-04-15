FROM python:3-slim
WORKDIR /usr/src/app/
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN export FLASK_APP=model
COPY user.py db.py amqp_setup.py schema.sql model.py sqlite_db data.sqlite ./
CMD [ "python", "model.py"]