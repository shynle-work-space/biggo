---
sidebar_label: "Dependent service in docker"
---

Imagine you want to create a service with a flask application and a MariaDB.
Your flask application make a TCP connection to the MariaDB service, and then it crash ... Cannot connect to the database !

This is exactly what it looks like: 

![Dependent service dies](/img/dependent_service_dies.png)

You be like: *Hmm 🤔, weird, I thought I include the `depends_on` option ???*

Every service in Docker has to undergoes a creation phase, where the docker download the image, provision the resouces, and run the image (any code preceeding the `ENTRYPOINT`)

However, each services has its own setup phase. That is the phase after running the `ENTRYPOINT` command. For `MariabDB`, that is where the database setup the databases, tables, create seeded user, setup TCP port, ...

`docker-composes` only cares about the creation phase. As we see in the diagram, the server immediately create after the creation phase of the database, and since the setup phase of the server much faster than the database, it makes a TCP request before the databases establish a TCP port -> leading to error.

To fix that problem, we implement a `wait-for-it` service.

A `wait-for-it` service is a service that after a db service start, it continously ping the db service to check for the status. Our server will set to depends on that service. If the db service is not ready, `wait-for-it` marks as stale, and wait till the next ping intervals. When the db service is ready, the service exit with code 0. Then, the server started to create. Since the creation of the server after the setup phase, it is guarentee the TCP connection is working properly.

![Dependent service works](/img/dependent_service_works.png)

```yml title="docker-compose.yml"
version: '3.9'

services:
  flask:
    build: 
      context: ./
      dockerfile: Dockerfile
    depends_on:
      wait-mariadb:
        condition: service_completed_successfully

  mariadb:
    image: mariadb:latest
    networks:
      - microgo

  wait-mariadb:
    image: atkrad/wait4x
    depends_on:
      - mariadb
    networks:
      - microgo
    # retry every 1s upto 20s
    command: tcp mariadb:3306 -t 20s -i 1000ms


networks:
  microgo:

```


:::warning

The `wait-for-it` requires the docker-compose version to be **3.9** or higher

:::