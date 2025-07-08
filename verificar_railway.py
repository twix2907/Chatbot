#!/usr/bin/env python3
"""
Script para verificar que el deployment en Railway funciona correctamente
"""
import requests
import time
import json

def verificar_railway_deployment(base_url):
    """Verifica que todos los endpoints funcionen correctamente"""
    print("🔍 VERIFICANDO DEPLOYMENT EN RAILWAY")
    print("=" * 50)
    print(f"🌐 URL base: {base_url}")
    print()
    
    # Lista de endpoints a verificar
    endpoints = [
        {"path": "/health", "method": "GET", "description": "Health check"},
        {"path": "/info", "method": "GET", "description": "Información del sistema"},
        {"path": "/test", "method": "GET", "description": "Endpoint de prueba"},
        {"path": "/webhook", "method": "GET", "params": {"hub.verify_token": "panaderia_jos_mar_2025", "hub.challenge": "test123"}, "description": "Verificación de webhook"}
    ]
    
    resultados = []
    
    for endpoint in endpoints:
        print(f"🔗 Probando {endpoint['path']} - {endpoint['description']}")
        
        try:
            url = base_url + endpoint['path']
            
            if endpoint['method'] == 'GET':
                if 'params' in endpoint:
                    response = requests.get(url, params=endpoint['params'], timeout=10)
                else:
                    response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ Status: {response.status_code}")
                try:
                    data = response.json()
                    if endpoint['path'] == '/health':
                        print(f"   📊 Estado: {data.get('status', 'N/A')}")
                        print(f"   💾 Base de datos: {data.get('database', 'N/A')}")
                    elif endpoint['path'] == '/info':
                        print(f"   📱 WhatsApp ready: {data.get('whatsapp_ready', 'N/A')}")
                        print(f"   💾 Database ready: {data.get('database_ready', 'N/A')}")
                except:
                    print(f"   📝 Respuesta: {response.text[:100]}...")
                
                resultados.append({"endpoint": endpoint['path'], "status": "✅ OK"})
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   📝 Error: {response.text[:100]}...")
                resultados.append({"endpoint": endpoint['path'], "status": f"❌ Error {response.status_code}"})
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ No se pudo conectar")
            resultados.append({"endpoint": endpoint['path'], "status": "❌ Conexión fallida"})
        except Exception as e:
            print(f"   ❌ Error: {e}")
            resultados.append({"endpoint": endpoint['path'], "status": f"❌ {str(e)}"})
        
        print()
        time.sleep(1)
    
    # Probar webhook con un pedido real
    print("🛒 PROBANDO WEBHOOK CON PEDIDO REAL")
    print("-" * 40)
    
    pedido_test = {
        "queryResult": {
            "queryText": "Quiero 2 francés y 1 torta de chocolate",
            "intent": {
                "displayName": "realizar_pedido"
            },
            "parameters": {
                "productos": [
                    {"cantidad": "2", "nombre": "francés"},
                    {"cantidad": "1", "nombre": "torta de chocolate"}
                ]
            }
        },
        "originalDetectIntentRequest": {
            "source": "whatsapp",
            "payload": {"from": "+51999999999"}
        }
    }
    
    try:
        response = requests.post(
            base_url + "/webhook",
            json=pedido_test,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        if response.status_code == 200:
            print("✅ Webhook de pedido: OK")
            data = response.json()
            respuesta_bot = data.get('fulfillmentText', '')
            if 'Pedido #' in respuesta_bot:
                print("✅ Pedido procesado correctamente")
                print(f"📝 Respuesta: {respuesta_bot[:100]}...")
            else:
                print("⚠️ Respuesta inesperada del bot")
            resultados.append({"endpoint": "/webhook (POST)", "status": "✅ OK"})
        else:
            print(f"❌ Webhook error: {response.status_code}")
            resultados.append({"endpoint": "/webhook (POST)", "status": f"❌ Error {response.status_code}"})
    except Exception as e:
        print(f"❌ Error en webhook: {e}")
        resultados.append({"endpoint": "/webhook (POST)", "status": f"❌ {str(e)}"})
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 50)
    
    exitosos = 0
    for resultado in resultados:
        print(f"{resultado['status']} {resultado['endpoint']}")
        if "✅" in resultado['status']:
            exitosos += 1
    
    print(f"\n📈 Resultados: {exitosos}/{len(resultados)} endpoints funcionando")
    
    if exitosos == len(resultados):
        print("\n🎉 ¡DEPLOYMENT COMPLETAMENTE FUNCIONAL!")
        print("✅ Listo para conectar con WhatsApp")
        return True
    else:
        print("\n⚠️ Algunos endpoints tienen problemas")
        print("🔧 Revisar logs de Railway y configuración")
        return False

def main():
    print("🚀 VERIFICADOR DE DEPLOYMENT RAILWAY")
    print("=" * 60)
    
    # Solicitar URL de Railway
    url = input("🌐 Ingresa la URL de tu proyecto en Railway (ej: https://mi-proyecto.up.railway.app): ").strip()
    
    if not url:
        print("❌ URL no proporcionada")
        return
    
    if not url.startswith('http'):
        url = 'https://' + url
    
    # Remover trailing slash
    url = url.rstrip('/')
    
    print(f"\n🔍 Verificando: {url}")
    print("⏳ Esto puede tomar unos segundos...\n")
    
    # Verificar deployment
    success = verificar_railway_deployment(url)
    
    if success:
        print("\n📱 PRÓXIMO PASO: CONFIGURAR WHATSAPP")
        print("🔗 Usar Twilio WhatsApp Sandbox:")
        print("   1. Ve a twilio.com")
        print("   2. Console > Messaging > WhatsApp")
        print(f"   3. Webhook URL: {url}/webhook")
        print("   4. ¡Probar tu chatbot!")
    else:
        print("\n🔧 SOLUCIONAR PROBLEMAS PRIMERO:")
        print("   1. Revisar logs en Railway")
        print("   2. Verificar variables de entorno") 
        print("   3. Confirmar que MySQL esté conectado")

if __name__ == "__main__":
    main()
