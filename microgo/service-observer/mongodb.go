package main

import (
	"context"
	"fmt"
	"time"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func getMongoDBConnection(chann chan <- *mongo.Client) {

	connectMongoDB := func() (*mongo.Client, error){
		// conn, err := amqp.Dial(rabbitMQURL)
		client, err := mongo.Connect(context.Background(), options.Client().ApplyURI(mongoDBURI))
		return client, err
	}

	for attempt := 1; attempt <= 10; attempt++ {
		fmt.Println("Attemp to connect to MongoDB ...")
		client, err := connectMongoDB()
		defer client.Disconnect(context.Background())
		if err == nil {
			chann <- client
			break
		} else {
			time.Sleep(2 * time.Second)
		}
	}
	

	close(chann)

	// fmt.Println("Attemp to connect to MongoDB")
	// client, err := mongo.Connect(context.Background(), options.Client().ApplyURI(mongoDBURI))
	// if err != nil {
	// 	fmt.Println(err)
	// 	close(chann)
	// }
	// chann <- client
	// close(chann)

	// err = client.Ping(context.Background(), nil)
	// if err != nil {
	// 	return err
	// }
}

