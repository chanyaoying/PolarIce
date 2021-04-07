FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./activity_log.py ./amqp_setup.py ./tele_log.py ./
CMD [ "python", "./activity_log.py" ]