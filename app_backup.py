import os
from flask import Flask, request, jsonify
from database import DatabaseManager
from dotenv import load_dotenv
from datetime import datetime

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
        'database_ready': True
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
# WEBHOOK PRINCIPAL
# ============================================

def extraer_parametros_dialogflow(req):
    """Extrae parámetros y datos del request de Dialogflow"""
    query_result = req.get('queryResult', {})
    
    return {
        'intent': query_result.get('intent', {}).get('displayName', ''),
        'parametros': query_result.get('parameters', {}),
        'mensaje_usuario': query_result.get('queryText', ''),
        'telefono_whatsapp': extraer_telefono_whatsapp(req)
    }

def extraer_telefono_whatsapp(req):
    """Extrae el número de teléfono del usuario desde WhatsApp"""
    original_request = req.get('originalDetectIntentRequest', {})
    payload = original_request.get('payload', {})
    source = original_request.get('source', '')
    
    telefono = None
    
    print(f"[DEBUG] Source: {source}")
    print(f"[DEBUG] Payload: {payload}")
    
    # Para diferentes fuentes de WhatsApp
    if source == 'whatsapp' or 'whatsapp' in str(payload).lower():
        # Para Twilio WhatsApp
        if 'from' in payload or 'From' in payload:
            telefono = payload.get('from', payload.get('From', ''))
            telefono = telefono.replace('whatsapp:', '').replace('+', '').strip()
        
        # Para Meta WhatsApp Cloud API
        elif 'phone_number_id' in payload:
            contacts = payload.get('contacts', [])
            if contacts:
                telefono = contacts[0].get('wa_id', '')
        
        # Para el JSON de prueba
        elif 'from' in payload:
            telefono = payload['from'].replace('+', '').strip()
    
    # Fallback: usar el from del payload directamente
    if not telefono and 'from' in payload:
        telefono = payload['from'].replace('+', '').strip()
    
    print(f"[DEBUG] Teléfono extraído: {telefono}")
    return telefono or "51987654321"  # Número por defecto para pruebas

def crear_respuesta_dialogflow(mensaje):
    """Crea la respuesta en formato Dialogflow"""
    return {
        'fulfillmentText': mensaje,
        'fulfillmentMessages': [
            {
                'text': {
                    'text': [mensaje]
                }
            }
        ]
    }

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json()
        datos = extraer_parametros_dialogflow(req)
        
        intent = datos['intent']
        parametros = datos['parametros']
        mensaje_usuario = datos['mensaje_usuario']
        telefono = datos['telefono_whatsapp']
        
        respuesta = ""
        
        # Manejar diferentes intents
        if intent == 'consulta_nombre_cliente':
            respuesta = manejar_registro_cliente(parametros, telefono)
        
        elif intent == 'RealizarPedido':
            respuesta = manejar_pedido(parametros, telefono)
        
        elif intent == 'ConsultarPedidosPrevios':
            respuesta = manejar_consulta_pedidos(telefono)
        
        elif intent == 'ConsultarProductos':
            respuesta = manejar_consulta_productos()
        
        elif intent == 'ConsultarPrecios':
            respuesta = manejar_consulta_precios(parametros)
        
        elif intent == 'Saludo':
            respuesta = "¡Hola! Bienvenido a la Panadería Jos & Mar. ¿En qué puedo ayudarte hoy?"
        
        elif intent == 'Despedida':
            respuesta = "¡Gracias por tu preferencia! Que tengas un excelente día."
        
        else:
            respuesta = "Lo siento, no entendí tu solicitud. ¿Podrías reformular tu pregunta?"
        
        # Guardar log de la conversación si tenemos cliente identificado
        cliente_id = obtener_cliente_id_por_telefono(telefono) if telefono else None
        if cliente_id:
            db.log_conversacion(cliente_id, mensaje_usuario, intent, respuesta)
        
        return jsonify(crear_respuesta_dialogflow(respuesta))
    
    except Exception as e:
        print(f"Error en webhook: {e}")
        return jsonify(crear_respuesta_dialogflow("Ocurrió un error. Por favor, intenta nuevamente."))

