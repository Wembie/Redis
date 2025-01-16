# XREAD Command

## Descripción
El comando `XREAD` en Redis permite leer entradas de uno o más streams, comenzando desde una posición específica y avanzando en el tiempo. Este comando es ideal para consumir datos secuenciales, como eventos o logs, que han sido previamente almacenados en streams.

## Sintaxis
```plaintext
XREAD [COUNT <numero>] STREAMS <nombre_stream> <id>
```
- **COUNT**: (Opcional) Especifica el número máximo de entradas que se desean leer.
- **STREAMS**: Indica los nombres de los streams y los IDs desde donde comenzar a leer.
- **nombre_stream**: Nombre del stream del cual se leerán las entradas.
- **id**: ID de inicio. Usar `0-0` para leer desde el principio o `$` para esperar nuevas entradas.

## Ejemplo en Python
Usando la biblioteca `redis-py`:

```python
import redis

# Conexión al servidor Redis
client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Leer entradas desde el stream "eventos"
entries = client.xread({"eventos": "0-0"}, count=5)

# Mostrar las entradas leídas
for stream, messages in entries:
    print(f"Stream: {stream}")
    for message_id, fields in messages:
        print(f"ID: {message_id}, Datos: {fields}")

# Leer nuevas entradas desde el stream
entries_new = client.xread({"eventos": "$"})
print(entries_new)
```

## Ejemplo en Go
Usando la biblioteca `github.com/go-redis/redis/v8`:

```go
package main

import (
	"context"
	"fmt"

	"github.com/go-redis/redis/v8"
)

func main() {
	ctx := context.Background()
	client := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
	})

	// Leer entradas desde el stream "eventos"
	streams, err := client.XRead(ctx, &redis.XReadArgs{
		Streams: []string{"eventos", "0-0"},
		Count:   5,
	}).Result()

	if err != nil {
		panic(err)
	}

	// Mostrar las entradas leídas
	for _, stream := range streams {
		fmt.Printf("Stream: %s\n", stream.Stream)
		for _, message := range stream.Messages {
			fmt.Printf("ID: %s, Datos: %v\n", message.ID, message.Values)
		}
	}

	// Leer nuevas entradas desde el stream
	newStreams, err := client.XRead(ctx, &redis.XReadArgs{
		Streams: []string{"eventos", "$"},
	}).Result()

	if err != nil {
		panic(err)
	}

	fmt.Printf("Nuevas entradas: %v\n", newStreams)
}
```

## Casos de Uso
1. **Procesamiento de datos en tiempo real**: Consumir logs o eventos generados por una aplicación.
2. **Colas de mensajes**: Implementar consumidores que procesen tareas secuenciales.
3. **Notificaciones en vivo**: Leer actualizaciones o eventos a medida que ocurren.

## Consideraciones
- `XREAD` puede usarse junto con `BLOCK` para esperar nuevas entradas en lugar de devolver inmediatamente.
- Si el stream especificado no existe, Redis devolverá una lista vacía.

## Ejemplo Avanzado
### Leer de múltiples streams
```python
# Leer entradas desde múltiples streams
entries = client.xread({"stream1": "0-0", "stream2": "0-0"}, count=10)

for stream, messages in entries:
    print(f"Stream: {stream}")
    for message_id, fields in messages:
        print(f"ID: {message_id}, Datos: {fields}")
```

### Uso de bloqueo en Go
```go
streams, err := client.XRead(ctx, &redis.XReadArgs{
	Streams: []string{"eventos", "$"},
	Block:   0,
}).Result()

if err != nil {
	panic(err)
}

for _, stream := range streams {
	fmt.Printf("Stream: %s\n", stream.Stream)
	for _, message := range stream.Messages {
		fmt.Printf("ID: %s, Datos: %v\n", message.ID, message.Values)
	}
}
