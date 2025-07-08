from database import DatabaseManager

db = DatabaseManager()

def mostrar_resumen_base_datos():
    print("📊 RESUMEN COMPLETO DE LA BASE DE DATOS")
    print("=" * 60)
    
    # Contar registros en cada tabla
    tablas = ['clientes', 'productos', 'pedidos', 'pedido_detalle', 'chat_logs']
    
    for tabla in tablas:
        try:
            result = db.execute_query(f"SELECT COUNT(*) as total FROM {tabla}")
            total = result[0]['total'] if result else 0
            print(f"📋 {tabla.capitalize()}: {total} registros")
        except Exception as e:
            print(f"❌ Error consultando {tabla}: {e}")
    
    print("\n" + "=" * 60)
    
    # Mostrar últimos 3 pedidos
    print("🛒 ÚLTIMOS 3 PEDIDOS:")
    query_pedidos = """
        SELECT p.id, p.total, p.estado, p.fecha, c.nombre, c.telefono 
        FROM pedidos p 
        JOIN clientes c ON p.cliente_id = c.id 
        ORDER BY p.fecha DESC 
        LIMIT 3
    """
    pedidos = db.execute_query(query_pedidos)
    
    if pedidos:
        for pedido in pedidos:
            print(f"\n📝 Pedido #{pedido['id']}")
            print(f"   👤 Cliente: {pedido['nombre']} ({pedido['telefono']})")
            print(f"   📅 Fecha: {pedido['fecha']}")
            print(f"   💰 Total: S/{pedido['total']:.2f}")
            print(f"   📊 Estado: {pedido['estado']}")
            
            # Mostrar detalles de este pedido
            query_detalles = """
                SELECT pd.cantidad, pd.precio_unitario, pr.nombre 
                FROM pedido_detalle pd 
                JOIN productos pr ON pd.producto_id = pr.id 
                WHERE pd.pedido_id = %s
            """
            detalles = db.execute_query(query_detalles, (pedido['id'],))
            
            if detalles:
                print(f"   📦 Productos:")
                for detalle in detalles:
                    subtotal = detalle['cantidad'] * detalle['precio_unitario']
                    print(f"      • {detalle['cantidad']}x {detalle['nombre']} - S/{detalle['precio_unitario']:.2f} c/u = S/{subtotal:.2f}")
    else:
        print("No hay pedidos registrados")
    
    print("\n" + "=" * 60)
    
    # Mostrar productos más vendidos
    print("🏆 TOP 5 PRODUCTOS MÁS VENDIDOS:")
    query_top_productos = """
        SELECT pr.nombre, SUM(pd.cantidad) as total_vendido, 
               COUNT(pd.pedido_id) as veces_pedido
        FROM pedido_detalle pd 
        JOIN productos pr ON pd.producto_id = pr.id 
        GROUP BY pr.id, pr.nombre 
        ORDER BY total_vendido DESC 
        LIMIT 5
    """
    top_productos = db.execute_query(query_top_productos)
    
    if top_productos:
        for i, producto in enumerate(top_productos, 1):
            print(f"   {i}. {producto['nombre']}")
            print(f"      📦 Cantidad vendida: {producto['total_vendido']}")
            print(f"      🔄 Pedidos: {producto['veces_pedido']}")
    else:
        print("No hay ventas registradas")
    
    print("\n" + "=" * 60)
    
    # Verificar logs de chat
    print("💬 ÚLTIMOS 3 LOGS DE CHAT:")
    query_logs = """
        SELECT cl.user_message, cl.intent_detected, cl.response_sent, 
               cl.timestamp, c.nombre, c.telefono
        FROM chat_logs cl 
        JOIN clientes c ON cl.cliente_id = c.id 
        ORDER BY cl.timestamp DESC 
        LIMIT 3
    """
    logs = db.execute_query(query_logs)
    
    if logs:
        for log in logs:
            print(f"\n💬 {log['timestamp']}")
            print(f"   👤 Cliente: {log['nombre']} ({log['telefono']})")
            print(f"   🗨️ Mensaje: {log['user_message']}")
            print(f"   🎯 Intent: {log['intent_detected']}")
            print(f"   🤖 Respuesta: {log['response_sent']}")
    else:
        print("No hay logs de chat registrados")

if __name__ == "__main__":
    try:
        mostrar_resumen_base_datos()
        print(f"\n🎉 BASE DE DATOS FUNCIONANDO CORRECTAMENTE")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