def manejar_registro_cliente(parametros, telefono):
    """Maneja el registro/consulta de cliente"""
    nombre = parametros.get('nombre', '')
    
    if not nombre:
        return "Por favor, dime tu nombre para registrarte."
    
    cliente_id = db.registrar_cliente(nombre, telefono)
    
    if cliente_id:
        return f"¡Hola {nombre}! Ya estás registrado en nuestro sistema. ¿En qué puedo ayudarte?"
    else:
        return "Hubo un problema al registrarte. Por favor, intenta nuevamente."

def manejar_pedido(parametros, telefono):
    """Maneja la creación de pedidos"""
    productos = parametros.get('producto', [])
    cantidades = parametros.get('cantidad', [])
    
    if not productos:
        return "¿Qué productos te gustaría pedir? Tenemos panes, pasteles, bocaditos y más."
    
    # Asegurar que productos y cantidades sean listas
    if isinstance(productos, str):
        productos = [productos]
    if isinstance(cantidades, (int, float)):
        cantidades = [cantidades]
    elif not cantidades:
        cantidades = [1] * len(productos)
    
    # Obtener o crear cliente
    cliente_id = obtener_o_crear_cliente_temporal(telefono)
    
    if not cliente_id:
        return "Necesito que te registres primero. Por favor, dime tu nombre."
    
    # Crear el pedido
    pedido_id = db.crear_pedido(cliente_id, productos, cantidades, telefono)
    
    if pedido_id:
        # Crear resumen del pedido
        resumen = "¡Pedido registrado exitosamente!\n\nResumen:\n"
        for i, producto in enumerate(productos):
            cantidad = cantidades[i] if i < len(cantidades) else 1
            resumen += f"• {cantidad}x {producto}\n"
        
        resumen += f"\nNúmero de pedido: #{pedido_id}\n"
        resumen += "Te confirmaremos el total y tiempo de entrega pronto."
        
        return resumen
    else:
        return "Hubo un problema al procesar tu pedido. Por favor, intenta nuevamente."

def manejar_consulta_pedidos(telefono):
    """Maneja la consulta de pedidos previos"""
    if not telefono:
        return "Necesito tu número de teléfono para buscar tus pedidos."
    
    pedidos = db.consultar_pedidos_cliente(telefono)
    
    if not pedidos:
        return "No encontré pedidos asociados a tu número. ¿Te gustaría hacer un pedido?"
    
    respuesta = "Tus pedidos recientes:\n\n"
    for pedido in pedidos:
        fecha = pedido['fecha'].strftime("%d/%m/%Y %H:%M")
        respuesta += f"🧾 Pedido #{pedido['id']} - {fecha}\n"
        respuesta += f"Productos: {pedido['productos']}\n"
        respuesta += f"Estado: {pedido['estado']}\n"
        if pedido['total']:
            respuesta += f"Total: S/{pedido['total']:.2f}\n"
        respuesta += "\n"
    
    return respuesta

def manejar_consulta_productos():
    """Maneja la consulta de productos disponibles"""
    return """🥖 **PRODUCTOS DISPONIBLES**

**Pan Salado:**
• Ciabatti
• Francés  
• Baguette

**Pan Dulce:**
• Bizcocho
• Chancay
• Wawas
• Caramanduca
• Panetones

**Panes Semidulces:**
• Yema
• Caracol
• Integral
• Camote
• Petipanes

**Pasteles:**
• Torta de chocolate
• Tres Leches
• Torta helada
• Torta de naranja
• Torta Marmoleado

**Bocaditos:**
• Empanaditas dulces
• Empanaditas de pollo
• Empanaditas de carne
• Enrolladitos de queso
• Enrolladitos de hot dog
• Alfajor
• Pionono

¿Qué te gustaría pedir?"""

