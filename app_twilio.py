import os
from flask import Flask, request, jsonify
from database import DatabaseManager
from dotenv import load_dotenv
from datetime import datetime
import re

load_dotenv()

app = Flask(__name__)
db = DatabaseManager()

# Configuración para Railway
port = int(os.getenv('PORT', 5000))

# ============================================
# ENDPOINTS DE SALUD Y VERIFICACIÓN
# ============================================

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de salud para Railway"""
    try:
        # Verificar conexión a la base de datos
        db.execute_query("SELECT 1")
        
        return jsonify({
            'status': 'healthy',
            'message': 'Panadería Jos & Mar Chatbot funcionando correctamente',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': 'Error en el sistema',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/webhook', methods=['GET'])
def webhook_verification():
    """Verificación de webhook para WhatsApp"""
    verify_token = os.getenv('WEBHOOK_VERIFY_TOKEN', 'panaderia_jos_mar_2025')
    
    # Verificar token de WhatsApp
    if request.args.get('hub.verify_token') == verify_token:
        return request.args.get('hub.challenge')
    
    return 'Token de verificación incorrecto', 403

@app.route('/info', methods=['GET'])
def info():
    """Información del sistema"""
    return jsonify({
        'name': 'Panadería Jos & Mar Chatbot',
        'version': '1.0.0',
        'description': 'Chatbot para pedidos de la Panadería Jos & Mar',
        'endpoints': {
            'webhook': '/webhook (POST)',
            'health': '/health (GET)',
            'info': '/info (GET)',
            'test': '/test (GET)'
        },
        'whatsapp_ready': True,
        'database_ready': True,
        'twilio_ready': True
    })

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Endpoint de prueba"""
    return jsonify({
        'message': '¡Hola desde la Panadería Jos & Mar!',
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })

# ============================================
# FUNCIONES PARA PROCESAR MENSAJES
# ============================================

def extraer_parametros_dialogflow(req):
    """Extrae parámetros y datos del request de Dialogflow"""
    query_result = req.get('queryResult', {})
    
    return {
        'intent': query_result.get('intent', {}).get('displayName', ''),
        'parametros': query_result.get('parameters', {}),
        'mensaje_usuario': query_result.get('queryText', ''),
        'telefono_whatsapp': req.get('originalDetectIntentRequest', {})
                              .get('payload', {})
                              .get('from', ''),
        'fuente': req.get('originalDetectIntentRequest', {}).get('source', '')
    }

def procesar_mensaje_twilio(mensaje_texto):
    """Procesa un mensaje de texto y determina el intent basado en palabras clave"""
    mensaje = mensaje_texto.lower().strip()
    
    # Detectar intents por palabras clave
    if any(word in mensaje for word in ['hola', 'buenos días', 'buenas tardes', 'hey', 'hi']):
        return 'saludo'
    
    elif any(word in mensaje for word in ['productos', 'que tienen', 'catálogo', 'menu', 'carta']):
        return 'consultar_productos'
    
    elif any(word in mensaje for word in ['precio', 'cuesta', 'cuánto', 'cost']):
        return 'consultar_precios'
    
    elif any(word in mensaje for word in ['pedido', 'pedidos', 'historial', 'anteriores']):
        return 'consultar_pedidos'
    
    elif any(word in mensaje for word in ['quiero', 'deseo', 'necesito', 'pedir', 'order']):
        return 'realizar_pedido'
    
    elif any(word in mensaje for word in ['gracias', 'adiós', 'bye', 'chau']):
        return 'despedida'
    
    else:
        return 'intent_no_reconocido'

def extraer_productos_del_texto(texto):
    """Extrae productos y cantidades de un texto libre"""
    # Patrones para encontrar cantidad + producto
    patrones = [
        r'(\d+)\s*x?\s*([a-záéíóúñ\s]+?)(?=\s*[,y]|\s*$)',
        r'(\d+)\s+([a-záéíóúñ\s]+?)(?=\s*[,y]|\s*$)',
    ]
    
    productos = []
    texto_lower = texto.lower()
    
    for patron in patrones:
        matches = re.findall(patron, texto_lower, re.IGNORECASE)
        for match in matches:
            cantidad = int(match[0])
            nombre = match[1].strip()
            
            # Limpiar el nombre del producto
            nombre = re.sub(r'\b(de|del|la|el|un|una)\b', '', nombre).strip()
            
            if len(nombre) > 2:  # Evitar nombres muy cortos
                productos.append({
                    'cantidad': str(cantidad),
                    'nombre': nombre
                })
    
    return productos

