from database import DatabaseManager

db = DatabaseManager()

print("=== PRODUCTOS EN BASE DE DATOS ===")
productos = db.execute_query("SELECT * FROM productos")

if productos:
    for producto in productos:
        print(f"ID: {producto['id']}")
        print(f"Nombre: {producto['nombre']}")
        print(f"Precio: S/{producto['precio']}")
        print(f"Descripción: {producto['descripcion']}")
        print("-" * 30)
else:
    print("No hay productos en la base de datos")

print(f"\nTotal de productos: {len(productos) if productos else 0}")
