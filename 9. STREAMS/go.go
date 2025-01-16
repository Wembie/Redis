package main

import (
	"context"
	"fmt"

	"github.com/go-redis/redis/v8"
)

var ctx = context.Background()

func main() {
	client := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
	})

	streamName := "user_activity"

	// Añadir eventos al stream
	addEvents(client, streamName)

	// Leer eventos desde el stream
	readEvents(client, streamName)

	// Recuperar un rango de eventos
	rangeEvents(client, streamName)

	// Obtener la longitud del stream
	getStreamLength(client, streamName)
}

// Función para añadir eventos al stream
func addEvents(client *redis.Client, streamName string) {
	events := []map[string]interface{}{
		{"user": "juan", "event": "login"},
		{"user": "maria", "event": "compra", "item": "laptop"},
		{"user": "carlos", "event": "logout"},
	}

	for _, event := range events {
		_, err := client.XAdd(ctx, &redis.XAddArgs{
			Stream: streamName,
			Values: event,
		}).Result()

		if err != nil {
			panic(err)
		}
	}
	fmt.Printf("%d eventos añadidos al stream '%s'.\n", len(events), streamName)
}

// Función para leer eventos desde el stream
func readEvents(client *redis.Client, streamName string) {
	entries, err := client.XRead(ctx, &redis.XReadArgs{
		Streams: []string{streamName, "0-0"},
		Count:   10,
	}).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println("\nEventos leídos:")
	for _, stream := range entries {
		for _, message := range stream.Messages {
			fmt.Printf("ID: %s, Datos: %v\n", message.ID, message.Values)
		}
	}
}

// Función para recuperar un rango de eventos
func rangeEvents(client *redis.Client, streamName string) {
	entries, err := client.XRange(ctx, streamName, "0-0", "+").Result()
	if err != nil {
		panic(err)
	}

	fmt.Println("\nEventos en rango:")
	for _, entry := range entries {
		fmt.Printf("ID: %s, Datos: %v\n", entry.ID, entry.Values)
	}
}

// Función para obtener la longitud del stream
func getStreamLength(client *redis.Client, streamName string) {
	length, err := client.XLen(ctx, streamName).Result()
	if err != nil {
		panic(err)
	}
	fmt.Printf("\nLongitud del stream '%s': %d\n", streamName, length)
}