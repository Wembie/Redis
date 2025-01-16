# XADD Command

## Descripción
El comando `XADD` en Redis se utiliza para agregar una nueva entrada a un stream. Es muy útil para registrar eventos en un flujo de datos, como logs, mensajes o cualquier información secuencial.

Cada entrada en un stream tiene una ID única y un conjunto de pares campo-valor asociados. Si no se especifica una ID al usar `XADD`, Redis genera una automáticamente basada en el tiempo actual.

## Sintaxis
```plaintext
XADD <nombre_stream> [MAXLEN ~ <longitud_maxima>] <id> <campo1> <valor1> [<campo2> <valor2> ...]
```
- **nombre_stream**: El nombre del stream.
- **MAXLEN ~**: (Opcional) Limita la cantidad máxima de entradas almacenadas en el stream.
- **id**: (Opcional) ID específica para la entrada. Si no se proporciona, Redis asigna una automáticamente.
- **campo-valor**: Pares de datos asociados a la entrada.

## Ejemplo en Python
Usando la biblioteca `redis-py`:

```python
import redis

# Conexión al servidor Redis
client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Agregar una entrada al stream "eventos"
stream_name = "eventos"
response = client.xadd(stream_name, {"usuario": "juan", "accion": "login", "tiempo": "2025-01-16T12:34:56"})
print(f"ID de la nueva entrada: {response}")

# Agregar con límite de longitud
response_limited = client.xadd(stream_name, {"usuario": "ana", "accion": "logout"}, maxlen=1000)
print(f"ID de la entrada con límite: {response_limited}")
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

	streamName := "eventos"

	// Agregar una entrada al stream "eventos"
	response, err := client.XAdd(ctx, &redis.XAddArgs{
		Stream: streamName,
		Values: map[string]interface{}{
			"usuario": "juan",
			"accion": "login",
			"tiempo": "2025-01-16T12:34:56",
		},
	}).Result()

	if err != nil {
		panic(err)
	}

	fmt.Printf("ID de la nueva entrada: %s\n", response)

	// Agregar con límite de longitud
	responseLimited, err := client.XAdd(ctx, &redis.XAddArgs{
		Stream: streamName,
		MaxLen: 1000,
		Values: map[string]interface{}{
			"usuario": "ana",
			"accion": "logout",
		},
	}).Result()

	if err != nil {
		panic(err)
	}

	fmt.Printf("ID de la entrada con límite: %s\n", responseLimited)
}
```

## Casos de Uso
1. **Registro de eventos**: Capturar logs de aplicaciones o eventos del sistema.
2. **Procesamiento de datos en tiempo real**: Almacenar eventos para ser consumidos por consumidores en tiempo real.
3. **Sistemas de colas**: Implementar un sistema de cola para distribuir tareas.
