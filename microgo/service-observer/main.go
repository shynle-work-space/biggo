package main

import (
	"fmt"
	"os"
	"log"
	"slices"
	"sync"
	// "time"
	amqp "github.com/rabbitmq/amqp091-go"
	"go.mongodb.org/mongo-driver/mongo"
)

func pingRabbitMQ(wg *sync.WaitGroup) {

	connChan := make(chan *amqp.Connection)	

	go testAMQPConnection(connChan)

	_, exit_status := <- connChan
	if !exit_status{
		log.Fatal("Cannot connect to RabbitMQ!")
	}
	fmt.Println("Successfully connect to RabbitMQ!")
	wg.Done()
}

func pingWorker(wg *sync.WaitGroup) {
	
	fmt.Println("Start to pingWorker")
	connChan := make(chan *amqp.Connection)	
	sendMsgChan := make(chan bool)
	receiveMsgChan := make(chan bool)
	
	fmt.Println("Run function `testAMQPConnection`")
	go testAMQPConnection(connChan)

	conn, exit_status := <- connChan
	if !exit_status{
		log.Fatal("Cannot connect to RabbitMQ!")
	}
	fmt.Println("Successfully connect to RabbitMQ!")

	go testSendMessage(sendMsgChan, conn)
	_, send_exit_status := <- sendMsgChan
	if !send_exit_status{
		log.Fatal("Cannot send message to RabbitMQ!")
	}
	fmt.Println("Successfully send message to RabbitMQ!")

	go waitForMessage(conn, receiveMsgChan)
	_, receive_exit_status := <- receiveMsgChan
	if !receive_exit_status {
		log.Fatal("Connection to Celery worker fails. Cannot receive loop back message!")
	}

	fmt.Println("Successfully send and receive message from Celery worker")

	wg.Done()
}

func pingMongoDB(wg *sync.WaitGroup) {
	
	connChan := make(chan *mongo.Client)	

	go getMongoDBConnection(connChan)

	_, exit_status := <- connChan
	if !exit_status{
		log.Fatal("Cannot connect to MongoDB!")
	}
	fmt.Println("Successfully connect to MongoDB")
	wg.Done()
}

func main() {
	fmt.Println("Orchestrator version v0.0.2a\n")
	args := os.Args
	validArguments := []string{"worker", "server", "abc"}

	if len(args) < 2 {
		log.Fatal("Argument required!")
	}
	firstArg := args[1]
	if slices.Contains(validArguments, firstArg) {
		wg := &sync.WaitGroup{}

		if firstArg == "worker" {
			wg.Add(2)
			go pingRabbitMQ(wg)
			go pingMongoDB(wg)
			wg.Wait()
		} else if firstArg == "server" {
			wg.Add(1)
			go pingWorker(wg)
			wg.Wait()
		}
	} else {
		log.Fatal("Invalid argument!")
	}
}


