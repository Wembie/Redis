# Redis como Cache

Redis es ampliamente utilizado como sistema de caché debido a su velocidad y flexibilidad. A continuación, se describen estrategias de cacheado, explicaciones detalladas y ejemplos de casos reales para entender mejor su uso.

---

## Estrategias de Cacheado

### 1. **Cache Bajo Demanda**
Esta estrategia almacena datos en la caché solo cuando se solicitan por primera vez. Si los datos no existen en la caché, se recuperan del origen y se almacenan para futuras consultas.

#### Ventajas
- Fácil de implementar.
- Reduce el uso innecesario de memoria, ya que solo almacena datos solicitados.

#### Desventajas
- La primera consulta a los datos no almacenados puede ser lenta, ya que necesita acceder al origen.

#### Ejemplo
```python
import redis

cache = redis.Redis()

def get_user(user_id):
    key = f"user:{user_id}"
    user_data = cache.get(key)

    if user_data:
        print("Datos obtenidos de la caché.")
        return user_data

    print("Datos no encontrados en caché. Consultando la base de datos...")
    user_data = query_database(user_id)  # Supongamos que esta función consulta la base de datos.
    cache.set(key, user_data, ex=3600)  # Cachea el dato durante 1 hora.
    return user_data
```

---

### 2. **Cache Precalentado**
En esta estrategia, la caché se llena proactivamente con datos predecibles o comúnmente solicitados, antes de que sean necesarios.

#### Ventajas
- Reduce la latencia para consultas frecuentes.
- Asegura que los datos importantes estén siempre disponibles.

#### Desventajas
- Incrementa el uso de memoria al almacenar datos que pueden no ser utilizados.

#### Ejemplo
```python
import redis

cache = redis.Redis()

def precache_users(user_ids):
    for user_id in user_ids:
        key = f"user:{user_id}"
        if not cache.exists(key):
            user_data = query_database(user_id)  # Consulta la base de datos.
            cache.set(key, user_data, ex=3600)  # Cachea cada dato durante 1 hora.

# Precalentar la caché con usuarios comunes
precache_users([1, 2, 3, 4, 5])
```

---

### 3. **Cache Basada en Expiración**
Configurar tiempos de expiración ayuda a invalidar automáticamente datos obsoletos y gestionar el uso de memoria de forma eficiente.

#### Ejemplo
```python
cache.set("session:123", "active", ex=300)  # Sesión válida por 5 minutos.
```

---

### 4. **Cache de Escritura-Determinada**
Actualiza o elimina datos en la caché cuando ocurren cambios en el origen de datos.

#### Ejemplo
```python
def update_user(user_id, new_data):
    key = f"user:{user_id}"
    update_database(user_id, new_data)  # Actualiza los datos en la base de datos.
    cache.set(key, new_data, ex=3600)   # Actualiza los datos en la caché.
```

---

## Ejemplo en un Caso Real

Imagina que estás desarrollando una plataforma de comercio electrónico y necesitas optimizar el tiempo de respuesta al cargar información de productos.

### Solución con Redis

1. **Precacheado de Productos Populares**
   - Al iniciar el sistema, los productos más vendidos se cargan en la caché.
2. **Bajo Demanda para Productos Raros**
   - Los productos menos consultados se cargan a la caché solo cuando son requeridos.
3. **Expiración Configurada**
   - Cada producto tiene un tiempo de expiración para asegurar que los precios y detalles estén actualizados.

#### Implementación
```python
import redis

cache = redis.Redis()

def get_product(product_id):
    key = f"product:{product_id}"
    product_data = cache.get(key)

    if product_data:
        return product_data

    product_data = query_database(product_id)  # Simula una consulta a la base de datos.
    cache.set(key, product_data, ex=3600)  # Configura una expiración de 1 hora.
    return product_data

# Precachear productos populares
popular_products = ["1001", "1002", "1003"]
for product_id in popular_products:
    if not cache.exists(f"product:{product_id}"):
        product_data = query_database(product_id)
        cache.set(f"product:{product_id}", product_data, ex=3600)
```

---

## Consideraciones Adicionales

### Evitar Datos Obsoletos
Asegúrate de invalidar o actualizar datos en la caché cada vez que cambien en el origen. 

### Elegir el Algoritmo de Expulsión Adecuado
Redis soporta varios algoritmos para manejar la eliminación de claves cuando la memoria está llena:
- `volatile-lru`: Elimina las claves menos usadas recientemente con tiempo de expiración.
- `allkeys-lru`: Elimina las claves menos usadas recientemente, sin importar si tienen tiempo de expiración.

Configura esto en el archivo `redis.conf`:
```bash
maxmemory-policy allkeys-lru
```

### Documentación Relacionada
- [Redis Caching Patterns](https://redis.io/docs/manual/cache/)
- [Best Practices for Redis](https://redis.io/docs/manual/best-practices/)
