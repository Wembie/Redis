# Comandos Básicos de Redis

## Operaciones de Clave-Valor
### Guardar un valor
```bash
SET key value
```
**Ejemplo:**  
```bash
SET user:1 "Juan"
```

### Leer un valor
```bash
GET key
```
**Ejemplo:**  
```bash
GET user:1
```

### Sobrescribir un valor existente
```bash
SET key new_value
```
**Ejemplo:**  
```bash
SET user:1 "Carlos"
```

---

## Operaciones con Listas
### Agregar elementos a una lista (al final)
```bash
RPUSH list_name value1 value2 ...
```
**Ejemplo:**  
```bash
RPUSH tasks "task1" "task2"
```

### Leer todos los elementos de una lista
```bash
LRANGE list_name start stop
```
**Ejemplo:**  
```bash
LRANGE tasks 0 -1
```

### Sobrescribir un elemento de la lista
```bash
LSET list_name index new_value
```
**Ejemplo:**  
```bash
LSET tasks 0 "updated_task1"
```

---

## Operaciones con Hashes
### Guardar campos y valores en un hash
```bash
HSET hash_name field value
```
**Ejemplo:**  
```bash
HSET user:1 name "Juan" age "25"
```

### Leer un campo específico de un hash
```bash
HGET hash_name field
```
**Ejemplo:**  
```bash
HGET user:1 name
```

### Leer todos los campos y valores de un hash
```bash
HGETALL hash_name
```
**Ejemplo:**  
```bash
HGETALL user:1
```

### Sobrescribir un campo en un hash
```bash
HSET hash_name field new_value
```
**Ejemplo:**  
```bash
HSET user:1 age "26"
```

---

## Eliminar Claves o Elementos
### Eliminar una clave
```bash
DEL key
```
**Ejemplo:**  
```bash
DEL user:1
```

### Eliminar un campo de un hash
```bash
HDEL hash_name field
```
**Ejemplo:**  
```bash
HDEL user:1 age
```

### Eliminar elementos de una lista
```bash
LREM list_name count value
```
**Ejemplo:**  
```bash
LREM tasks 1 "task2"
```

---

## Notas Adicionales
- **Ver todas las claves almacenadas:**  
  ```bash
  KEYS *
  ```

- **Ver el tipo de dato de una clave:**  
  ```bash
  TYPE key
  ```

---

## Uso de NX y XX en SET

### NX: Solo establecer si la clave no existe
- Este flag asegura que el valor solo se establecerá si la clave no existe.
```bash
SET key value NX
```
**Ejemplo:**  
```bash
SET user:2 "Pedro" NX
```

### XX: Solo establecer si la clave ya existe
- Este flag asegura que el valor solo se establecerá si la clave ya existe.
```bash
SET key value XX
```
**Ejemplo:**  
```bash
SET user:1 "Actualizado" XX
```

### Notas:
- Puedes combinar NX o XX con otros parámetros como `EX` (expiración en segundos) o `PX` (expiración en milisegundos).
  ```bash
  SET key value NX EX 10
  ```

---

## Consideraciones para Producción

### Evitar el uso de `KEYS *`
- El comando `KEYS *` devuelve todas las claves almacenadas en Redis. Sin embargo, en un entorno de producción, este comando **puede afectar severamente el rendimiento del servidor**, ya que bloquea el proceso hasta obtener todas las claves, lo que puede causar problemas graves si hay muchas claves almacenadas.

**Alternativa:** Usar `SCAN`
- En lugar de `KEYS *`, utiliza `SCAN` para realizar un escaneo iterativo de las claves. Esto es más seguro y evita bloquear el servidor.
```bash
SCAN cursor [MATCH pattern] [COUNT count]
```
**Ejemplo:**  
```bash
SCAN 0 MATCH "user:*" COUNT 100
```
- `cursor`: Inicialmente `0` y se actualiza con el valor devuelto por `SCAN` hasta que sea `0` nuevamente.
- `MATCH pattern`: Filtra las claves que coinciden con el patrón dado.
- `COUNT count`: Sugerencia para la cantidad de claves a escanear en cada iteración (no garantiza precisión).

