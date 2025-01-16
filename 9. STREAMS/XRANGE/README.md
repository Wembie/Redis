# XRANGE Command

## Descripción
El comando `XRANGE` en Redis permite leer un rango específico de entradas de un stream, basándose en sus IDs. Es útil para consultar eventos pasados o realizar análisis sobre un subconjunto de datos en un stream.

## Sintaxis
```plaintext
XRANGE <nombre_stream> <id_inicio> <id_fin> [COUNT <numero>]
```
- **nombre_stream**: Nombre del stream a consultar.
- **id_inicio**: ID desde donde se comenzará la lectura. Usar `-` para el inicio del stream.
- **id_fin**: ID hasta donde se leerá. Usar `+` para el final del stream.
- **COUNT**: (Opcional) Número máximo de entradas a devolver.

## Ejemplo en Python
Usando la biblioteca `redis-py`:

```python
import redis

# Conexión al servidor Redis
client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Leer un rango de entradas del stream "eventos"
entries = client.xrange("eventos", min="0-0", max="+")

# Mostrar las entradas leídas
for message_id, fields in entries:
    print(f"ID: {message_id}, Datos: {fields}")

# Leer con límite de cantidad
limited_entries = client.xrange("eventos", min="0-0", max="+", count=5)
for message_id, fields in limited_entries:
    print(f"ID: {message_id}, Datos: {fields}")
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

	// Leer un rango de entradas del stream "eventos"
	entries, err := client.XRange(ctx, "eventos", "0-0", "+").Result()
	if err != nil {
		panic(err)
	}

	// Mostrar las entradas leídas
	for _, entry := range entries {
		fmt.Printf("ID: %s, Datos: %v\n", entry.ID, entry.Values)
	}

	// Leer con límite de cantidad
	limitedEntries, err := client.XRangeN(ctx, "eventos", "0-0", "+", 5).Result()
	if err != nil {
		panic(err)
	}

	for _, entry := range limitedEntries {
		fmt.Printf("ID: %s, Datos: %v\n", entry.ID, entry.Values)
	}
}
```

## Casos de Uso
1. **Análisis de datos históricos**: Obtener un subconjunto de datos almacenados en el stream para análisis o reportes.
2. **Depuración**: Consultar eventos específicos dentro de un rango de tiempo.
3. **Procesamiento batch**: Leer entradas en bloques para procesarlas de manera eficiente.

## Consideraciones
- `XRANGE` devuelve las entradas ordenadas por sus IDs en orden ascendente.
- Para leer en orden descendente, se puede usar el comando `XREVRANGE`.
- Si el stream no contiene entradas en el rango especificado, se devuelve una lista vacía.

## Ejemplo Avanzado
### Leer entradas con filtros específicos
```python
# Leer entradas en un rango con un límite específico
filtered_entries = client.xrange("eventos", min="1675900000000-0", max="1675999999999-0", count=10)
for message_id, fields in filtered_entries:
    print(f"ID: {message_id}, Datos: {fields}")
```

### Uso combinado con `XREVRANGE` en Go
```go
// Leer entradas en orden inverso
descendingEntries, err := client.XRevRange(ctx, "eventos", "+", "0-0").Result()
if err != nil {
	panic(err)
}

for _, entry := range descendingEntries {
	fmt.Printf("ID: %s, Datos: %v\n", entry.ID, entry.Values)
}
