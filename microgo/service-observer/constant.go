package main

import (
	"fmt"
	"os"
)

const (
	ChannelReceiverRoute = "celery_receiver_queue"
	ChannelSenderRoute = "celery_sender_queue"
)

var accessUser = os.Getenv("ACCESS_USR")
var accessPwd = os.Getenv("ACCESS_PWD")

var rb_host = os.Getenv("RABBITMQ_HOST")
var rb_port = os.Getenv("RABBITMQ_PORT")
var vhost = os.Getenv("RABBITMQ_VHOST")

var mongo_host = os.Getenv("MONGO_HOST")
var mongo_port = os.Getenv("MONGO_PORT")

var rabbitMQURL = fmt.Sprintf("amqp://%s:%s@%s:%v/%s", accessUser, accessPwd, rb_host, rb_port, vhost)

var mongoDBURI = fmt.Sprintf("mongodb://%s:%s@%s:%v/celery?authSource=admin", accessUser, accessPwd, mongo_host, mongo_port)