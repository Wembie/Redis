# Sección 9: Listas - El poder de enumerar cosas

## 83. ¿Qué diferencia hay entre una Lista y un Array? ¿Qué usa Redis internamente?

Redis utiliza internamente estructuras de datos conocidas como **listas**. Una lista en Redis es una colección ordenada de cadenas, implementada como una lista vinculada o como un arreglo comprimido dependiendo de su tamaño.

- **Lista**: Permite operaciones rápidas de inserción y eliminación al principio o al final.
- **Array**: Es más eficiente para acceso aleatorio a elementos específicos, pero no está diseñado para operaciones frecuentes de inserción y eliminación.

Redis usa listas para representar datos que necesitan mantener un orden estricto.

### Ejemplo en consola Redis:
```shell
LPUSH lista "elemento1"
RPUSH lista "elemento2"
LRANGE lista 0 -1  # Devuelve todos los elementos de la lista
```

### Ejemplo en Python:
```python
import redis

r = redis.Redis()
r.lpush("lista", "elemento1")
r.rpush("lista", "elemento2")
print(r.lrange("lista", 0, -1))  # Devuelve: [b'elemento1', b'elemento2']
```

---

## 84. ¿Cuándo usar listas?

Las listas son útiles cuando necesitas:
- Mantener el orden de los elementos.
- Implementar colas (FIFO) o pilas (LIFO).
- Agregar o eliminar datos frecuentemente al principio o al final.

---

## 85. Casos de uso habituales con Listas

1. **Colas de procesamiento**: Procesar tareas en orden.
2. **Historiales**: Almacenar el historial de acciones (por ejemplo, navegación web).
3. **Chats o mensajes**: Almacenar mensajes en aplicaciones de mensajería.

---

## 86. Añadiendo elementos al principio de una lista

En Redis, `LPUSH` agrega elementos al principio de la lista.

### Ejemplo en consola Redis:
```shell
LPUSH mi_lista "primero"
LPUSH mi_lista "segundo"
LRANGE mi_lista 0 -1
```

### Ejemplo en Python:
```python
r.lpush("mi_lista", "primero")
r.lpush("mi_lista", "segundo")
print(r.lrange("mi_lista", 0, -1))  # Devuelve: [b'segundo', b'primero']
```

---

## 87. Añadiendo elementos al final de una lista

En Redis, `RPUSH` agrega elementos al final de la lista.

### Ejemplo en consola Redis:
```shell
RPUSH mi_lista "ultimo"
RPUSH mi_lista "final"
LRANGE mi_lista 0 -1
```

### Ejemplo en Python:
```python
r.rpush("mi_lista", "ultimo")
r.rpush("mi_lista", "final")
print(r.lrange("mi_lista", 0, -1))  # Devuelve: [b'primero', b'segundo', b'ultimo', b'final']
```

---

## 88. Enumerando elementos de una lista

`LRANGE` permite obtener un rango específico de elementos de la lista.

### Ejemplo en consola Redis:
```shell
LRANGE mi_lista 0 -1  # Devuelve todos los elementos
```

### Ejemplo en Python:
```python
print(r.lrange("mi_lista", 0, -1))  # Devuelve: [b'primero', b'segundo', b'ultimo', b'final']
```

---

## 89. Longitud de una lista

`LLEN` devuelve el número de elementos en una lista.

### Ejemplo en consola Redis:
```shell
LLEN mi_lista
```

### Ejemplo en Python:
```python
print(r.llen("mi_lista"))  # Devuelve: 4
```

---

## 90. Borrando elementos de la lista

`LREM` elimina elementos específicos de una lista.

### Ejemplo en consola Redis:
```shell
LREM mi_lista 1 "primero"  # Elimina una aparición de "primero"
LRANGE mi_lista 0 -1
```

### Ejemplo en Python:
```python
r.lrem("mi_lista", 1, "primero")
print(r.lrange("mi_lista", 0, -1))  # Devuelve: [b'segundo', b'ultimo', b'final']
```

---

## 91. Leyendo y borrando elementos del principio y final

- `LPOP` elimina y devuelve el primer elemento.
- `RPOP` elimina y devuelve el último elemento.

### Ejemplo en consola Redis:
```shell
LPOP mi_lista
RPOP mi_lista
```

### Ejemplo en Python:
```python
print(r.lpop("mi_lista"))  # Devuelve: b'segundo'
print(r.rpop("mi_lista"))  # Devuelve: b'final'
```

---

## 92. Borrado automático de listas

Cuando una lista queda vacía, Redis la elimina automáticamente para ahorrar recursos.

---

## 93. Colecciones Limitadas (Capped Collections)

Con `LTRIM`, puedes limitar el tamaño de una lista, manteniendo solo los elementos más recientes.

### Ejemplo en consola Redis:
```shell
RPUSH mi_lista "1" "2" "3" "4"
LTRIM mi_lista -3 -1  # Conserva los últimos 3 elementos
```

### Ejemplo en Python:
```python
r.rpush("mi_lista", "1", "2", "3", "4")
r.ltrim("mi_lista", -3, -1)
print(r.lrange("mi_lista", 0, -1))  # Devuelve: [b'2', b'3', b'4']
```

---

## 94. Caso Real: Usando listas limitadas

Un uso común de listas limitadas es registrar los últimos eventos de un usuario o los mensajes recientes en un chat.

### Ejemplo en Python:
```python
def registrar_evento(r, usuario, evento):
    clave = f"eventos:{usuario}"
    r.rpush(clave, evento)
    r.ltrim(clave, -10, -1)  # Mantiene solo los últimos 10 eventos

registrar_evento(r, "juan", "Inicio de sesión")
registrar_evento(r, "juan", "Cerró sesión")
print(r.lrange("eventos:juan", 0, -1))
```

### Resultado:
```plaintext
[b'Inicio de sesión', b'Cerró sesión']
