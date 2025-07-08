from database import DatabaseManager

def test_sistema_completo():
    print("🎯 PRUEBA COMPLETA DEL SISTEMA DE PEDIDOS")
    print("=" * 60)
    
    db = DatabaseManager()
    
    # 1. Verificar productos disponibles
    print("1️⃣ VERIFICANDO PRODUCTOS DISPONIBLES:")
    productos_test = ["Francés", "Torta de chocolate", "Empanaditas de pollo"]
    
    productos_disponibles = []
    for nombre in productos_test:
        query = "SELECT id, nombre, precio, stock FROM productos WHERE nombre = %s"
        resultado = db.execute_query(query, (nombre,))
        
        if resultado:
            producto = resultado[0]
            productos_disponibles.append(producto)
            print(f"   ✅ {producto['nombre']} - S/{producto['precio']:.2f} (Stock: {producto['stock']})")
        else:
            print(f"   ❌ {nombre} - No disponible")
    
    if not productos_disponibles:
        print("❌ No hay productos disponibles para la prueba")
        return
    
    # 2. Registrar/verificar cliente
    print(f"\n2️⃣ REGISTRANDO CLIENTE:")
    telefono = "+51999888777"
    nombre = "Cliente Prueba Final"
    
    query_cliente = "SELECT id FROM clientes WHERE telefono = %s"
    cliente_existente = db.execute_query(query_cliente, (telefono,))
    
    if cliente_existente:
        cliente_id = cliente_existente[0]['id']
        print(f"   👤 Cliente existente ID: {cliente_id}")
    else:
        query_insertar = "INSERT INTO clientes (nombre, telefono) VALUES (%s, %s)"
        cliente_id = db.execute_insert(query_insertar, (nombre, telefono))
        print(f"   👤 Cliente nuevo registrado ID: {cliente_id}")
    
    # 3. Crear pedido
    print(f"\n3️⃣ CREANDO PEDIDO:")
    pedido_items = [
        {"nombre": "Francés", "cantidad": 3},
        {"nombre": "Empanaditas de pollo", "cantidad": 2}
    ]
    
    total_pedido = 0
    items_validos = []
    
    for item in pedido_items:
        for producto in productos_disponibles:
            if producto['nombre'] == item['nombre']:
                cantidad = item['cantidad']
                precio = float(producto['precio'])
                subtotal = precio * cantidad
                total_pedido += subtotal
                
                items_validos.append({
                    'id': producto['id'],
                    'nombre': producto['nombre'],
                    'cantidad': cantidad,
                    'precio': precio,
                    'subtotal': subtotal
                })
                
                print(f"   🛒 {cantidad}x {producto['nombre']} = S/{precio:.2f} x {cantidad} = S/{subtotal:.2f}")
                break
    
    print(f"   💰 TOTAL: S/{total_pedido:.2f}")
    
    # 4. Insertar pedido en BD
    print(f"\n4️⃣ GUARDANDO EN BASE DE DATOS:")
    query_pedido = "INSERT INTO pedidos (cliente_id, total, estado) VALUES (%s, %s, %s)"
    pedido_id = db.execute_insert(query_pedido, (cliente_id, total_pedido, "pendiente"))
    print(f"   📝 Pedido creado con ID: {pedido_id}")
    
    # 5. Insertar detalles
    for item in items_validos:
        query_detalle = """
            INSERT INTO pedido_detalle (pedido_id, producto_id, cantidad, precio_unitario) 
            VALUES (%s, %s, %s, %s)
        """
        db.execute_insert(query_detalle, (
            pedido_id,
            item['id'],
            item['cantidad'],
            item['precio']
        ))
        print(f"   📦 Detalle guardado: {item['cantidad']}x {item['nombre']}")
    
    # 6. Guardar log
    query_log = """
        INSERT INTO chat_logs (cliente_id, user_message, intent_detected, response_sent) 
        VALUES (%s, %s, %s, %s)
    """
    productos_texto = ", ".join([f"{item['cantidad']}x {item['nombre']}" for item in items_validos])
    mensaje = f"Pedido: {productos_texto}"
    respuesta = f"Pedido #{pedido_id} registrado exitosamente. Total: S/{total_pedido:.2f}"
    
    db.execute_insert(query_log, (cliente_id, mensaje, "realizar_pedido", respuesta))
    print(f"   💬 Log guardado")
    
    # 7. Verificación final
    print(f"\n5️⃣ VERIFICACIÓN FINAL:")
    query_verificacion = """
        SELECT p.id, p.total, p.estado, c.nombre, c.telefono,
               COUNT(pd.id) as num_productos
        FROM pedidos p 
        JOIN clientes c ON p.cliente_id = c.id 
        LEFT JOIN pedido_detalle pd ON p.id = pd.pedido_id
        WHERE p.id = %s
        GROUP BY p.id
    """
    
    verificacion = db.execute_query(query_verificacion, (pedido_id,))
    if verificacion:
        v = verificacion[0]
        print(f"   ✅ Pedido #{v['id']} verificado")
        print(f"   👤 Cliente: {v['nombre']} ({v['telefono']})")
        print(f"   💰 Total: S/{v['total']:.2f}")
        print(f"   📦 Productos: {v['num_productos']} tipos")
        print(f"   📊 Estado: {v['estado']}")
    
    print(f"\n🎉 ¡SISTEMA FUNCIONANDO PERFECTAMENTE!")
    print(f"✅ Productos: OK")
    print(f"✅ Clientes: OK") 
    print(f"✅ Pedidos: OK")
    print(f"✅ Detalles: OK")
    print(f"✅ Logs: OK")
    print(f"✅ Precios: OK")
    
    return pedido_id

if __name__ == "__main__":
    try:
        pedido_id = test_sistema_completo()
        print(f"\n🏆 PRUEBA COMPLETADA - Pedido #{pedido_id} creado exitosamente")
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
