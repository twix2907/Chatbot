import requests
import json

# URL del webhook local
webhook_url = "http://localhost:5000/webhook"

def test_pedido_real_dialogflow():
    print("🤖 PROBANDO PEDIDO REAL A TRAVÉS DE DIALOGFLOW")
    print("=" * 60)
    
    # Datos que enviaría Dialogflow para un pedido real
    dialogflow_request = {
        "queryResult": {
            "queryText": "Quiero 2 francés, 1 torta de chocolate y 3 empanaditas de pollo",
            "intent": {
                "displayName": "realizar_pedido"
            },
            "parameters": {
                "productos": [
                    {
                        "cantidad": "2",
                        "nombre": "francés"
                    },
                    {
                        "cantidad": "1", 
                        "nombre": "torta de chocolate"
                    },
                    {
                        "cantidad": "3",
                        "nombre": "empanaditas de pollo"
                    }
                ]
            }
        },
        "originalDetectIntentRequest": {
            "source": "whatsapp",
            "payload": {
                "from": "+51987654321"
            }
        }
    }
    
    print("📤 Enviando pedido al webhook...")
    print(f"📱 Cliente: +51987654321")
    print(f"🛒 Productos: 2x francés, 1x torta de chocolate, 3x empanaditas de pollo")
    
    try:
        # Enviar request al webhook
        response = requests.post(
            webhook_url,
            json=dialogflow_request,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"\n📥 RESPUESTA DEL WEBHOOK:")
        print(f"   🔗 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"   ✅ Respuesta exitosa")
            print(f"   🤖 Mensaje: {response_data.get('fulfillmentText', 'Sin mensaje')}")
        else:
            print(f"   ❌ Error en el servidor")
            print(f"   📝 Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al webhook. ¿Está el servidor corriendo?")
        print("💡 Para iniciar el servidor: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_consulta_precios():
    print("\n💰 PROBANDO CONSULTA DE PRECIOS")
    print("=" * 40)
    
    dialogflow_request = {
        "queryResult": {
            "queryText": "¿Cuánto cuesta el francés y la torta de chocolate?",
            "intent": {
                "displayName": "consultar_precios"
            },
            "parameters": {
                "productos": ["francés", "torta de chocolate"]
            }
        },
        "originalDetectIntentRequest": {
            "source": "whatsapp",
            "payload": {
                "from": "+51987654321"
            }
        }
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=dialogflow_request,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📥 Status: {response.status_code}")
        if response.status_code == 200:
            response_data = response.json()
            print(f"🤖 Respuesta: {response_data.get('fulfillmentText', 'Sin mensaje')}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Servidor no disponible")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DEL WEBHOOK CON PRODUCTOS REALES")
    print("=" * 70)
    
    # Probar pedido real
    test_pedido_real_dialogflow()
    
    # Probar consulta de precios
    test_consulta_precios()
    
    print(f"\n✅ PRUEBAS COMPLETADAS")
    print(f"💡 Asegúrate de que el servidor esté corriendo con: python app.py")
