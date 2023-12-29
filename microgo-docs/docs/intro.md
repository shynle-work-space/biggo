---
sidebar_position: 1
---

# Microservices Project

This project is a complete microservices project that takes an image compress service and scale it to enterprise level that resilient and able to serve millions of request per day.

## What's different about this project

**This project is not a mindless youtube code along**. This project start from a humble Flask development server 
(kinda like the one from blog and youtube tutorials), and incrementally adapt its capacity to scale into a microservices. Every step and consideration was documented as a knowledge base and for future guidance 

## Project workflow

![Flowchart Image](/img/flowchart.jpg)

The user data is stored in MariaDB, and images are stored in MongoDB by GridFS. The service mimick high load access by throttle the image process service (sleep between 5-30s)

## Technical implementations

- User authentication by JWT
- Message queue for optimistic feedback


## Project Overview

Our program will have four routes:
- `login`: Login user and create JWT token
- `upload`: Upload the image for image compression
- `download`: Provide the ID for download the image
- `img_collection`: Check the available images of a user

We will test the route using **Postman** and python's `httpx` for concurrent requests.