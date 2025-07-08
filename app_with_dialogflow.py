#!/usr/bin/env python3
"""
Versión mejorada del chatbot con integración completa a Dialogflow
"""
import os
from flask import Flask, request, jsonify
from database import DatabaseManager
from dotenv import load_dotenv
from datetime import datetime
import re

# Importaciones para Dialogflow
try:
    from google.cloud import dialogflow
    DIALOGFLOW_AVAILABLE = True
    print("[INFO] Dialogflow SDK disponible")
except ImportError:
    DIALOGFLOW_AVAILABLE = False
    print("[WARNING] Dialogflow SDK no disponible. Usando procesamiento local.")

load_dotenv()

app = Flask(__name__)
db = DatabaseManager()

# Configuración
port = int(os.getenv('PORT', 5000))
DIALOGFLOW_PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')
USE_DIALOGFLOW = DIALOGFLOW_AVAILABLE and DIALOGFLOW_PROJECT_ID

print(f"[CONFIG] Dialogflow habilitado: {USE_DIALOGFLOW}")

# ============================================
# FUNCIONES DE DIALOGFLOW
# ============================================

def detectar_intent_dialogflow(texto, telefono, idioma='es'):
    """Detecta intent usando Dialogflow"""
    if not USE_DIALOGFLOW:
        return None
    
    try:
        # Crear cliente de Dialogflow
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, telefono)
        
        # Crear input de texto
        text_input = dialogflow.TextInput(text=texto, language_code=idioma)
        query_input = dialogflow.QueryInput(text=text_input)
        
        # Detectar intent
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        
        print(f"[DIALOGFLOW] Intent detectado: {response.query_result.intent.display_name}")
        print(f"[DIALOGFLOW] Confianza: {response.query_result.intent_detection_confidence}")
        
        return {
            'intent': response.query_result.intent.display_name,
            'parametros': dict(response.query_result.parameters),
            'mensaje_usuario': response.query_result.query_text,
            'confianza': response.query_result.intent_detection_confidence,
            'fuente': 'dialogflow'
        }
        
    except Exception as e:
        print(f"[ERROR] Error con Dialogflow: {e}")
        return None

def procesar_mensaje_hibrido(mensaje_texto, telefono):
    """Procesa mensaje usando Dialogflow primero, luego fallback local"""
    
    # Intentar con Dialogflow primero
    if USE_DIALOGFLOW:
        resultado_df = detectar_intent_dialogflow(mensaje_texto, telefono)
        
        if resultado_df and resultado_df['confianza'] > 0.7:
            print(f"[INFO] Usando respuesta de Dialogflow (confianza: {resultado_df['confianza']:.2f})")
            return {
                'intent': resultado_df['intent'],
                'parametros': resultado_df['parametros'],
                'mensaje_usuario': mensaje_texto,
                'telefono_whatsapp': telefono,
                'fuente': 'dialogflow',
                'confianza': resultado_df['confianza']
            }
        else:
            print("[INFO] Confianza baja en Dialogflow, usando procesamiento local")
    
    # Fallback a procesamiento local
    intent_local = procesar_mensaje_local(mensaje_texto)
    datos_locales = {
        'intent': intent_local,
        'parametros': {},
        'mensaje_usuario': mensaje_texto,
        'telefono_whatsapp': telefono,
        'fuente': 'local',
        'confianza': 1.0
    }
    
    # Si es un pedido, extraer productos
    if intent_local == 'realizar_pedido':
        productos_extraidos = extraer_productos_del_texto(mensaje_texto)
        datos_locales['parametros']['productos'] = productos_extraidos
    
    return datos_locales

def procesar_mensaje_local(mensaje_texto):
    """Procesamiento local de mensajes (el código actual)"""
    mensaje = mensaje_texto.lower().strip()
    
    # Detectar intents por palabras clave (código actual)
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
    """Extrae productos y cantidades de un texto libre (mejorado)"""
    # Patrones mejorados para encontrar cantidad + producto
    patrones = [
        r'(\d+)\s*x?\s*([a-záéíóúñ\s]+?)(?=\s*[,y]|\s*$)',
        r'(\d+)\s+([a-záéíóúñ\s]+?)(?=\s*[,y]|\s*$)',
        r'(uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)\s+([a-záéíóúñ\s]+?)(?=\s*[,y]|\s*$)',
    ]
    
    # Diccionario para convertir números en texto
    numeros_texto = {
        'uno': 1, 'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5,
        'seis': 6, 'siete': 7, 'ocho': 8, 'nueve': 9, 'diez': 10
    }
    
    productos = []
    texto_lower = texto.lower()
    
    for patron in patrones:
        matches = re.findall(patron, texto_lower, re.IGNORECASE)
        for match in matches:
            cantidad_str = match[0]
            nombre = match[1].strip()
            
            # Convertir cantidad a número
            if cantidad_str.isdigit():
                cantidad = int(cantidad_str)
            else:
                cantidad = numeros_texto.get(cantidad_str.lower(), 1)
            
            # Limpiar el nombre del producto
            nombre = re.sub(r'\b(de|del|la|el|un|una)\b', '', nombre).strip()
            
            if len(nombre) > 2:  # Evitar nombres muy cortos
                productos.append({
                    'cantidad': str(cantidad),
                    'nombre': nombre
                })
    
    return productos