def guardar_log_conversacion(telefono, mensaje, intent, respuesta):
    """Guarda el log de la conversación en la base de datos"""
    try:
        # Buscar cliente por teléfono
        cliente_query = "SELECT id FROM clientes WHERE telefono = %s"
        cliente_result = db.execute_query(cliente_query, (telefono,))
        
        if cliente_result:
            cliente_id = cliente_result[0]['id']
            
            # Guardar log
            log_query = """
                INSERT INTO chat_logs (cliente_id, user_message, intent_detected, response_sent) 
                VALUES (%s, %s, %s, %s)
            """
            db.execute_insert(log_query, (cliente_id, mensaje, intent, respuesta))
            print(f"[LOG] Conversación guardada para cliente {cliente_id}")
        else:
            print(f"[WARNING] Cliente no encontrado para teléfono: {telefono}")
    except Exception as e:
        print(f"[ERROR] Error guardando log: {e}")

def obtener_o_crear_cliente(telefono):
    """Obtiene el ID del cliente o crea uno temporal"""
    if not telefono:
        return None
    
    # Buscar cliente existente
    cliente_query = "SELECT id FROM clientes WHERE telefono = %s"
    cliente_result = db.execute_query(cliente_query, (telefono,))
    
    if cliente_result:
        return cliente_result[0]['id']
    else:
        # Crear cliente temporal con solo el teléfono
        try:
            cliente_id = db.execute_insert(
                "INSERT INTO clientes (nombre, telefono) VALUES (%s, %s)",
                (f"Cliente_{telefono[-4:]}", telefono)
            )
            return cliente_id
        except:
            return None

# ============================================
# MANEJADORES DE INTENTS
# ============================================

def manejar_saludo(datos):
    """Maneja intents de saludo"""
    telefono = datos['telefono_whatsapp']
    respuesta = "🥖 ¡Hola! Bienvenido a la Panadería Jos & Mar. Soy tu asistente virtual.\n\n"
    respuesta += "Puedo ayudarte con:\n"
    respuesta += "🛒 Realizar pedidos\n"
    respuesta += "📋 Consultar productos y precios\n"
    respuesta += "📞 Ver tus pedidos anteriores\n\n"
    respuesta += "¿En qué puedo ayudarte hoy?"
    
    guardar_log_conversacion(telefono, datos['mensaje_usuario'], 'saludo', respuesta)
    return respuesta

def manejar_consultar_productos(datos):
    """Maneja consultas de productos disponibles"""
    telefono = datos['telefono_whatsapp']
    
    try:
        # Obtener productos disponibles
        productos_query = """
            SELECT nombre, precio, descripcion 
            FROM productos 
            WHERE precio > 0 AND stock > 0
            ORDER BY nombre
        """
        productos = db.execute_query(productos_query)
        
        if productos:
            respuesta = "🥖 *PRODUCTOS DISPONIBLES - PANADERÍA JOS & MAR*\n\n"
            
            # Agrupar por tipo de producto
            panes = []
            pasteles = []
            bocaditos = []
            otros = []
            
            for producto in productos:
                nombre = producto['nombre']
                precio = float(producto['precio'])
                
                if any(word in nombre.lower() for word in ['francés', 'ciabatti', 'baguette', 'pan']):
                    panes.append(f"• {nombre} - S/{precio:.2f}")
                elif any(word in nombre.lower() for word in ['torta', 'tres leches', 'panetón']):
                    pasteles.append(f"• {nombre} - S/{precio:.2f}")
                elif any(word in nombre.lower() for word in ['empanadita', 'enrolladito', 'pionono']):
                    bocaditos.append(f"• {nombre} - S/{precio:.2f}")
                else:
                    otros.append(f"• {nombre} - S/{precio:.2f}")
            
            if panes:
                respuesta += "🍞 *PANES:*\n" + "\n".join(panes) + "\n\n"
            if pasteles:
                respuesta += "🎂 *PASTELES:*\n" + "\n".join(pasteles) + "\n\n"
            if bocaditos:
                respuesta += "🥐 *BOCADITOS:*\n" + "\n".join(bocaditos) + "\n\n"
            if otros:
                respuesta += "🍰 *OTROS:*\n" + "\n".join(otros) + "\n\n"
            
            respuesta += "Para hacer un pedido, solo dime qué productos y cantidades quieres. ¡Ejemplo: 'Quiero 2 francés y 1 torta de chocolate'!"
        else:
            respuesta = "En este momento no tenemos productos disponibles. Te contactaremos cuando tengamos nuevos productos."
        
        guardar_log_conversacion(telefono, datos['mensaje_usuario'], 'consultar_productos', respuesta)
        return respuesta
        
    except Exception as e:
        print(f"Error consultando productos: {e}")
        respuesta = "Disculpa, hubo un error consultando los productos. Por favor intenta nuevamente."
        guardar_log_conversacion(telefono, datos['mensaje_usuario'], 'consultar_productos', respuesta)
        return respuesta

