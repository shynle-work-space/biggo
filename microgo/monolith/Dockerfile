# Stage 1: Build Golang application

FROM golang:1.21.5-alpine3.19 AS build
WORKDIR /app
COPY service-observer /app
# Build the Golang application
# RUN go build -o /app/bin/golang_app
RUN go build -ldflags "-s -w" -o /app/bin/orchestrator

FROM python:3.10.12-slim
RUN pip install poetry==1.7.1

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
COPY ./monolith ./monolith
COPY ./microgo ./microgo

# Copy the binary from the first stage into the second stage
COPY --from=build /app/bin/orchestrator ./monolith/orchestrator

RUN poetry config virtualenvs.create false
RUN poetry install 

WORKDIR /app/monolith
RUN chmod +x ./run_server.sh
ENTRYPOINT ["sh", "./run_server.sh"]