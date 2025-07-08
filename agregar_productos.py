from database import DatabaseManager

db = DatabaseManager()

# Productos de la Panadería Jos & Mar con precios realistas para Chincha, Perú
productos_panaderia = [
    # Pan Salado
    {"nombre": "Ciabatti", "precio": 0.50, "categoria": "Pan Salado", "descripcion": "Pan italiano tradicional con corteza crujiente"},
    {"nombre": "Francés", "precio": 0.30, "categoria": "Pan Salado", "descripcion": "Pan francés clásico, ideal para el desayuno"},
    {"nombre": "Baguette", "precio": 2.50, "categoria": "Pan Salado", "descripcion": "Pan baguette francés de masa madre"},
    
    # Pan Dulce
    {"nombre": "Chancay", "precio": 0.80, "categoria": "Pan Dulce", "descripcion": "Pan dulce tradicional peruano"},
    {"nombre": "Wawas", "precio": 3.50, "categoria": "Pan Dulce", "descripcion": "Pan de muerto tradicional con decoraciones"},
    {"nombre": "Caramanduca", "precio": 1.20, "categoria": "Pan Dulce", "descripcion": "Pan dulce con azúcar y canela"},
    {"nombre": "Panetones", "precio": 25.00, "categoria": "Pan Dulce", "descripcion": "Panetón tradicional navideño con frutas confitadas"},
    
    # Panes Semidulces
    {"nombre": "Yema", "precio": 1.00, "categoria": "Pan Semidulce", "descripcion": "Pan enriquecido con yema de huevo"},
    {"nombre": "Caracol", "precio": 1.50, "categoria": "Pan Semidulce", "descripcion": "Pan en forma de caracol con azúcar"},
    {"nombre": "Integral", "precio": 1.20, "categoria": "Pan Semidulce", "descripcion": "Pan integral nutritivo con fibra"},
    {"nombre": "Camote", "precio": 1.80, "categoria": "Pan Semidulce", "descripcion": "Pan dulce de camote peruano"},
    {"nombre": "Petipanes", "precio": 0.60, "categoria": "Pan Semidulce", "descripcion": "Pequeños panes individuales"},
    
    # Pasteles
    {"nombre": "Torta de chocolate", "precio": 35.00, "categoria": "Pasteles", "descripcion": "Torta de chocolate húmeda con cobertura"},
    {"nombre": "Tres Leches", "precio": 30.00, "categoria": "Pasteles", "descripcion": "Torta tres leches tradicional peruana"},
    {"nombre": "Torta helada", "precio": 40.00, "categoria": "Pasteles", "descripcion": "Torta helada de vainilla y chocolate"},
    {"nombre": "Torta de naranja", "precio": 28.00, "categoria": "Pasteles", "descripcion": "Torta esponjosa con sabor a naranja"},
    {"nombre": "Torta Marmoleado", "precio": 32.00, "categoria": "Pasteles", "descripcion": "Torta marmoleada de vainilla y chocolate"},
    
    # Bocaditos
    {"nombre": "Empanaditas dulces", "precio": 1.50, "categoria": "Bocaditos", "descripcion": "Empanaditas rellenas de manjar blanco"},
    {"nombre": "Empanaditas de pollo", "precio": 2.00, "categoria": "Bocaditos", "descripcion": "Empanaditas rellenas de pollo guisado"},
    {"nombre": "Empanaditas de carne", "precio": 2.50, "categoria": "Bocaditos", "descripcion": "Empanaditas rellenas de carne molida"},
    {"nombre": "Enrolladitos de queso", "precio": 2.20, "categoria": "Bocaditos", "descripcion": "Enrollados de masa con queso derretido"},
    {"nombre": "Enrolladitos de hot dog", "precio": 2.80, "categoria": "Bocaditos", "descripcion": "Enrollados con salchicha hot dog"},
    {"nombre": "Pionono", "precio": 4.50, "categoria": "Bocaditos", "descripcion": "Pionono relleno de manjar y frutas"}
]

def agregar_productos():
    print("🥖 AGREGANDO PRODUCTOS DE LA PANADERÍA JOS & MAR")
    print("=" * 60)
    
    productos_agregados = 0
    productos_actualizados = 0
    
    for producto in productos_panaderia:
        # Verificar si el producto ya existe
        query_buscar = "SELECT id, precio FROM productos WHERE nombre = %s"
        resultado = db.execute_query(query_buscar, (producto["nombre"],))
        
        if resultado:
            # Producto existe, actualizar precio y descripción
            query_actualizar = """
                UPDATE productos 
                SET precio = %s, descripcion = %s, stock = 50
                WHERE nombre = %s
            """
            db.execute_query(query_actualizar, (
                producto["precio"], 
                producto["descripcion"], 
                producto["nombre"]
            ))
            productos_actualizados += 1
            print(f"✅ Actualizado: {producto['nombre']} - S/{producto['precio']:.2f}")
        else:
            # Producto no existe, insertarlo
            query_insertar = """
                INSERT INTO productos (nombre, precio, descripcion, stock) 
                VALUES (%s, %s, %s, %s)
            """
            db.execute_insert(query_insertar, (
                producto["nombre"],
                producto["precio"],
                producto["descripcion"],
                50  # Stock inicial
            ))
            productos_agregados += 1
            print(f"🆕 Agregado: {producto['nombre']} - S/{producto['precio']:.2f}")
    
    print("=" * 60)
    print(f"📊 RESUMEN:")
    print(f"   • Productos nuevos agregados: {productos_agregados}")
    print(f"   • Productos actualizados: {productos_actualizados}")
    print(f"   • Total procesados: {len(productos_panaderia)}")
    
    # Mostrar resumen por categoría
    print(f"\n📋 PRODUCTOS POR CATEGORÍA:")
    categorias = {}
    for producto in productos_panaderia:
        categoria = producto["categoria"]
        if categoria not in categorias:
            categorias[categoria] = []
        categorias[categoria].append(f"{producto['nombre']} (S/{producto['precio']:.2f})")
    
    for categoria, items in categorias.items():
        print(f"\n🏷️ {categoria}:")
        for item in items:
            print(f"   • {item}")

if __name__ == "__main__":
    try:
        agregar_productos()
        print(f"\n✅ ¡Todos los productos han sido agregados exitosamente!")
        print(f"🎉 La Panadería Jos & Mar ya tiene su catálogo completo en la base de datos.")
    except Exception as e:
        print(f"❌ Error al agregar productos: {e}")
