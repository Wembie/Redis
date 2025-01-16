# Limitador de Peticiones (Rate Limiter) en Redis

## Introducción
Un **limitador de peticiones** (Rate Limiter) es una herramienta que restringe el número de solicitudes que un cliente puede realizar en un periodo de tiempo específico. Se utiliza ampliamente para evitar abusos en APIs, controlar tráfico y garantizar la estabilidad del sistema.

Redis es una opción ideal para implementar un limitador de peticiones debido a su alta velocidad y capacidades de manipulación de datos en memoria.

---

## 1. ¿Qué es un limitador de peticiones y para qué sirve?
Un limitador de peticiones:
- Restringe el número de solicitudes que un cliente puede realizar en un intervalo de tiempo.
- Protege los recursos del servidor contra abusos.
- Mejora la calidad del servicio al repartir las solicitudes de manera equitativa entre los usuarios.

**Ejemplo de uso:**
- Permitir hasta 10 solicitudes por minuto por usuario en una API REST.

---

## 2. ¿Hay una única forma de implementar un limitador?
No, existen varias estrategias para implementar un limitador de peticiones, entre ellas:

1. **Token Bucket:** Utiliza un "balde" con tokens que se consumen por cada solicitud. Los tokens se recargan a un ritmo constante.
2. **Sliding Window Log:** Almacena un registro de timestamps para cada solicitud en una ventana de tiempo móvil.
3. **Fixed Window Counter:** Usa un contador para un periodo fijo de tiempo (por ejemplo, 1 minuto).
4. **Sliding Window Counter:** Similar al anterior, pero con una ventana móvil para mayor precisión.

Redis puede soportar todas estas estrategias con operaciones simples y rápidas.

---

## 3. Implementación simple y efectiva en Redis
La estrategia de **Fixed Window Counter** es la más sencilla y efectiva para comenzar. Redis maneja esto eficientemente con sus operaciones atómicas como `INCR` y `EXPIRE`.

### Ejemplo en Python
```python
import time
import redis

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Configuración del límite
LIMIT = 10  # Número máximo de solicitudes
PERIOD = 60  # Periodo de tiempo en segundos

# Función para limitar las peticiones
def is_rate_limited(client_id):
    key = f"rate_limit:{client_id}"
    current_count = r.get(key)

    if current_count is None:
        # Primera solicitud, inicializamos el contador
        r.set(key, 1, ex=PERIOD)
        return False

    if int(current_count) < LIMIT:
        # Incrementamos el contador si no se ha alcanzado el límite
        r.incr(key)
        return False

    # Límite alcanzado
    return True

# Pruebas
client_id = "user_123"
for i in range(15):
    if is_rate_limited(client_id):
        print(f"Solicitud {i + 1}: Bloqueada (Rate Limited)")
    else:
        print(f"Solicitud {i + 1}: Permitida")
    time.sleep(2)  # Simulamos tiempo entre solicitudes
```

---

### Ejemplo en la consola Redis
```bash
# Configuramos una clave con expiración
SET rate_limit:user_123 1 EX 60

# Incrementamos el contador
INCR rate_limit:user_123

# Obtenemos el valor actual
GET rate_limit:user_123
```

---

## 4. Cómo funciona un bloqueador de peticiones en el mundo real
### Escenario
Una API que permite un máximo de 100 solicitudes por usuario cada hora.

#### Solución
Utilizamos Redis con el comando `INCRBY` para incrementar el contador de solicitudes en cada llamada y `EXPIRE` para restablecerlo cada hora.

```python
LIMIT = 100
PERIOD = 3600  # 1 hora en segundos

# Modificamos la función para adaptarla

def is_rate_limited(client_id):
    key = f"rate_limit:{client_id}"
    if r.incr(key) == 1:
        r.expire(key, PERIOD)
    
    return int(r.get(key)) > LIMIT
```

### Ventajas de este enfoque
- **Eficiencia:** Redis maneja operaciones en milisegundos.
- **Escalabilidad:** Redis puede manejar miles de usuarios concurrentes.

---

## 5. Mejorando el limitador con Sliding Window Log
Para casos que requieren mayor precisión, implementamos un registro de timestamps para cada solicitud.

### Ejemplo en Python
```python
import redis
import time

LIMIT = 10
PERIOD = 60

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def is_rate_limited_sliding_window(client_id):
    key = f"sliding_window:{client_id}"
    now = time.time()

    # Agregamos el timestamp actual al conjunto ordenado
    r.zadd(key, {now: now})

    # Eliminamos los timestamps fuera del periodo
    r.zremrangebyscore(key, 0, now - PERIOD)

    # Contamos las solicitudes en la ventana
    request_count = r.zcard(key)

    # Configuramos una expiración para el conjunto
    r.expire(key, PERIOD)

    return request_count > LIMIT

# Pruebas
client_id = "user_456"
for i in range(15):
    if is_rate_limited_sliding_window(client_id):
        print(f"Solicitud {i + 1}: Bloqueada (Rate Limited)")
    else:
        print(f"Solicitud {i + 1}: Permitida")
    time.sleep(1)
```

---

## Conclusión
Redis ofrece una base sólida para implementar diferentes estrategias de limitación de peticiones, desde enfoques simples hasta avanzados como ventanas deslizantes. Este documento demuestra cómo iniciar y personalizar un limitador de peticiones de acuerdo a tus necesidades.