def manejar_realizar_pedido(datos):
    """Maneja la creación de pedidos"""
    parametros = datos['parametros']
    telefono = datos['telefono_whatsapp']
    
    try:
        # Obtener o crear cliente
        cliente_id = obtener_o_crear_cliente(telefono)
        if not cliente_id:
            return "Para hacer pedidos necesitas estar registrado. ¿Cuál es tu nombre?"
        
        # Extraer productos del parámetro
        productos_param = parametros.get('productos', [])
        if not productos_param:
            return "No pude identificar los productos que quieres. Por favor especifica qué productos y cantidades deseas."
        
        # Procesar productos
        productos_validos = []
        total_pedido = 0
        
        for item in productos_param:
            if isinstance(item, dict):
                cantidad = int(item.get('cantidad', 1))
                nombre_producto = item.get('nombre', '').strip()
            else:
                # Si es string, intentar extraer
                cantidad = 1
                nombre_producto = str(item).strip()
            
            if not nombre_producto:
                continue
                
            # Buscar producto en base de datos (búsqueda flexible)
            producto_query = """
                SELECT id, nombre, precio FROM productos 
                WHERE LOWER(nombre) LIKE LOWER(%s) 
                LIMIT 1
            """
            producto_result = db.execute_query(producto_query, (f"%{nombre_producto}%",))
            
            if producto_result:
                producto = producto_result[0]
                precio = float(producto['precio'])
                subtotal = precio * cantidad
                
                productos_validos.append({
                    'id': producto['id'],
                    'nombre': producto['nombre'],
                    'cantidad': cantidad,
                    'precio': precio,
                    'subtotal': subtotal
                })
                
                total_pedido += subtotal
        
        if not productos_validos:
            return "No pude encontrar los productos que mencionaste. ¿Podrías especificar mejor?"
        
        # Crear pedido
        pedido_id = db.execute_insert(
            "INSERT INTO pedidos (cliente_id, total, estado) VALUES (%s, %s, %s)",
            (cliente_id, total_pedido, "pendiente")
        )
        
        # Agregar detalles del pedido
        for producto in productos_validos:
            db.execute_insert(
                "INSERT INTO pedido_detalle (pedido_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                (pedido_id, producto['id'], producto['cantidad'], producto['precio'])
            )
        
        # Generar respuesta
        respuesta = f"✅ ¡Pedido #{pedido_id} registrado exitosamente!\n\n"
        respuesta += "📋 Resumen de tu pedido:\n"
        
        for producto in productos_validos:
            respuesta += f"• {producto['cantidad']}x {producto['nombre']} - S/{producto['precio']:.2f} c/u = S/{producto['subtotal']:.2f}\n"
        
        respuesta += f"\n💰 Total: S/{total_pedido:.2f}"
        respuesta += "\n\n📞 Te contactaremos pronto para confirmar tu pedido y coordinar la entrega."
        
        guardar_log_conversacion(telefono, datos['mensaje_usuario'], 'realizar_pedido', respuesta)
        return respuesta
        
    except Exception as e:
        print(f"Error procesando pedido: {e}")
        respuesta = "Disculpa, hubo un error procesando tu pedido. Por favor intenta nuevamente."
        guardar_log_conversacion(telefono, datos['mensaje_usuario'], 'realizar_pedido', respuesta)
        return respuesta

