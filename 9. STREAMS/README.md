# Redis Streams: Guía Completa y Detallada

Redis Streams es una estructura de datos poderosa introducida en Redis 5.0. Es ideal para modelar sistemas de mensajería y procesamiento de datos en tiempo real, proporcionando capacidades similares a sistemas como Kafka o RabbitMQ, pero con la simplicidad de Redis.

## Conceptos Fundamentales

Redis Streams es una lista de mensajes ordenados cronológicamente. Cada mensaje tiene un ID único y contiene uno o más pares clave-valor. Está diseñado para aplicaciones que necesitan:

- Procesamiento de datos en tiempo real.
- Cola de mensajes.
- Almacenamiento temporal de datos para sistemas distribuidos.

Un Stream en Redis se identifica por una clave (por ejemplo, `mystream`) y almacena mensajes asociados con esa clave.

---

## Operaciones Comunes en Redis Streams

### 1. Creación y Adición de Mensajes a un Stream
La operación `XADD` se utiliza para agregar mensajes a un Stream.

#### Ejemplo en Python
Usando la biblioteca `redis-py`:

```python
import redis

# Conectar a Redis
client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Agregar un mensaje al Stream
message_id = client.xadd('mystream', {'sensor': 'temp', 'value': '22.5'})
print(f"Mensaje agregado con ID: {message_id}")
```

#### Ejemplo en Go
Usando la biblioteca `go-redis`:

```go
package main

import (
	"context"
	"fmt"
	"github.com/redis/go-redis/v9"
)

func main() {
	ctx := context.Background()
	client := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
	})

	// Agregar un mensaje al Stream
	msgID, err := client.XAdd(ctx, &redis.XAddArgs{
		Stream: "mystream",
		Values: map[string]interface{}{
			"sensor": "temp",
			"value": "22.5",
		},
	}).Result()

	if err != nil {
		fmt.Println("Error al agregar mensaje:", err)
		return
	}

	fmt.Println("Mensaje agregado con ID:", msgID)
}
```

---

### 2. Lectura de Mensajes
La operación `XRANGE` permite leer mensajes dentro de un rango de IDs.

#### Ejemplo en Python
```python
# Leer mensajes del Stream
messages = client.xrange('mystream', '-', '+')
for message in messages:
    print(f"ID: {message[0]}, Datos: {message[1]}")
```

#### Ejemplo en Go
```go
// Leer mensajes del Stream
msgs, err := client.XRange(ctx, "mystream", "-", "+").Result()
if err != nil {
	fmt.Println("Error al leer mensajes:", err)
	return
}

for _, msg := range msgs {
	fmt.Printf("ID: %s, Datos: %v\n", msg.ID, msg.Values)
}
```

---

### 3. Lectura en Tiempo Real
Usa `XREAD` para leer mensajes nuevos a medida que llegan.

#### Ejemplo en Python
```python
# Leer mensajes nuevos en tiempo real
messages = client.xread({"mystream": "$"}, block=0)
for stream, msgs in messages:
    for msg in msgs:
        print(f"ID: {msg[0]}, Datos: {msg[1]}")
```

#### Ejemplo en Go
```go
msgs, err := client.XRead(ctx, &redis.XReadArgs{
	Streams: []string{"mystream", "$"},
	Count:   0,
	Block:   0,
}).Result()
if err != nil {
	fmt.Println("Error al leer mensajes:", err)
	return
}

for _, stream := range msgs {
	for _, msg := range stream.Messages {
		fmt.Printf("ID: %s, Datos: %v\n", msg.ID, msg.Values)
	}
}
```

---

### 4. Creación de Grupos de Consumidores
Los grupos de consumidores permiten distribuir la carga entre múltiples consumidores.

#### Python
```python
# Crear un grupo de consumidores
client.xgroup_create('mystream', 'mygroup', id='$', mkstream=True)
print("Grupo de consumidores creado")
```

#### Go
```go
// Crear un grupo de consumidores
err := client.XGroupCreateMkStream(ctx, "mystream", "mygroup", "$").Err()
if err != nil {
	fmt.Println("Error al crear grupo:", err)
	return
}

fmt.Println("Grupo de consumidores creado")
```

---

### 5. Procesamiento de Mensajes en un Grupo
Con `XREADGROUP`, los consumidores pueden procesar mensajes.

#### Python
```python
# Leer mensajes como parte de un grupo de consumidores
messages = client.xreadgroup('mygroup', 'consumer1', {'mystream': '>'}, block=0)
for stream, msgs in messages:
    for msg in msgs:
        print(f"ID: {msg[0]}, Datos: {msg[1]}")
```

#### Go
```go
msgs, err := client.XReadGroup(ctx, &redis.XReadGroupArgs{
	Group:   "mygroup",
	Consumer: "consumer1",
	Streams:  []string{"mystream", ">"},
	Count:    10,
	Block:    0,
}).Result()
if err != nil {
	fmt.Println("Error al leer como grupo:", err)
	return
}

for _, stream := range msgs {
	for _, msg := range stream.Messages {
		fmt.Printf("ID: %s, Datos: %v\n", msg.ID, msg.Values)
	}
}
```

---

## Casos de Uso

### Ejemplo 1: Sistema de Monitoreo de Sensores
Imagina un sistema que registra datos de sensores en tiempo real y los distribuye a diferentes consumidores.

- **Python:** Los sensores envían datos usando `XADD`, mientras que los consumidores los procesan con `XREADGROUP`.
- **Go:** Se utilizan consumidores distribuidos para procesar los datos simultáneamente.

### Ejemplo 2: Cola de Mensajes para Tareas
Redis Streams se puede usar como cola para distribuir tareas entre diferentes trabajadores.

---

Con esta guía, tienes una comprensión detallada de Redis Streams y cómo implementarlos con Python y Go.
