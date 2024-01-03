---
sidebar_position: 3
sidebar_label: "2. WSGI server"
---

The repository for this section is located at branch **[2.2_three_way_merge](https://github.com/highlander-spirou/microgo/tree/1_Monolith_architecture)**

This section aim to scale the web using traditional `nginx` and `wsgi` that create multiple web workers (flask instance) rather than just one flask. For detail explaination about `nginx` & `gunicorn wsgi` visit: **[WSGI & Nginx explain](/docs/tutorial-basics/wsgi-and-nginx)**.

## Bridge network

Greatest changes come from the networking setup. In the previous setup, we exposes all of our app to `host` network. But in this section, we will construct an internal bridge network (See **[Docker networking](/docs/tutorial-basics/docker-network)** for more info 👀)

The bridge network helps:
- Bridge network maps the container's IP to a route table. This helps multiple containers to open to the same port
- Keep track of scaled services since Docker will assign the services to a range of IPs 

### Change the host name
The first change need to be done when migrating from host network to bridge network is the change from `localhost` -> `<service name>` 

```md title="monolith/.env"
...

MARIADB_HOST="mariadb"
MONGO_HOST= "mongodb"

...
```
### `wait-for-it` service

Since our composes use database as a service, we have to wait for the TCP port open on both MariaDB and MongoDB, we will use the `wait-for-it` container. See **[Dependent services](/docs/tutorial-basics/dependent-service)** for more information.

## Gunicorn WSGI interface:

### Create gunicorn_config.py

The core application does not change (since we want an incremental upgrade to the application, not to introduce breaking changes).

We renamed the `index.py` to `server.py`, and create `gunicorn_config.py` to run `gunicorn` interface.

```mdx title="Monolith"
│   # Seperate the controller when the logic gets complicates (and reduce the import of `index.py`)
├── controllers
│   └── ...
├── middleware
│   └── ...
├── modules
│   └── ...
├── logs
│
├── .env
├── pyproject.toml
├── instantiation.py
├── server.py
└── gunicorn_config.py
```

### Update the `ENTRYPOINT`

We also update the `ENTRYPOINT` of the image to call the gunicorn service

```Dockerfile title="Dockerfile"
FROM python:3.10.12-slim
RUN pip install poetry==1.7.1

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
COPY monolith ./monolith

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

WORKDIR /app/monolith

// highlight-start
ENTRYPOINT ["poetry", "run", "gunicorn", "-c", "gunicorn_config.py", "server:app"]
// highlight-end
```

### Mount the `logs` folder

We want to be able to investigate the log, so we mount the `logs` folder into the docker volume. Since the `logging` module default mode is append mode, new log from all the containers will be written into a single `app_logs.log` file, create a central debug point for our distributed service

```yml title="docker-compose.yml"
services:
  flask:
    volumes:
      - ./monolith/logs:/app/monolith/logs
```

## Nginx

Nginx will expose the port 80. But in this example, we have setup Postman to test on port 5000. So we will map the nginx container port 80 to the host port 5000.

We also need to make sure that the Nginx depends on `Flask` service, since we need the gunicorn open the corresponding port -> register to route table -> proxy_pass by `nginx`

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

```yml title="docker-compose.yml"
nginx:
image: nginx:latest
depends_on:
    - flask
networks:
    - microgo
ports:
    - "5000:80"
```

