FROM python:3-slim
WORKDIR /usr/src/app/
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# RUN export FLASK_APP=roomController
COPY ./roomController.py ./user.py ./db.py ./amqp_setup.py ./activity_log.py ./twitter.py ./
CMD [ "python", "./roomController.py"]

