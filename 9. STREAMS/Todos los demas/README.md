# Sistema de Mensajería Redis Streams

## Índice
1. [Stream de Mensajes](#stream-de-mensajes)
2. [Lectura de Streams](#lectura-de-streams)
3. [Grupos de Consumidores](#grupos-de-consumidores)
4. [Información del Stream](#información-del-stream)
5. [Comandos Auxiliares](#comandos-auxiliares)
6. [Ejemplos Prácticos](#ejemplos-prácticos)
7. [Mejores Prácticas](#mejores-prácticas)

## Stream de Mensajes

### XADD
Agrega un nuevo mensaje a un stream con campos clave-valor.

```python
# Python ejemplo
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Agregar mensaje con campos clave-valor
message_id = r.xadd('mystream', 
                    {'sensor': 'temperatura',
                     'valor': '25.5',
                     'timestamp': '1642345678'})
```

```go
// Go ejemplo
import (
    "github.com/redis/go-redis/v8"
    "context"
)

client := redis.NewClient(&redis.Options{
    Addr: "localhost:6379",
})

// Agregar mensaje
messageID, err := client.XAdd(context.Background(), &redis.XAddArgs{
    Stream: "mystream",
    Values: map[string]interface{}{
        "sensor": "temperatura",
        "valor": "25.5",
        "timestamp": "1642345678",
    },
}).Result()
```

## Lectura de Streams

### XREAD
Lee mensajes nuevos de uno o más streams.

```python
# Python ejemplo
# Lectura no bloqueante
streams = {'mystream': '0-0'}  # Desde el principio
messages = r.xread(streams)

# Lectura bloqueante con timeout
messages = r.xread(streams, block=5000)  # Timeout 5 segundos
```

```go
// Go ejemplo
streams := []string{"mystream", "0-0"}
messages, err := client.XRead(context.Background(), &redis.XReadArgs{
    Streams: streams,
    Block:   5000,  // Timeout 5 segundos
}).Result()
```

### XREADGROUP
Lee mensajes como parte de un grupo de consumidores.

```python
# Python ejemplo
# Leer mensajes nuevos para este consumidor
messages = r.xreadgroup('mygroup', 'consumer1',
                       {'mystream': '>'})

# Leer mensajes pendientes
messages = r.xreadgroup('mygroup', 'consumer1',
                       {'mystream': '0'})
```

```go
// Go ejemplo
messages, err := client.XReadGroup(context.Background(), &redis.XReadGroupArgs{
    Group:    "mygroup",
    Consumer: "consumer1",
    Streams:  []string{"mystream", ">"},
}).Result()
```

## Grupos de Consumidores

### XGROUP CREATE
Crea un nuevo grupo de consumidores.

```python
# Python ejemplo
# Crear grupo desde el inicio del stream
r.xgroup_create('mystream', 'mygroup', '0')

# Crear grupo desde el último mensaje
r.xgroup_create('mystream', 'mygroup', '$')

# Crear grupo y stream si no existe
r.xgroup_create('mystream', 'mygroup', '0', mkstream=True)
```

```go
// Go ejemplo
// Crear grupo
err := client.XGroupCreate(context.Background(), "mystream", "mygroup", "0").Err()

// Crear grupo desde último mensaje
err = client.XGroupCreate(context.Background(), "mystream", "mygroup", "$").Err()
```

### XACK
Confirma el procesamiento de mensajes en un grupo.

```python
# Python ejemplo
# Confirmar un mensaje
r.xack('mystream', 'mygroup', 'message-id-1')

# Confirmar múltiples mensajes
r.xack('mystream', 'mygroup', 
       'message-id-1', 'message-id-2', 'message-id-3')
```

```go
// Go ejemplo
// Confirmar mensaje
err := client.XAck(context.Background(), "mystream", "mygroup", "message-id-1").Err()
```

### XAUTOCLAIM
Reclama automáticamente mensajes pendientes.

```python
# Python ejemplo
# Reclamar mensajes pendientes más antiguos que 30 minutos
messages = r.xautoclaim(
    'mystream', 'mygroup', 'consumer1',
    min_idle_time=1800000,  # 30 minutos en ms
    start_id='0-0'
)
```

```go
// Go ejemplo
messages, err := client.XAutoClaimMessages(context.Background(), &redis.XAutoClaimArgs{
    Stream:   "mystream",
    Group:    "mygroup",
    Consumer: "consumer1",
    MinIdle:  30 * time.Minute,
    Start:    "0-0",
}).Result()
```

## Información del Stream

### XINFO STREAM
Obtiene información detallada sobre un stream.

```python
# Python ejemplo
# Obtener información del stream
info = r.xinfo_stream('mystream')

# Obtener información de los grupos de consumidores
groups_info = r.xinfo_groups('mystream')

# Obtener información de los consumidores de un grupo
consumers_info = r.xinfo_consumers('mystream', 'mygroup')
```

```go
// Go ejemplo
// Obtener información del stream
info, err := client.XInfoStream(context.Background(), "mystream").Result()

// Obtener información de grupos
groupsInfo, err := client.XInfoGroups(context.Background(), "mystream").Result()
```

### XTRIM
Limita el tamaño del stream.

```python
# Python ejemplo
# Mantener solo los últimos 1000 mensajes
r.xtrim('mystream', maxlen=1000)

# Aproximación (~) para mejor rendimiento
r.xtrim('mystream', maxlen=1000, approximate=True)
```

```go
// Go ejemplo
// Limitar tamaño del stream
err := client.XTrimMaxLen(context.Background(), "mystream", 1000).Err()

// Con aproximación
err = client.XTrimMaxLen(context.Background(), "mystream", 1000, redis.XTrimApprox).Err()
```

## Comandos Auxiliares

### XRANGE y XREVRANGE
Lee un rango de mensajes en orden normal o inverso.

```python
# Python ejemplo
# Leer rango de mensajes
messages = r.xrange('mystream', 
                   min='-',      # Desde el inicio
                   max='+',      # Hasta el final
                   count=100)    # Límite de mensajes

# Leer en orden inverso
messages = r.xrevrange('mystream',
                      max='+',    # Desde el final
                      min='-',    # Hasta el inicio
                      count=100)  # Límite de mensajes
```

```go
// Go ejemplo
// Leer rango de mensajes
messages, err := client.XRange(context.Background(), "mystream", "-", "+").Result()

// Leer en orden inverso
messages, err = client.XRevRange(context.Background(), "mystream", "+", "-").Result()
```

### XCLAIM
Reclama mensajes específicos para un consumidor.

```python
# Python ejemplo
# Reclamar mensajes específicos
messages = r.xclaim('mystream', 'mygroup', 'consumer1',
                   min_idle_time=60000,  # 1 minuto en ms
                   message_ids=['message-id-1', 'message-id-2'])
```

```go
// Go ejemplo
messages, err := client.XClaim(context.Background(), &redis.XClaimArgs{
    Stream:   "mystream",
    Group:    "mygroup",
    Consumer: "consumer1",
    MinIdle:  time.Minute,
    Messages: []string{"message-id-1", "message-id-2"},
}).Result()
```

## Ejemplos Prácticos

### Sistema de Procesamiento Distribuido

```python
import redis
import json
from datetime import datetime
import time

class StreamProcessor:
    def __init__(self, stream_name, group_name, consumer_name):
        self.redis = redis.Redis(decode_responses=True)
        self.stream_name = stream_name
        self.group_name = group_name
        self.consumer_name = consumer_name
        
        # Asegurar que existe el grupo
        try:
            self.redis.xgroup_create(stream_name, group_name, '0', mkstream=True)
        except redis.exceptions.ResponseError:
            # Grupo ya existe
            pass
            
    def process_messages(self):
        while True:
            try:
                # Leer nuevos mensajes
                messages = self.redis.xreadgroup(
                    self.group_name,
                    self.consumer_name,
                    {self.stream_name: '>'},
                    count=10,
                    block=5000
                )
                
                if not messages:
                    continue
                    
                for message in messages[0][1]:
                    message_id = message[0]
                    data = message[1]
                    
                    try:
                        # Procesar mensaje
                        self.process_single_message(data)
                        
                        # Confirmar procesamiento
                        self.redis.xack(
                            self.stream_name,
                            self.group_name,
                            message_id
                        )
                    except Exception as e:
                        print(f"Error procesando mensaje {message_id}: {e}")
                        
            except Exception as e:
                print(f"Error en el procesamiento: {e}")
                time.sleep(1)
                
    def process_single_message(self, data):
        # Implementar lógica de procesamiento específica
        print(f"Procesando mensaje: {data}")
```

### Sistema de Monitoreo

```python
class StreamMonitor:
    def __init__(self, stream_name):
        self.redis = redis.Redis(decode_responses=True)
        self.stream_name = stream_name
        
    def monitor_stream_size(self):
        """Monitorea el tamaño del stream y mantiene un límite"""
        while True:
            try:
                # Obtener información del stream
                info = self.redis.xinfo_stream(self.stream_name)
                length = info['length']
                
                print(f"Tamaño actual del stream: {length}")
                
                # Mantener el stream en un tamaño manejable
                if length > 10000:
                    self.redis.xtrim(self.stream_name, 
                                   maxlen=5000, 
                                   approximate=True)
                    
            except Exception as e:
                print(f"Error en monitoreo: {e}")
            
            time.sleep(60)  # Verificar cada minuto
            
    def monitor_pending_messages(self, group_name):
        """Monitorea mensajes pendientes en un grupo"""
        while True:
            try:
                # Obtener información de mensajes pendientes
                pending = self.redis.xpending(self.stream_name, group_name)
                
                if pending['pending'] > 0:
                    print(f"Mensajes pendientes: {pending['pending']}")
                    
                    # Obtener detalles de mensajes pendientes
                    details = self.redis.xpending_range(
                        self.stream_name,
                        group_name,
                        min='-',
                        max='+',
                        count=10
                    )
                    
                    for msg in details:
                        print(f"Mensaje {msg['message_id']} pendiente por "
                              f"{msg['time_since_delivered']}ms")
                
            except Exception as e:
                print(f"Error monitoreando pendientes: {e}")
                
            time.sleep(30)  # Verificar cada 30 segundos
```

## Mejores Prácticas

1. **Gestión de Mensajes**
   - Utilizar IDs de mensaje significativos cuando sea posible
   - Implementar reintentos para mensajes fallidos
   - Mantener un tamaño manejable del stream con XTRIM

2. **Grupos de Consumidores**
   - Crear consumidores específicos para cada worker
   - Implementar heartbeat para detectar consumidores caídos
   - Usar XAUTOCLAIM para recuperar mensajes de consumidores inactivos

3. **Monitoreo**
   - Mantener registro de mensajes procesados/fallidos
   - Monitorear regularmente el tamaño del stream
   - Verificar mensajes pendientes periódicamente

4. **Rendimiento**
   - Usar aproximación en XTRIM para mejor performance
   - Procesar mensajes en lotes cuando sea posible
   - Implementar timeout en operaciones bloqueantes

5. **Recuperación de Errores**
   - Implementar circuit breaker para conexiones Redis
   - Manejar reconexiones automáticas
   - Mantener log de errores detallado

