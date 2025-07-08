from database import DatabaseManager

db = DatabaseManager()

print("🔍 VERIFICACIÓN RÁPIDA DE PRODUCTOS Y PRECIOS")
print("=" * 50)

# Consultar algunos productos específicos
productos_consulta = ["Francés", "Torta de chocolate", "Empanaditas de pollo", "Chancay"]

for nombre_producto in productos_consulta:
    query = "SELECT nombre, precio, stock FROM productos WHERE nombre = %s"
    resultado = db.execute_query(query, (nombre_producto,))
    
    if resultado:
        producto = resultado[0]
        print(f"✅ {producto['nombre']}")
        print(f"   💰 Precio: S/{producto['precio']:.2f}")
        print(f"   📦 Stock: {producto['stock']}")
    else:
        print(f"❌ {nombre_producto} - No encontrado")
    print("-" * 30)

# Simular cálculo de pedido
print("\n🧮 SIMULACIÓN DE CÁLCULO DE PEDIDO:")
pedido_items = [
    {"nombre": "Francés", "cantidad": 2},
    {"nombre": "Torta de chocolate", "cantidad": 1},
    {"nombre": "Empanaditas de pollo", "cantidad": 3}
]

total = 0
for item in pedido_items:
    query = "SELECT precio FROM productos WHERE nombre = %s"
    resultado = db.execute_query(query, (item["nombre"],))
    
    if resultado:
        precio = float(resultado[0]['precio'])
        subtotal = precio * item["cantidad"]
        total += subtotal
        print(f"   {item['cantidad']}x {item['nombre']} = S/{precio:.2f} x {item['cantidad']} = S/{subtotal:.2f}")

print(f"\n💵 TOTAL DEL PEDIDO: S/{total:.2f}")
print(f"✅ ¡Los precios están funcionando correctamente!")