def manejar_consultar_precios(datos):
    """Maneja consultas de precios específicos"""
    telefono = datos['telefono_whatsapp']
    
    # Para Twilio, extraer productos del mensaje
    if datos.get('fuente') == 'twilio':
        productos_extraidos = extraer_productos_del_texto(datos['mensaje_usuario'])
        if productos_extraidos:
            productos_consultados = [p['nombre'] for p in productos_extraidos]
        else:
            # Buscar nombres de productos en el mensaje
            mensaje = datos['mensaje_usuario'].lower()
            productos_conocidos = ['francés', 'torta de chocolate', 'empanaditas', 'ciabatti', 'baguette']
            productos_consultados = [p for p in productos_conocidos if p in mensaje]
    else:
        productos_consultados = datos['parametros'].get('productos', [])
    
    if not productos_consultados:
        return "¿De qué productos te gustaría conocer el precio?"
    
    try:
        respuesta = "💰 *PRECIOS - PANADERÍA JOS & MAR*\n\n"
        productos_encontrados = 0
        
        for nombre_producto in productos_consultados:
            if isinstance(nombre_producto, dict):
                nombre_producto = nombre_producto.get('nombre', '')
            
            nombre_producto = str(nombre_producto).strip()
            
            # Buscar producto
            producto_query = """
                SELECT nombre, precio FROM productos 
                WHERE LOWER(nombre) LIKE LOWER(%s) AND precio > 0
                LIMIT 1
            """
            resultado = db.execute_query(producto_query, (f"%{nombre_producto}%",))
            
            if resultado:
                producto = resultado[0]
                precio = float(producto['precio'])
                respuesta += f"• {producto['nombre']}: S/{precio:.2f}\n"
                productos_encontrados += 1
            else:
                respuesta += f"• {nombre_producto}: No disponible actualmente\n"
        
        if productos_encontrados == 0:
            respuesta += "\nNo encontré precios para los productos consultados. "
            respuesta += "¿Te gustaría ver todos nuestros productos disponibles?"
        else:
            respuesta += "\n¿Te gustaría hacer un pedido?"
        
        guardar_log_conversacion(telefono, datos['mensaje_usuario'], 'consultar_precios', respuesta)
        return respuesta
        
    except Exception as e:
        print(f"Error consultando precios: {e}")
        respuesta = "Disculpa, hubo un error consultando los precios."
        guardar_log_conversacion(telefono, datos['mensaje_usuario'], 'consultar_precios', respuesta)
        return respuesta

def manejar_consultar_pedidos(datos):
    """Maneja consultas de pedidos anteriores"""
    telefono = datos['telefono_whatsapp']
    
    try:
        # Buscar cliente
        cliente_query = "SELECT id, nombre FROM clientes WHERE telefono = %s"
        cliente_result = db.execute_query(cliente_query, (telefono,))
        
        if not cliente_result:
            return "No encontré tu registro. ¿Te gustaría registrarte primero?"
        
        cliente = cliente_result[0]
        cliente_id = cliente['id']
        
        # Buscar pedidos del cliente
        pedidos_query = """
            SELECT id, fecha, total, estado 
            FROM pedidos 
            WHERE cliente_id = %s 
            ORDER BY fecha DESC 
            LIMIT 3
        """
        pedidos = db.execute_query(pedidos_query, (cliente_id,))
        
        if not pedidos:
            respuesta = f"Hola {cliente['nombre']}, aún no tienes pedidos registrados. ¿Te gustaría hacer tu primer pedido?"
        else:
            respuesta = f"📋 *TUS ÚLTIMOS PEDIDOS, {cliente['nombre'].upper()}:*\n\n"
            
            for pedido in pedidos:
                respuesta += f"🧾 *Pedido #{pedido['id']}*\n"
                respuesta += f"📅 Fecha: {pedido['fecha']}\n"
                respuesta += f"💰 Total: S/{float(pedido['total']):.2f}\n"
                respuesta += f"📊 Estado: {pedido['estado']}\n\n"
            
            respuesta += "¿Te gustaría hacer un nuevo pedido?"
        
        guardar_log_conversacion(telefono, datos['mensaje_usuario'], 'consultar_pedidos', respuesta)
        return respuesta
        
    except Exception as e:
        print(f"Error consultando pedidos: {e}")
        respuesta = "Disculpa, hubo un error consultando tus pedidos."
        guardar_log_conversacion(telefono, datos['mensaje_usuario'], 'consultar_pedidos', respuesta)
        return respuesta

# ============================================
# WEBHOOK PRINCIPAL
# ============================================

