FROM python:alpine3.19
ARG name
WORKDIR /usr/src/app

ARG LISTEN_PORT
ENV LISTEN_PORT=9100

EXPOSE ${LISTEN_PORT}

COPY requirements.txt device-driver.py ./

#UN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./device-driver.py" ]
