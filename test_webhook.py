import requests
import json

# URL del webhook local
webhook_url = "http://localhost:5000/webhook"

def test_saludo():
    """Prueba el intent de saludo"""
    payload = {
        "queryResult": {
            "intent": {
                "displayName": "Saludo"
            },
            "queryText": "Hola",
            "parameters": {}
        }
    }
    
    response = requests.post(webhook_url, json=payload)
    print("=== TEST SALUDO ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_registro_cliente():
    """Prueba el registro de cliente"""
    payload = {
        "queryResult": {
            "intent": {
                "displayName": "consulta_nombre_cliente"
            },
            "queryText": "Me llamo Juan",
            "parameters": {
                "nombre": "Juan"
            }
        },
        "originalDetectIntentRequest": {
            "payload": {
                "From": "whatsapp:+51987654321"
            }
        }
    }
    
    response = requests.post(webhook_url, json=payload)
    print("=== TEST REGISTRO CLIENTE ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_realizar_pedido():
    """Prueba realizar un pedido"""
    payload = {
        "queryResult": {
            "intent": {
                "displayName": "RealizarPedido"
            },
            "queryText": "Quiero 2 panes francés y 1 torta de chocolate",
            "parameters": {
                "producto": ["pan francés", "torta de chocolate"],
                "cantidad": [2, 1]
            }
        },
        "originalDetectIntentRequest": {
            "payload": {
                "From": "whatsapp:+51987654321"
            }
        }
    }
    
    response = requests.post(webhook_url, json=payload)
    print("=== TEST REALIZAR PEDIDO ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_consultar_productos():
    """Prueba consultar productos"""
    payload = {
        "queryResult": {
            "intent": {
                "displayName": "ConsultarProductos"
            },
            "queryText": "¿Qué productos tienen?",
            "parameters": {}
        }
    }
    
    response = requests.post(webhook_url, json=payload)
    print("=== TEST CONSULTAR PRODUCTOS ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_consultar_pedidos():
    """Prueba consultar pedidos previos"""
    payload = {
        "queryResult": {
            "intent": {
                "displayName": "ConsultarPedidosPrevios"
            },
            "queryText": "¿Cuáles son mis pedidos?",
            "parameters": {}
        },
        "originalDetectIntentRequest": {
            "payload": {
                "From": "whatsapp:+51987654321"
            }
        }
    }
    
    response = requests.post(webhook_url, json=payload)
    print("=== TEST CONSULTAR PEDIDOS ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

if __name__ == "__main__":
    print("🧪 INICIANDO PRUEBAS DEL WEBHOOK...")
    print("=" * 50)
    
    try:
        # Verificar que el servidor esté corriendo
        health_response = requests.get("http://localhost:5000/health")
        if health_response.status_code == 200:
            print("✅ Servidor funcionando correctamente")
            print()
            
            # Ejecutar pruebas
            test_saludo()
            test_registro_cliente()
            test_realizar_pedido()
            test_consultar_productos()
            test_consultar_pedidos()
            
            print("🎉 TODAS LAS PRUEBAS COMPLETADAS")
        else:
            print("❌ Error: Servidor no responde")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("Asegúrate de que la aplicación Flask esté ejecutándose en http://localhost:5000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
