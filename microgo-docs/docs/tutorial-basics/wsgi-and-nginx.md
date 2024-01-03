---
sidebar_label: "WSGI & Nginx"
---

# Definition

![Flask warning](/img/flask-warning.png)

Let's find out what this message means!

## WSGI and web workers

*Web Server Gateway Interface (WSGI)* is a standardize way for python frameworks to receive and send response back to client

![WSGI diagram](/img/wsgi.png)

A Flask server is called a `web worker`. The Flask worker process the user requests in a synchronous fashion: After it receives one request, the gate is blocked until the Flask worker done (either a success or a failure). Imagine you have a crazily heavy task runs at the backend (our application throttle upto 5s per task), it will takes more than 8 mins just to process 100 requests !!!

In development, we only spawn one web worker to process user requests, that open a localhost:5000 port. If we want a another server to offload our initial server, we need to have another port open. `WSGI` interface born to solve that problem. A WSGI application does the following things:

- Create web worker accordingly to the config
- Bind all the web workers to a single port
- Load balance the user request to the worker

## Nginx

In the previous diagram, we see that user request are sent to a `web server` before hitting the WSGI layer. This is the Nginx layer. Nginx is used to load balance the user request, set timeout and smart HTTP error if the user request is out of scope.

## The wsgi implementation for python web framework

![wsgi nginx](/img/wsgi_nginx.png)

To be able to bind to all the `Gunicorn` wsgi interface, we need to map the `Nginx` to the corresponding port that the `Gunicorn` is open. When deploying to `docker-compose.yml`, luckily, all services IPs are mapped to a route table, and Nginx can refer to them as service name.

In brief: 
1. Create `gunicorn_config.py`, that opens a port
2. Create an image that run the gunicorn 
3. In `docker-compose.yml`, create a service from the image, only specify the container port (let docker decide the host port automatically)
4. Create an `nginx.conf` that map to gunicorn service: `proxy_pass http://<service_name>:<service_port>`
5. Create a `nginx` service in `docker-compose.yml` and mount the `nginx.conf`


See the full implementation below 👇

1. Create a `gunicorn_config.py` that spawn web workers at port 5000 (the example will create 5 flask app)

```py title="app/gunicorn_config.py"
bind = '0.0.0.0:5000'
workers = 5
worker_connections = 1000
loglevel = 'info'
```

2. Create docker image of the flask application

```Dockerfile
FROM python:3.10.12-slim
RUN pip install poetry==1.7.1


COPY pyproject.toml poetry.lock README.md ./
COPY app ./app

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

WORKDIR /app
ENTRYPOINT ["poetry", "run", "gunicorn", "-c", "gunicorn_config.py", "server:app"]
```

3. Create a `nginx.conf`

```conf title="nginx.conf"
events {
    worker_connections 1000;
}

http {
    server {
        listen 80;

        location / {
            proxy_pass http://flask:5000;
        }
    }
}
```
4. Bundle all to docker-compose.yml

```yml title="docker-compose.yml"
version: '3.9'

services:
  flask:
    build: 
      context: ./
      dockerfile: Dockerfile
    ports: 
      - "5000"
    networks:
      - microgo

  nginx:
    image: nginx:latest
    depends_on:
      - flask
    networks:
      - microgo
    ports:
      - "5000:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro

networks:
  microgo:
```