**Beneficios de `SCAN`:**
1. No bloquea el servidor.
2. Puede usarse para manejar grandes cantidades de datos de manera eficiente.

### Recomendación
- Siempre evalúa el impacto de los comandos que utilizan Redis en producción.
- Monitorea las métricas de tu servidor para identificar cuellos de botella y optimizar consultas.

---

## Buenas Prácticas para Nombres de Claves

### Reglas Generales
1. **Usar prefijos claros:** Ayuda a organizar y categorizar las claves.
   - Ejemplo: `user:`, `order:`, `session:`
   ```bash
   SET user:123 "Juan"
   SET order:456 "Compra1"
   ```

2. **Separar niveles jerárquicos con delimitadores:** Utiliza `:` como separador para niveles lógicos.
   - Ejemplo: `user:123:settings` o `order:456:items`
   ```bash
   HSET user:123:settings theme "dark" language "es"
   ```

3. **Evitar claves demasiado largas:** Mantén las claves cortas para mejorar el rendimiento.
   - Malo: `user:12345678901234567890:details`
   - Bueno: `user:123:details`

4. **Incluir identificadores únicos:** Usa valores como IDs o timestamps para evitar colisiones.
   - Ejemplo:
   ```bash
   SET session:1627654321 "active"
   ```

### Ejemplo Completo
```bash
HSET user:101 name "Alice" email "alice@example.com"
HSET order:2023:001 status "shipped" total "99.99"
RPUSH log:2023:09 errors "Error1" "Error2"
```

### Documentación Relacionada
- [Redis Keys Best Practices](https://redis.io/docs/manual/key-patterns/)
- [Redis Data Modeling](https://redis.io/docs/manual/data-modeling/)

---

## Creación de Múltiples Bases de Datos en Redis

Redis permite trabajar con múltiples bases de datos en una misma instancia. Por defecto, la configuración básica incluye 16 bases de datos numeradas del `0` al `15`.

### Cambiar de Base de Datos
Usa el comando `SELECT` para cambiar entre bases de datos.
```bash
SELECT database_number
```
**Ejemplo:**
```bash
SELECT 1
```
Esto cambia a la base de datos número `1`.

### Problemas con el Uso de Múltiples Bases de Datos
1. **Falta de aislamiento adecuado:** Redis no tiene controles avanzados para gestionar accesos concurrentes o permisos separados para cada base de datos.
2. **Confusión en entornos complejos:** La separación lógica con múltiples bases puede ser difícil de rastrear y gestionar.
3. **Rendimiento:** Todas las bases de datos comparten los mismos recursos de la instancia, lo que puede causar cuellos de botella si una base tiene alta carga.

### Recomendación
Es preferible usar prefijos claros en las claves en lugar de múltiples bases de datos para simular partición lógica:
```bash
SET app1:user:1 "Juan"
SET app2:user:2 "Pedro"
```
Esto mantiene el sistema organizado y simplifica la administración.

---

## Uso de Namespaces

Un namespace en Redis es una forma de categorizar claves mediante prefijos. Es útil para mantener un orden lógico y evitar colisiones.

### Ejemplo de Namespace
```bash
SET app1:user:123 "Alice"
SET app1:order:456 "Compra1"
SET app2:user:789 "Bob"
```
En este caso:
- `app1` y `app2` son namespaces que separan datos de distintas aplicaciones.
- Los datos permanecen organizados y se pueden consultar con patrones específicos.

### Consulta con Namespaces
Utiliza `SCAN` con `MATCH` para buscar claves de un namespace:
```bash
SCAN 0 MATCH "app1:*" COUNT 100
```
Esto devuelve todas las claves que pertenecen al namespace `app1`.

### Beneficios
1. Facilita la organización y el mantenimiento.
2. Evita colisiones entre claves.
3. Simplifica la consulta de datos relacionados.

### Notas
- Los namespaces son una convención, no una característica nativa de Redis.
- Diseña claves cuidadosamente para aprovechar esta práctica al máximo.

