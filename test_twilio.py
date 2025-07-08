#!/usr/bin/env python3
"""
Script para probar el webhook con mensajes simulados de Twilio WhatsApp
"""
import requests

def test_twilio_webhook(base_url="http://localhost:5000"):
    """Prueba el webhook con diferentes mensajes de Twilio"""
    
    print("🧪 PROBANDO WEBHOOK CON MENSAJES DE TWILIO WHATSAPP")
    print("=" * 60)
    
    # Mensajes de prueba simulando Twilio
    test_messages = [
        {
            "nombre": "Saludo",
            "body": "Hola",
            "expected": "Bienvenido a la Panadería Jos & Mar"
        },
        {
            "nombre": "Consultar productos", 
            "body": "¿Qué productos tienen?",
            "expected": "PRODUCTOS DISPONIBLES"
        },
        {
            "nombre": "Hacer pedido",
            "body": "Quiero 2 francés y 1 torta de chocolate",
            "expected": "Pedido #"
        },
        {
            "nombre": "Consultar precio",
            "body": "¿Cuánto cuesta el francés?",
            "expected": "PRECIOS"
        },
        {
            "nombre": "Despedida",
            "body": "Gracias, adiós",
            "expected": "Gracias por contactar"
        }
    ]
    
    telefono_test = "+51999888777"
    
    for i, test in enumerate(test_messages, 1):
        print(f"\n{i}️⃣ PROBANDO: {test['nombre']}")
        print(f"   📱 Mensaje: '{test['body']}'")
        
        # Datos que enviaría Twilio
        twilio_data = {
            'Body': test['body'],
            'From': f'whatsapp:{telefono_test}',
            'To': 'whatsapp:+14155238886',
            'MessageSid': f'SM{i}234567890abcdef',
            'AccountSid': 'AC1234567890abcdef',
            'ApiVersion': '2010-04-01'
        }
        
        try:
            # Simular request de Twilio
            response = requests.post(
                f"{base_url}/webhook",
                data=twilio_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=10
            )
            
            if response.status_code == 200:
                # Extraer texto de respuesta TwiML
                response_text = response.text
                if test['expected'] in response_text:
                    print(f"   ✅ Respuesta correcta")
                    # Extraer el mensaje del XML
                    import re
                    match = re.search(r'<Message>(.*?)</Message>', response_text, re.DOTALL)
                    if match:
                        mensaje = match.group(1).strip()
                        print(f"   🤖 Bot: {mensaje[:100]}..." if len(mensaje) > 100 else f"   🤖 Bot: {mensaje}")
                else:
                    print(f"   ⚠️ Respuesta inesperada")
                    print(f"   📝 Respuesta: {response_text[:200]}...")
                    
            else:
                print(f"   ❌ Error HTTP {response.status_code}")
                print(f"   📝 Error: {response.text[:100]}...")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ No se pudo conectar al servidor")
            print(f"   💡 ¿Está corriendo python app.py?")
            break
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🎯 PRUEBAS COMPLETADAS")
    print(f"💡 Si todo funcionó, tu webhook está listo para Twilio!")

def test_health_check(base_url="http://localhost:5000"):
    """Prueba el endpoint de salud"""
    print(f"\n🏥 PROBANDO HEALTH CHECK")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data.get('status', 'N/A')}")
            print(f"💾 Base de datos: {data.get('database', 'N/A')}")
        else:
            print(f"❌ Health check falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en health check: {e}")

if __name__ == "__main__":
    print("🚀 TESTER PARA TWILIO WHATSAPP")
    print("=" * 70)
    
    # Probar health check primero
    test_health_check()
    
    # Probar webhook con mensajes
    test_twilio_webhook()
    
    print(f"\n🔗 PRÓXIMO PASO:")
    print(f"1. Subir código a GitHub")
    print(f"2. Desplegar en Railway") 
    print(f"3. Configurar Twilio con URL de Railway")
    print(f"4. ¡Probar desde WhatsApp real!")
