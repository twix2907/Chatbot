from database import DatabaseManager

db = DatabaseManager()

print("=== VERIFICACIÓN DE DATOS EN BASE DE DATOS ===")
print()

# Verificar clientes
print("📋 CLIENTES REGISTRADOS:")
clientes = db.execute_query("SELECT * FROM clientes")
if clientes:
    for cliente in clientes:
        print(f"  • ID: {cliente['id']}, Nombre: {cliente['nombre']}, Teléfono: {cliente['telefono']}")
else:
    print("  No hay clientes registrados")

print()

# Verificar pedidos
print("🛒 PEDIDOS REGISTRADOS:")
pedidos = db.execute_query("SELECT * FROM pedidos")
if pedidos:
    for pedido in pedidos:
        print(f"  • ID: {pedido['id']}, Cliente: {pedido['cliente_id']}, Fecha: {pedido['fecha']}, Estado: {pedido['estado']}")
else:
    print("  No hay pedidos registrados")

print()

# Verificar detalles de pedidos
print("📦 DETALLES DE PEDIDOS:")
detalles = db.execute_query("SELECT * FROM pedido_detalle")
if detalles:
    for detalle in detalles:
        print(f"  • Pedido: {detalle['pedido_id']}, Producto ID: {detalle['producto_id']}, Cantidad: {detalle['cantidad']}")
else:
    print("  No hay detalles de pedidos")

print()

# Verificar logs de chat
print("💬 LOGS DE CONVERSACIÓN:")
logs = db.execute_query("SELECT * FROM chat_logs ORDER BY timestamp DESC LIMIT 5")
if logs:
    for log in logs:
        print(f"  • Cliente: {log['cliente_id']}, Intent: {log['intent_detected']}, Mensaje: {log['user_message'][:50]}...")
else:
    print("  No hay logs de conversación")
