build_test:
	export ACCESS_USR=accessuser \
	&& export ACCESS_PWD=accesspwd \
	&& export RABBITMQ_HOST=localhost \
	&& export RABBITMQ_PORT=5672 \
	&& export RABBITMQ_VHOST=first-vhost \
	&& export MONGO_HOST=localhost \
	&& export MONGO_PORT=27017 \
	&& go build -ldflags "-s -w" -o bin/orchestrator && ./bin/orchestrator "worker"

run_test:
	export ACCESS_USR=accessuser \
	&& export ACCESS_PWD=accesspwd \
	&& export RABBITMQ_HOST=localhost \
	&& export RABBITMQ_PORT=5672 \
	&& export RABBITMQ_VHOST=first-vhost \
	&& export MONGO_HOST=localhost \
	&& export MONGO_PORT=27017 \
	&& ./bin/orchestrator "server"
	
build_1:
	go build -o bin/orchestrator

build:
	go build -ldflags "-s -w" -o bin/orchestrator

test_1: build run_test