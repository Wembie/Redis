# ![La Salle BES](http://jcarreras.es/images/lasalle.png)

# ![screenshot](.screenshot.png)

# Descripción
-----------------------

Uso práctico de Redis en una página principal.

En este ejercicio se muestran los diferentes enfoques de políticas de cache, para ello se ha dispuesto de diferentes bloques, cada uno de ellos
aplicando una política de cache diferente.

- Bloque cabecera página: se sirve el contenido de cache, si no existe se guarda indefinidamente
- Bloque Top comentarios de la semana: Se espera que ya esté en cache, si no hay nada, no muestra ningún elemento
- Bloque páginas mas visitadas: Tiene un TTL de un minuto, cuando expire se volverá a meter en cache el contenido
- Bloque artículos: se sirve el contenido de cache, si no existe se guarda indefinidamente

Cada uno de los sistemas tiene su propósito, ventajas e inconvenientes.

Para simular un lento acceso a datos, se ha creado `App\Home\Home.php` que en cada función hay 'sleep's para simular que hacemos
una consulta pesada en base de datos, que tarda en devolver resultados.

Al cargar la página, se podrá ver en la parte inferior que se ha puesto un contador que indica el tiempo de carga de la misma.


# Instalación
-----------------------

```
$ make install
```


# Instrucciones
-----------------------

- Ejecuta `make up` para levantar el entorno
- Revisa el código del fichero `App\Home\Home.php` así como `index.php`
- Entra en el navegador `http://localhost:8080/`
- Anota cuanto tiempo ha tarda en cargar la página. Recarga un par de veces más, y anota los tiempos.
- Si ahora entras en `http://localhost:8080/?cache=1` se hará uso de la cache. Anota el tiempo de carga de la página.
- Como habrás notado, no todos los bloques de la página son mostrados, puesto que el apartado 'top comentarios de la semana' necesita estar ya en cache
- Abajo de la página verás un enlace 'Precalentar cache', lee el fichero `heatcache.php` y después pulsa el enlace
- Recarga la página y deberías ver todas las secciones
- Si sigues recargando la página, cuanto tiempo tarda?
- Si haces click en el link 'Flush-All' y vuelves a recargar la página, ves diferentes tiempos?


# Desinstalación
-----------------------

```
$ make down
```
