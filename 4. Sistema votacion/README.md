# Sistema de Votación con Redis

## 1. Descripción de un Sistema de Votación
Un sistema de votación permite a los usuarios expresar su aprobación o desaprobación sobre comentarios o publicaciones. Este sistema puede incluir:
- Incrementar y decrementar votos.
- Almacenar datos por usuarios para evitar múltiples votos.
- Generar métricas como el número total de votos.

### Ejemplo
Un usuario puede votar positivamente (+1) o negativamente (-1) en un comentario. El total de votos se almacena en Redis y se puede consultar en tiempo real.

## 2. Equivalente en SGBD como MySQL
En MySQL, el sistema de votación podría implementarse con una tabla estructurada de la siguiente manera:

```sql
CREATE TABLE votes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    vote INT NOT NULL, -- 1 para upvote, -1 para downvote
    UNIQUE (post_id, user_id)
);
```

Para registrar un voto, se usaría un `INSERT` o `UPDATE` dependiendo de si el usuario ya votó:

```sql
INSERT INTO votes (post_id, user_id, vote) VALUES (1, 123, 1)
ON DUPLICATE KEY UPDATE vote = 1;
```

## 3. ¿Podemos hacerlo con lo que ya sabemos de Redis?
Redis permite implementar sistemas de votación de manera eficiente utilizando operaciones como `INCR` y `DECR`, combinadas con estructuras como Hashes para almacenar votos por usuario.

### Ejemplo en Python
```python
import redis

r = redis.Redis()
post_id = "post:1"
user_id = "user:123"

# Registrar un voto
if not r.hexists(post_id, user_id):
    r.hset(post_id, user_id, 1)  # Registrar upvote
    r.incr(f"{post_id}:score")  # Incrementar el puntaje total
else:
    print("El usuario ya votó")

# Obtener el puntaje total
print(r.get(f"{post_id}:score"))
```

## 4. Condiciones de carrera 1/2
En sistemas concurrentes, dos usuarios pueden intentar votar simultáneamente, causando inconsistencias.

### Solución
Redis resuelve esto con comandos atómicos como `INCR` y `HSET`. Estos comandos garantizan que los datos se actualicen sin interferencia.

```python
# Comando atómico
with r.pipeline() as pipe:
    pipe.hset(post_id, user_id, 1)
    pipe.incr(f"{post_id}:score")
    pipe.execute()
```

## 5. Condiciones de carrera con concurrencia 2/2
En caso de alta concurrencia, puede ser necesario implementar bloqueos con `SETNX` para evitar conflictos:

```python
lock_key = f"{post_id}:lock"
if r.setnx(lock_key, 1):
    r.expire(lock_key, 5)  # Bloqueo de 5 segundos
    r.hset(post_id, user_id, 1)
    r.incr(f"{post_id}:score")
    r.delete(lock_key)
else:
    print("Otro proceso está actualizando")
```

## 6. Operaciones Atómicas
Redis garantiza la atomicidad de comandos como `INCR`, `DECR`, y `HSET`. Esto evita inconsistencias en sistemas con múltiples usuarios.

## 7. Repasando las características de un sistema de voto
Un sistema de votación debe cumplir con:
- Consistencia de datos.
- Soporte para concurrencia.
- Almacenamiento eficiente.
- Tiempo de respuesta rápido.

## 8. Incrementos y Decrementos
Redis permite incrementar o decrementar valores almacenados con `INCR` y `DECR`.

### Ejemplo en Python
```python
r.set("score", 0)
r.incr("score")  # Incrementa en 1
r.decr("score")  # Decrementa en 1
print(r.get("score"))
```

## 9. Incrementamos por un valor específico
Con `INCRBY`, podemos aumentar un valor en una cantidad definida.

### Ejemplo en Python
```python
r.incrby("score", 5)  # Incrementa en 5
```

## 10. Incrementos en Hashes
Redis permite realizar incrementos dentro de un Hash con `HINCRBY`.

### Ejemplo en Python
```python
r.hset("post:1", "votes", 10)
r.hincrby("post:1", "votes", 2)  # Incrementa en 2
print(r.hget("post:1", "votes"))
```

## 11. Contador de visitas en una página por día, mes y año
Redis puede usarse para rastrear visitas en múltiples niveles de granularidad:

### Ejemplo en Python
```python
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
month = datetime.now().strftime("%Y-%m")
year = datetime.now().strftime("%Y")

r.incr(f"visitas:{today}")
r.incr(f"visitas:{month}")
r.incr(f"visitas:{year}")

print(r.get(f"visitas:{today}"))
```

## 12. Implementando el Sistema de Votación
A continuación, se presenta un programa completo que integra todas las características anteriores.

### Programa Completo en Python
```python
import redis
from datetime import datetime

def votar(redis_client, post_id, user_id, voto):
    lock_key = f"{post_id}:lock"
    
    if redis_client.setnx(lock_key, 1):
        try:
            redis_client.expire(lock_key, 5)  # Bloqueo de 5 segundos
            if not redis_client.hexists(post_id, user_id):
                redis_client.hset(post_id, user_id, voto)
                if voto == 1:
                    redis_client.incr(f"{post_id}:score")
                elif voto == -1:
                    redis_client.decr(f"{post_id}:score")
            else:
                print("El usuario ya votó")
        finally:
            redis_client.delete(lock_key)
    else:
        print("Otro proceso está actualizando")

def obtener_puntaje(redis_client, post_id):
    return redis_client.get(f"{post_id}:score")

def contador_visitas(redis_client):
    today = datetime.now().strftime("%Y-%m-%d")
    redis_client.incr(f"visitas:{today}")
    return redis_client.get(f"visitas:{today}")

# Ejemplo de uso
r = redis.Redis()
votar(r, "post:1", "user:123", 1)
print(obtener_puntaje(r, "post:1"))
print(contador_visitas(r))