def manejar_consulta_precios(parametros):
    """Maneja la consulta de precios específicos"""
    producto = parametros.get('producto', '')
    
    if not producto:
        return "¿De qué producto te gustaría saber el precio?"
    
    # Buscar precio en la base de datos
    query = "SELECT precio FROM productos WHERE nombre LIKE %s"
    resultado = db.execute_query(query, (f"%{producto}%",))
    
    if resultado:
        precio = resultado[0]['precio']
        return f"El precio de {producto} es S/{precio:.2f}"
    else:
        return f"No tengo el precio de {producto} actualizado. Te recomiendo contactar directamente para consultar precios."

def obtener_cliente_id_por_telefono(telefono):
    """Obtiene el ID del cliente por teléfono"""
    if not telefono:
        return None
    
    query = "SELECT id FROM clientes WHERE telefono = %s"
    resultado = db.execute_query(query, (telefono,))
    
    return resultado[0]['id'] if resultado else None

def obtener_o_crear_cliente_temporal(telefono):
    """Obtiene cliente existente o crea uno temporal"""
    if telefono:
        cliente_id = obtener_cliente_id_por_telefono(telefono)
        if cliente_id:
            return cliente_id
        
        # Crear cliente temporal con solo el teléfono
        return db.registrar_cliente(f"Cliente_{telefono[-4:]}", telefono)
    
    return None

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que el servicio está funcionando"""
    return jsonify({'status': 'healthy', 'message': 'Webhook funcionando correctamente'})

@app.route('/webhook', methods=['GET'])
def webhook_verify():
    """Endpoint para verificación de webhook de WhatsApp"""
    # Para Meta WhatsApp Cloud API
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    # Token de verificación (configurable en .env)
    verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN', 'mi_token_secreto_123')
    
    if mode == 'subscribe' and token == verify_token:
        print("[INFO] Webhook verificado correctamente")
        return challenge
    else:
        print(f"[ERROR] Verificación fallida. Mode: {mode}, Token: {token}")
        return 'Forbidden', 403

@app.route('/status', methods=['GET'])
def status():
    """Endpoint para verificar el estado del servidor"""
    try:
        # Probar conexión a base de datos
        productos = db.execute_query("SELECT COUNT(*) as total FROM productos")
        total_productos = productos[0]['total'] if productos else 0
        
        return jsonify({
            'status': 'ok',
            'message': 'Servidor funcionando correctamente',
            'database': 'connected',
            'productos': total_productos,
            'timestamp': str(datetime.now())
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'database': 'disconnected'
        }), 500

@app.route('/test-whatsapp', methods=['POST'])
def test_whatsapp():
    """Endpoint para probar mensajes de WhatsApp directamente"""
    try:
        data = request.get_json()
        mensaje = data.get('mensaje', 'Hola')
        telefono = data.get('telefono', '51987654321')
        
        # Simular request de Dialogflow
        fake_request = {
            'queryResult': {
                'queryText': mensaje,
                'intent': {
                    'displayName': 'Saludo'
                },
                'parameters': {}
            },
            'originalDetectIntentRequest': {
                'source': 'whatsapp',
                'payload': {
                    'from': f'+{telefono}'
                }
            }
        }
        
        # Procesar como webhook normal
        datos = extraer_parametros_dialogflow(fake_request)
        respuesta = "¡Hola! Bienvenido a la Panadería Jos & Mar. ¿En qué puedo ayudarte hoy?"
        
        return jsonify({
            'respuesta': respuesta,
            'telefono_detectado': datos['telefono_whatsapp'],
            'mensaje_recibido': mensaje
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Configuración para Railway
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f"🚀 Iniciando Panadería Jos & Mar Chatbot en puerto {port}")
    print(f"🔧 Debug mode: {debug_mode}")
    print(f"🌐 Health check: http://localhost:{port}/health")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