# ============================================
# WEBHOOK MEJORADO
# ============================================

@app.route('/webhook', methods=['POST'])
def webhook_mejorado():
    """Webhook mejorado con soporte para Dialogflow + Twilio"""
    try:
        content_type = request.headers.get('Content-Type', '')
        print(f"[INFO] Content-Type: {content_type}")
        
        if 'application/x-www-form-urlencoded' in content_type:
            # Request de Twilio WhatsApp
            print("[INFO] Request de Twilio WhatsApp detectado")
            
            mensaje_texto = request.form.get('Body', '')
            telefono = request.form.get('From', '').replace('whatsapp:', '')
            
            print(f"[INFO] Mensaje: {mensaje_texto}")
            print(f"[INFO] Teléfono: {telefono}")
            
            # Procesar con sistema híbrido (Dialogflow + Local)
            datos = procesar_mensaje_hibrido(mensaje_texto, telefono)
            
            print(f"[INFO] Intent final: {datos['intent']}")
            print(f"[INFO] Fuente: {datos['fuente']}")
            print(f"[INFO] Confianza: {datos.get('confianza', 'N/A')}")
            
            # Procesar el intent (usar las funciones existentes)
            respuesta = procesar_intent(datos['intent'], datos)
            print(f"[INFO] Respuesta: {respuesta[:100]}...")
            
            # Respuesta TwiML para Twilio
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{respuesta}</Message>
</Response>""", 200, {'Content-Type': 'application/xml'}
        
        elif 'application/json' in content_type:
            # Request directo de Dialogflow
            print("[INFO] Request directo de Dialogflow detectado")
            req = request.get_json()
            
            # Extraer datos del request de Dialogflow
            query_result = req.get('queryResult', {})
            intent = query_result.get('intent', {}).get('displayName', '')
            parametros = query_result.get('parameters', {})
            mensaje = query_result.get('queryText', '')
            
            # Extraer información de WhatsApp si está disponible
            original_request = req.get('originalDetectIntentRequest', {})
            telefono = original_request.get('payload', {}).get('from', '')
            
            datos = {
                'intent': intent,
                'parametros': parametros,
                'mensaje_usuario': mensaje,
                'telefono_whatsapp': telefono,
                'fuente': 'dialogflow_directo'
            }
            
            print(f"[INFO] Intent de Dialogflow: {intent}")
            print(f"[INFO] Parámetros: {parametros}")
            
            # Procesar intent
            respuesta = procesar_intent(intent, datos)
            
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
        
        else:
            return jsonify({'error': 'Content-Type no soportado'}), 400
    
    except Exception as e:
        print(f"[ERROR] Error en webhook: {e}")
        import traceback
        traceback.print_exc()
        
        # Respuesta de error
        content_type = request.headers.get('Content-Type', '')
        if 'application/x-www-form-urlencoded' in content_type:
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Disculpa, hubo un error. Por favor intenta nuevamente.</Message>
</Response>""", 500, {'Content-Type': 'application/xml'}
        else:
            return jsonify({
                'fulfillmentText': 'Disculpa, hubo un error procesando tu solicitud.'
            }), 500

# ============================================
# ENDPOINTS DE INFORMACIÓN
# ============================================

@app.route('/dialogflow-status', methods=['GET'])
def dialogflow_status():
    """Endpoint para verificar el estado de Dialogflow"""
    return jsonify({
        'dialogflow_available': DIALOGFLOW_AVAILABLE,
        'dialogflow_enabled': USE_DIALOGFLOW,
        'project_id': DIALOGFLOW_PROJECT_ID,
        'fallback_mode': 'local_processing'
    })

# Aquí irían todas las demás funciones (manejar_saludo, manejar_realizar_pedido, etc.)
# Las mantenemos iguales del archivo original

if __name__ == '__main__':
    print(f"🚀 Iniciando Panadería Jos & Mar Chatbot MEJORADO")
    print(f"🤖 Dialogflow: {'✅ Habilitado' if USE_DIALOGFLOW else '❌ Deshabilitado (usando procesamiento local)'}")
    print(f"🔧 Modo híbrido: Dialogflow → Fallback local")
    
    app.run(host='0.0.0.0', port=port, debug=False)
