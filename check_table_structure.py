from database import DatabaseManager

db = DatabaseManager()

# Verificar estructura de todas las tablas importantes
tablas = ['productos', 'clientes', 'pedidos', 'pedido_detalle', 'chat_logs']

for tabla in tablas:
    print(f"=== ESTRUCTURA DE LA TABLA {tabla.upper()} ===")
    result = db.execute_query(f"SHOW COLUMNS FROM {tabla}")
    
    if result:
        for campo in result:
            print(f"Campo: {campo['Field']} - Tipo: {campo['Type']}")
    else:
        print(f"Error al obtener la estructura de {tabla}")
    print("-" * 40)
