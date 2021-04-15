FROM python:3-slim
WORKDIR /usr/src/app/
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN export FLASK_APP=tele_log
COPY ./tele_log.py ./
CMD [ "python", "tele_log.py"]