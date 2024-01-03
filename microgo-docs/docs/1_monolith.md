---
sidebar_position: 3
sidebar_label: "1. Monolith server"
---

The repository for this section is located at branch **[1_Monolith_architecture](https://github.com/highlander-spirou/microgo/tree/1_Monolith_architecture)**

# The starting point

We will start with a very simple Flask application, that we normally see in most Youtube tutorials. 

The Flask app contains 4 routes that is registered at `index.py`. Simple & straightfoward route logic are baked into the `index.py` while the complicated ones are separated into `controllers`. Reusable codes are placed at `modules` (or `libs`, `utils`, ..., whatever you please) and `middlewares` (reusable code applied directly to the `request` object)

## Directory tree:


```mdx title="Monolith"
│   # Seperate the controller when the logic gets complicates (and reduce the import of `index.py`)
├── controllers
│   ├── download_ctrl.py
│   └── upload_ctrl.py
│
│   # Reusable logic (`user_authentication`) 
├── middleware
│   └── authenticate_route.py
│
│   # Small pieces of code with specific functionality
├── modules
│   ├── auth
│   ├── config
│   ├── file_access
│   ├── img_process
│   ├── log
│   └── errors
│   
│   # To store application logs
├── logs
│ 
│   # This is server's .env (contains database host, ports and access identifier)  
├── .env
├── pyproject.toml
├── instantiation.py
├── index.py
└── wsgi.py
```

```mdx title="Top level file"
│   # Files for containerization  
├── pyproject.toml
├── poetry.lock
│   # Cluster .env file (for secrets like root user)  
├── .env
│
│   # This folder responsible for initialize the creation of desired state of the database. 
├── bootstrap
│   ├── auth
│   └── errors
│
├── Dockerfile
├── .dockerignore
└── docker-compose.yml
```

## Databases

The two databases will be declared in the `docker-compose.yml`. Here, we state that the two database will be registered to `host` network, so that the server could refer to their IP address as `localhost`.

We will utilize the `docker-entrypoint-initdb.d` to finalize the desired state the databases (including create access users, create tables, collections and seeded data). In production environment, this folder with be RIGHT BEFORE BUILD TIME since this contains confidential data.

:::tip

More about Docker networking see **[Docker networking tutorial](/docs/tutorial-basics/docker-network)**

:::


## The monolith server

To mimic a crowded website, the image process function will be throttled for 5s. Eventhough the entry file is called `wsgi.py`, we will run a bare Flask development server without any WSGI interface

Run this command 👇

```bash
docker compose up -d
cd monolith && python wsgi.py
```

*Test results*

![Postman test result for monolith server](/img/postman_test_monolith.png)


<!-- <p style="font-size: large; font-weight: 600;">Boom 💥 !!! Now you have a cool webserver up and running 😎</p> -->
<p style={{fontSize: "1.7em", fontWeight: 600}}>Now you have a web server up and running !!!</p>


