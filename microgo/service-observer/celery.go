package main

import (
	"encoding/json"
	"fmt"
	"log"
	"time"
	"errors"

	"github.com/google/uuid"
	amqp "github.com/rabbitmq/amqp091-go"
)

func generateUUID() string {
	return uuid.New().String()
}

func testAMQPConnection(connChan chan *amqp.Connection) {

	fmt.Println("Inside function `testAMQPConnection`")

	connectRabbitMQ := func() (*amqp.Connection, error){
		conn, err := amqp.Dial(rabbitMQURL)
		fmt.Println(err)
		return conn, err
	}
	
	for attempt := 1; attempt <= 10; attempt++ {
		fmt.Println("Attemp to connect to RabbitMQ ...")
		conn, err := connectRabbitMQ()
		if err == nil {
			connChan <- conn
			break
		} else {
			time.Sleep(2 * time.Second)
		}
	}

	close(connChan)
}

func createMesage(msg map[string]string) []byte {
	payload := map[string]interface{}{
		"args":  []interface{}{},
		"kwargs": msg,
		"embed":  map[string]interface{}{},
	}
	// Convert the message to JSON
	messageBody, err := json.Marshal(payload)
	if err != nil {
		log.Fatal("Cannot serialize message to JSON")
	}
	return messageBody
}

func ensureExchange(ch *amqp.Channel) {
	// Declare the exchange
	err := ch.ExchangeDeclare(
		ChannelReceiverRoute, // name
		"direct",       // type
		true,         // durable
		false,        // auto-delete
		false,        // internal
		false,        // no-wait
		nil,          // arguments
	)
	if err != nil {
		log.Fatal("Failed to declare the queue:", err)
	}

	_, err = ch.QueueDeclare(
		ChannelReceiverRoute, // name
		true,      // durable
		false,     // delete when unused
		false,     // exclusive
		false,     // no-wait
		nil,       // arguments
	)
	if err != nil {
		log.Fatal("Failed to declare the queue:", err)
	}

	// Bind the queue to the exchange
	err = ch.QueueBind(
		ChannelReceiverRoute,    // name
		ChannelReceiverRoute,   // routing key
		ChannelReceiverRoute, // exchange
		false,        // no-wait
		nil,          // arguments
	)
	if err != nil {
		log.Fatal("Failed to bind the queue to the exchange:", err)
	}

}

func publishMessage(conn *amqp.Connection, messageBody []byte) error {
	correlationID := generateUUID()
	// Create a channel
	ch, err := conn.Channel()
	if err != nil {
		return err
	}
	defer ch.Close()

	headers := amqp.Table{
		"task": "ping",
		"id": correlationID,
	}

	ensureExchange(ch)
	// Publish the message to the exchange
	err = ch.Publish(
		ChannelReceiverRoute, // exchange
		ChannelReceiverRoute,   // routing key
		false,        // mandatory
		false,        // immediate
		amqp.Publishing {
			Headers: headers,
			Body:      messageBody,
			Timestamp: time.Now(),
			CorrelationId: correlationID,
			ContentType: "application/json",
			ContentEncoding: "utf-8",
		},
	)
	if err != nil {
		return err
	}

	return nil

}

func testSendMessage(chann chan bool, conn *amqp.Connection) {
	
	// Create a message
	msgBody := map[string]string{}
	msgBody["message"] = "hello from golang"
	msg := createMesage(msgBody)


	// Create an inner function to retry
	sendMessage := func(conn *amqp.Connection, messageBody []byte) (bool, error){
		error := publishMessage(conn, msg)
		if error != nil {
			return false, error
		}
		return true, nil
	}

	
	// Retry the function for 10 times, 2 second break => max 20s
	fmt.Println("Attemp to send message to RabbitMQ ...")
	for attempt := 1; attempt <= 10; attempt++ {
		status, err := sendMessage(conn, msg)
		if err == nil {
			chann <- status
			break
		} else {
			fmt.Println("Cannot send message to RabbitMQ, retrying ...")
			time.Sleep(2 * time.Second)
		}
	}

	close(chann)
	
}

func msgConsumer(conn *amqp.Connection, maxWaitTime time.Duration) error {
	ch, err := conn.Channel()
	if err != nil {
		return err
	}
	defer ch.Close()

	// Set up a channel to receive messages
	msgs, err := ch.Consume(
		ChannelSenderRoute, // queue
		"",        // consumer
		true,      // auto-ack
		false,     // exclusive
		false,     // no-local
		false,     // no-wait
		nil,       // args
	)
	if err != nil {
		fmt.Println("Queue not found!")
		return err
	}

	// Wait for a message with a timeout
	select {
	case msg := <-msgs:
		fmt.Printf("Received message: %s\n", string(msg.Body))
		return nil
	case <-time.After(maxWaitTime):
		return errors.New("Timeout waiting for message")
	}
}

func waitForMessage(conn *amqp.Connection, chann chan bool) {
	fmt.Println("Attemp to wait for worker message ...")
	for attempt := 1; attempt <= 10; attempt++ {
		err := msgConsumer(conn, 30)
		if err != nil {
			time.Sleep(6 * time.Second)
		} else {
			chann <- true
			break
		}
	}
	close(chann)
}