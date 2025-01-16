import redis

# Conexión al servidor Redis
client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Nombre del stream
stream_name = "user_activity"

# Función para agregar eventos al stream
def add_events():
    events = [
        {"user": "juan", "event": "login"},
        {"user": "maria", "event": "compra", "item": "laptop"},
        {"user": "carlos", "event": "logout"},
    ]
    for event in events:
        client.xadd(stream_name, event)
    print(f"{len(events)} eventos añadidos al stream '{stream_name}'.")

# Función para leer eventos desde el stream
def read_events():
    entries = client.xread({stream_name: "0-0"}, count=10)
    print("\nEventos leídos:")
    for stream, messages in entries:
        for message_id, fields in messages:
            print(f"ID: {message_id}, Datos: {fields}")

# Función para recuperar un rango de eventos
def range_events():
    entries = client.xrange(stream_name, min="0-0", max="+", count=5)
    print("\nEventos en rango:")
    for message_id, fields in entries:
        print(f"ID: {message_id}, Datos: {fields}")

# Función para obtener la longitud del stream
def stream_length():
    length = client.xlen(stream_name)
    print(f"\nLongitud del stream '{stream_name}': {length}")

# Simulación completa
if __name__ == "__main__":
    add_events()
    read_events()
    range_events()
    stream_length()
