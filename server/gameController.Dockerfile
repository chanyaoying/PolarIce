FROM python:3-slim
WORKDIR /usr/src/app/
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN export FLASK_APP=gameController
COPY ./gameController.py ./
CMD [ "python", "gameController.py"]