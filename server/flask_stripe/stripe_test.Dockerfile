FROM python:3-slim
WORKDIR /usr/src/app/
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN export FLASK_APP=stripe_test
# COPY static ./static
# COPY templates ./templates
# COPY stripe_test.py ./
COPY . .
CMD [ "python", "stripe_test.py"]