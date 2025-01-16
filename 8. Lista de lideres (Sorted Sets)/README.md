# Lista de líderes mediante Conjuntos Ordenados (Sorted Sets) en Redis

## 95. Listas de líderes. ¿Qué son? Veamos ejemplos...

Las listas de líderes son estructuras de datos que permiten mantener un ranking ordenado por puntuación. En Redis, se implementan mediante Sorted Sets, que asocian cada elemento con un valor de puntuación que determina su posición en la lista.

### Ejemplo:
```bash
ZADD leaderboard 100 "Alice"
ZADD leaderboard 200 "Bob"
ZADD leaderboard 150 "Charlie"
```
Esto añade a "Alice", "Bob" y "Charlie" al conjunto ordenado `leaderboard` con sus respectivas puntuaciones.

### Recuperar el ranking:
```bash
ZRANGE leaderboard 0 -1 WITHSCORES
```
Este comando muestra el ranking completo con puntuaciones.

---

## 96. Conjuntos Ordenados. Definición.

Los Sorted Sets en Redis son estructuras de datos que combinan características de conjuntos y listas. Cada elemento tiene una puntuación asociada, y los elementos están ordenados según esta puntuación.

### Características:
1. Sin duplicados.
2. Ordenados por puntuación.

---

## 97. Añadiendo elementos en un conjunto ordenado

Usamos el comando `ZADD` para insertar elementos en un conjunto ordenado.

### Ejemplo:
```bash
ZADD leaderboard 300 "Daniel"
```
Esto añade a "Daniel" con una puntuación de 300.

---

## 98. Sobreescribiendo valores

Si se añade un elemento existente con una nueva puntuación, esta se actualiza automáticamente.

### Ejemplo:
```bash
ZADD leaderboard 350 "Daniel"
```
Esto actualiza la puntuación de "Daniel" a 350.

---

## 99. Listando elementos en el conjunto ordenado

Para listar los elementos según su orden:

### Ejemplo:
```bash
ZRANGE leaderboard 0 -1
```
Este comando devuelve todos los elementos ordenados por puntuación.

---

## 100. Cardinalidad y contando elementos entre rangos

Puedes contar elementos con `ZCARD` o elementos en un rango de puntuación con `ZCOUNT`.

### Ejemplo:
```bash
ZCARD leaderboard
ZCOUNT leaderboard 100 200
```
El primer comando devuelve el total de elementos, y el segundo cuenta cuántos tienen puntuaciones entre 100 y 200.

---

## 101. Incrementando un valor

Usa `ZINCRBY` para incrementar la puntuación de un elemento.

### Ejemplo:
```bash
ZINCRBY leaderboard 50 "Alice"
```
Esto aumenta la puntuación de "Alice" en 50.

---

## 102. ¿Qué puntuación tenemos en un ranking? ¿En qué posición estamos?

Para obtener la puntuación y posición de un elemento:

### Ejemplo:
```bash
ZSCORE leaderboard "Alice"
ZRANK leaderboard "Alice"
```
`ZSCORE` devuelve la puntuación, y `ZRANK` la posición (empezando desde 0).

---

## 103. Borrando elementos del conjunto y conclusiones

Puedes borrar elementos con `ZREM`.

### Ejemplo:
```bash
ZREM leaderboard "Bob"
```
Esto elimina a "Bob" del conjunto ordenado.

### Conclusión:
Los conjuntos ordenados son ideales para implementar rankings eficientes en tiempo real.

---

## 104. Caso práctico: Lista de líderes de los libros con más puntuación

### Supongamos:
Queremos un ranking de libros basado en su popularidad.

### Implementación:
```bash
ZADD books 100 "Book A"
ZADD books 150 "Book B"
ZADD books 120 "Book C"
```

### Ver el ranking:
```bash
ZRANGE books 0 -1 WITHSCORES
```
Este comando devuelve el ranking completo de libros con sus puntuaciones.

### Incrementar popularidad:
```bash
ZINCRBY books 30 "Book A"
```
Esto incrementa la puntuación de "Book A" en 30.

### Ver el libro más popular:
```bash
ZRANGE books -1 -1 WITHSCORES
```
Devuelve el libro con la puntuación más alta.