@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint principal del webhook para Dialogflow/WhatsApp/Twilio"""
    try:
        # Detectar el tipo de request por Content-Type
        content_type = request.headers.get('Content-Type', '')
        print(f"[INFO] Content-Type: {content_type}")
        
        if 'application/x-www-form-urlencoded' in content_type:
            # Es un request de Twilio WhatsApp
            print("[INFO] Request de Twilio WhatsApp detectado")
            
            mensaje_texto = request.form.get('Body', '')
            telefono = request.form.get('From', '').replace('whatsapp:', '')
            
            print(f"[INFO] Mensaje: {mensaje_texto}")
            print(f"[INFO] Teléfono: {telefono}")
            
            # Detectar intent basado en el texto
            intent = procesar_mensaje_twilio(mensaje_texto)
            print(f"[INFO] Intent detectado: {intent}")
            
            # Crear datos simulando estructura de Dialogflow
            datos = {
                'intent': intent,
                'parametros': {},
                'mensaje_usuario': mensaje_texto,
                'telefono_whatsapp': telefono,
                'fuente': 'twilio'
            }
            
            # Si es un pedido, extraer productos del texto
            if intent == 'realizar_pedido':
                productos_extraidos = extraer_productos_del_texto(mensaje_texto)
                datos['parametros']['productos'] = productos_extraidos
                print(f"[INFO] Productos extraídos: {productos_extraidos}")
            
            # Procesar el intent
            respuesta = procesar_intent(intent, datos)
            print(f"[INFO] Respuesta: {respuesta[:100]}...")
            
            # Respuesta en formato TwiML para Twilio
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{respuesta}</Message>
</Response>""", 200, {'Content-Type': 'application/xml'}
        
        else:
            # Es un request JSON de Dialogflow
            print("[INFO] Request de Dialogflow detectado")
            req = request.get_json()
            print(f"[INFO] Request JSON: {req}")
            
            # Extraer datos del request
            datos = extraer_parametros_dialogflow(req)
            intent = datos['intent']
            telefono = datos['telefono_whatsapp']
            mensaje = datos['mensaje_usuario']
            
            print(f"[INFO] Intent: {intent}")
            print(f"[INFO] Teléfono: {telefono}")
            print(f"[INFO] Mensaje: {mensaje}")
            
            # Procesar el intent
            respuesta = procesar_intent(intent, datos)
            print(f"[INFO] Respuesta: {respuesta[:100]}...")
            
            # Respuesta para Dialogflow
            return jsonify({
                'fulfillmentText': respuesta,
                'fulfillmentMessages': [
                    {
                        'text': {
                            'text': [respuesta]
                        }
                    }
                ]
            })
        
    except Exception as e:
        print(f"[ERROR] Error en webhook: {e}")
        import traceback
        traceback.print_exc()
        
        # Respuesta de error según el tipo de request
        content_type = request.headers.get('Content-Type', '')
        if 'application/x-www-form-urlencoded' in content_type:
            # Error para Twilio
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Disculpa, hubo un error. Por favor intenta nuevamente.</Message>
</Response>""", 500, {'Content-Type': 'application/xml'}
        else:
            # Error para Dialogflow
            return jsonify({
                'fulfillmentText': 'Disculpa, hubo un error procesando tu solicitud.',
                'fulfillmentMessages': [
                    {
                        'text': {
                            'text': ['Disculpa, hubo un error procesando tu solicitud.']
                        }
                    }
                ]
            }), 500

def procesar_intent(intent, datos):
    """Procesa un intent y devuelve la respuesta correspondiente"""
    telefono = datos['telefono_whatsapp']
    mensaje = datos['mensaje_usuario']
    
    # Manejar diferentes intents
    if intent in ['saludo', 'bienvenida', 'hola']:
        return manejar_saludo(datos)
    
    elif intent == 'realizar_pedido':
        return manejar_realizar_pedido(datos)
    
    elif intent == 'consultar_productos':
        return manejar_consultar_productos(datos)
    
    elif intent == 'consultar_precios':
        return manejar_consultar_precios(datos)
    
    elif intent == 'consultar_pedidos':
        return manejar_consultar_pedidos(datos)
    
    elif intent in ['despedida', 'adios']:
        respuesta = "¡Gracias por contactar a la Panadería Jos & Mar! 🥖 Que tengas un excelente día."
        guardar_log_conversacion(telefono, mensaje, intent, respuesta)
        return respuesta
    
    else:
        respuesta = "Hola! Puedo ayudarte con:\n• Ver productos (escribe 'productos')\n• Hacer pedidos (ej: 'quiero 2 francés')\n• Ver precios (ej: '¿cuánto cuesta el francés?')\n• Ver tus pedidos anteriores (escribe 'pedidos')"
        guardar_log_conversacion(telefono, mensaje, 'intent_no_reconocido', respuesta)
        return respuesta

if __name__ == '__main__':
    # Configuración para Railway
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f"🚀 Iniciando Panadería Jos & Mar Chatbot en puerto {port}")
    print(f"🔧 Debug mode: {debug_mode}")
    print(f"🌐 Health check: http://localhost:{port}/health")
    print(f"📱 Soporte: Dialogflow + Twilio WhatsApp")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
