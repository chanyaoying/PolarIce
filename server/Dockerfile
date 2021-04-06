FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./invokes.py ./roomController.py ./
CMD [ "python", "./roomController.py" ]

# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# EXPOSE 5000
# COPY . .
# CMD ["flask", "run"]

# FROM python:3-slim
# WORKDIR /usr/src/app
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt
# COPY ./invokes.py ./test_invoke_http.py ./
# CMD [ "python", "./test_invoke_http.py" ]
