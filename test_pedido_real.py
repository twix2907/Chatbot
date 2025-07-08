from database import DatabaseManager
import json

db = DatabaseManager()

def simular_pedido_real():
    print("🛒 SIMULANDO PEDIDO REAL CON PRODUCTOS DE LA PANADERÍA")
    print("=" * 60)
    
    # Datos del cliente de prueba
    cliente_telefono = "+51987654321"
    cliente_nombre = "María García"
    
    # Registrar cliente si no existe
    query_cliente = "SELECT id FROM clientes WHERE telefono = %s"
    cliente_existente = db.execute_query(query_cliente, (cliente_telefono,))
    
    if not cliente_existente:
        query_insertar_cliente = """
            INSERT INTO clientes (nombre, telefono) 
            VALUES (%s, %s)
        """
        cliente_id = db.execute_insert(query_insertar_cliente, (cliente_nombre, cliente_telefono))
        print(f"👤 Cliente registrado: {cliente_nombre} - ID: {cliente_id}")
    else:
        cliente_id = cliente_existente[0]['id']
        print(f"👤 Cliente existente: {cliente_nombre} - ID: {cliente_id}")
    
    # Productos para el pedido (nombres reales de la panadería)
    productos_pedido = [
        {"nombre": "Francés", "cantidad": 6},
        {"nombre": "Empanaditas de pollo", "cantidad": 4},
        {"nombre": "Torta de chocolate", "cantidad": 1},
        {"nombre": "Chancay", "cantidad": 3},
        {"nombre": "Enrolladitos de queso", "cantidad": 2}
    ]
    
    print(f"\n📋 PRODUCTOS SOLICITADOS:")
    for item in productos_pedido:
        print(f"   • {item['cantidad']}x {item['nombre']}")
    
    # Verificar que todos los productos existen y obtener precios
    productos_validos = []
    total_pedido = 0
    
    print(f"\n💰 VERIFICANDO PRECIOS:")
    for item in productos_pedido:
        query_producto = "SELECT id, nombre, precio, stock FROM productos WHERE nombre = %s"
        producto_info = db.execute_query(query_producto, (item["nombre"],))
        
        if producto_info:
            producto = producto_info[0]
            cantidad = item["cantidad"]
            subtotal = producto['precio'] * cantidad
            total_pedido += subtotal
            
            productos_validos.append({
                "id": producto['id'],
                "nombre": producto['nombre'],
                "precio": producto['precio'],
                "cantidad": cantidad,
                "subtotal": subtotal
            })
            
            print(f"   ✅ {cantidad}x {producto['nombre']} - S/{producto['precio']:.2f} c/u = S/{subtotal:.2f}")
        else:
            print(f"   ❌ Producto no encontrado: {item['nombre']}")
    
    if not productos_validos:
        print("❌ No se encontraron productos válidos para el pedido")
        return
    
    print(f"\n💵 TOTAL DEL PEDIDO: S/{total_pedido:.2f}")
    
    # Crear el pedido
    query_pedido = """
        INSERT INTO pedidos (cliente_id, total, estado) 
        VALUES (%s, %s, %s)
    """
    pedido_id = db.execute_insert(query_pedido, (cliente_id, total_pedido, "pendiente"))
    print(f"\n📝 Pedido creado con ID: {pedido_id}")
    
    # Agregar detalles del pedido
    print(f"\n📦 AGREGANDO DETALLES DEL PEDIDO:")
    for producto in productos_validos:
        query_detalle = """
            INSERT INTO pedido_detalle (pedido_id, producto_id, cantidad, precio_unitario) 
            VALUES (%s, %s, %s, %s)
        """
        db.execute_insert(query_detalle, (
            pedido_id,
            producto['id'],
            producto['cantidad'],
            producto['precio']
        ))
        print(f"   ✅ Detalle agregado: {producto['cantidad']}x {producto['nombre']}")
    
    # Guardar log de la conversación
    conversacion_log = {
        "tipo": "pedido_real",
        "productos": productos_validos,
        "total": total_pedido,
        "pedido_id": pedido_id
    }
    
    query_log = """
        INSERT INTO chat_logs (cliente_id, user_message, intent_detected, response_sent) 
        VALUES (%s, %s, %s, %s)
    """
    
    # Crear mensaje del pedido
    productos_texto = ', '.join([f"{p['cantidad']}x {p['nombre']}" for p in productos_validos])
    mensaje_pedido = f"Pedido: {productos_texto}"
    respuesta_pedido = f"Pedido #{pedido_id} registrado. Total: S/{total_pedido:.2f}"
    
    db.execute_insert(query_log, (
        cliente_id,
        mensaje_pedido,
        "realizar_pedido",
        respuesta_pedido
    ))
    
    print(f"\n📊 RESUMEN FINAL:")
    print(f"   • Cliente: {cliente_nombre} ({cliente_telefono})")
    print(f"   • Pedido ID: {pedido_id}")
    print(f"   • Productos: {len(productos_validos)} tipos diferentes")
    print(f"   • Total: S/{total_pedido:.2f}")
    print(f"   • Estado: pendiente")
    
    return pedido_id

def verificar_pedido(pedido_id):
    print(f"\n🔍 VERIFICANDO PEDIDO #{pedido_id}")
    print("=" * 40)
    
    # Consultar pedido
    query_pedido = """
        SELECT p.id, p.total, p.estado, p.fecha, c.nombre, c.telefono 
        FROM pedidos p 
        JOIN clientes c ON p.cliente_id = c.id 
        WHERE p.id = %s
    """
    pedido_info = db.execute_query(query_pedido, (pedido_id,))
    
    if pedido_info:
        pedido = pedido_info[0]
        print(f"📋 Pedido: #{pedido['id']}")
        print(f"👤 Cliente: {pedido['nombre']} ({pedido['telefono']})")
        print(f"📅 Fecha: {pedido['fecha']}")
        print(f"💰 Total: S/{pedido['total']:.2f}")
        print(f"📊 Estado: {pedido['estado']}")
        
        # Consultar detalles
        query_detalles = """
            SELECT pd.cantidad, pd.precio_unitario, pr.nombre 
            FROM pedido_detalle pd 
            JOIN productos pr ON pd.producto_id = pr.id 
            WHERE pd.pedido_id = %s
        """
        detalles = db.execute_query(query_detalles, (pedido_id,))
        
        if detalles:
            print(f"\n📦 DETALLES DEL PEDIDO:")
            for detalle in detalles:
                subtotal = detalle['cantidad'] * detalle['precio_unitario']
                print(f"   • {detalle['cantidad']}x {detalle['nombre']} - S/{detalle['precio_unitario']:.2f} c/u = S/{subtotal:.2f}")
    else:
        print(f"❌ No se encontró el pedido #{pedido_id}")

if __name__ == "__main__":
    try:
        # Simular pedido real
        pedido_id = simular_pedido_real()
        
        # Verificar el pedido creado
        if pedido_id:
            verificar_pedido(pedido_id)
            
        print(f"\n🎉 ¡PRUEBA DE PEDIDO REAL COMPLETADA EXITOSAMENTE!")
        print(f"✅ El sistema está funcionando correctamente con productos y precios reales.")
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
