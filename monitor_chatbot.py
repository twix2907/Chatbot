#!/usr/bin/env python3
"""
Script para monitorear la actividad del chatbot en tiempo real
"""
import requests
import time
import json
from datetime import datetime

def monitor_chatbot():
    railway_url = "https://chatbot-production-ec53.up.railway.app"
    
    print("📊 MONITOR DEL CHATBOT - PANADERÍA JOS & MAR")
    print("="*60)
    print(f"🔗 URL: {railway_url}")
    print("="*60)
    print("⏱️  Presiona Ctrl+C para detener el monitoreo")
    print("="*60)
    
    last_check = datetime.now()
    check_count = 0
    
    try:
        while True:
            check_count += 1
            current_time = datetime.now().strftime("%H:%M:%S")
            
            print(f"\n🔍 Check #{check_count} - {current_time}")
            
            # Test de salud rápido
            try:
                response = requests.get(f"{railway_url}/health", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    status = data.get('status', 'unknown')
                    db_status = data.get('database', 'unknown')
                    print(f"   ✅ App: {status} | DB: {db_status}")
                else:
                    print(f"   ❌ Status: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error: {str(e)[:50]}...")
            
            # Simular un mensaje cada 30 segundos para mantener activa la app
            if check_count % 6 == 0:  # Cada 6 checks (30 segundos)
                print("   🔄 Enviando ping para mantener activa la app...")
                try:
                    ping_data = {
                        'From': 'whatsapp:+51999999999',
                        'Body': 'ping',
                        'MessageSid': f'monitor_ping_{int(time.time())}'
                    }
                    ping_response = requests.post(
                        f"{railway_url}/webhook", 
                        data=ping_data, 
                        headers={'Content-Type': 'application/x-www-form-urlencoded'},
                        timeout=10
                    )
                    if ping_response.status_code == 200:
                        print("   ✅ Ping successful")
                    else:
                        print(f"   ⚠️  Ping status: {ping_response.status_code}")
                except Exception as e:
                    print(f"   ❌ Ping error: {str(e)[:50]}...")
            
            # Esperar 5 segundos antes del siguiente check
            time.sleep(5)
            
    except KeyboardInterrupt:
        print(f"\n\n🛑 Monitoreo detenido por el usuario")
        print(f"📊 Total de checks realizados: {check_count}")
        print("👋 ¡Hasta luego!")

def test_webhook_manual():
    """Función para probar el webhook manualmente"""
    railway_url = "https://chatbot-production-ec53.up.railway.app"
    
    print("🧪 PRUEBA MANUAL DEL WEBHOOK")
    print("="*40)
    
    while True:
        mensaje = input("\n💬 Escribe un mensaje para probar (o 'exit' para salir): ")
        
        if mensaje.lower() in ['exit', 'quit', 'salir']:
            print("👋 ¡Hasta luego!")
            break
        
        if not mensaje.strip():
            continue
        
        print(f"📤 Enviando: '{mensaje}'")
        
        try:
            test_data = {
                'From': 'whatsapp:+51999999999',
                'Body': mensaje,
                'MessageSid': f'manual_test_{int(time.time())}'
            }
            
            response = requests.post(
                f"{railway_url}/webhook",
                data=test_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=15
            )
            
            print(f"📨 Status: {response.status_code}")
            
            if response.status_code == 200:
                response_text = response.text
                
                # Extraer mensaje de TwiML
                if '<Message>' in response_text:
                    start = response_text.find('<Message>') + 9
                    end = response_text.find('</Message>')
                    if start > 8 and end > start:
                        bot_message = response_text[start:end]
                        print(f"🤖 Respuesta del bot:")
                        print(f"   {bot_message}")
                    else:
                        print("⚠️  No se pudo extraer el mensaje de la respuesta")
                else:
                    print(f"📝 Respuesta completa: {response_text[:200]}...")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   {response.text[:100]}...")
                
        except Exception as e:
            print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("🎯 HERRAMIENTAS DE MONITOREO")
    print("="*40)
    print("1. Monitor automático (cada 5 segundos)")
    print("2. Prueba manual del webhook")
    print("="*40)
    
    choice = input("Elige una opción (1 o 2): ").strip()
    
    if choice == "1":
        monitor_chatbot()
    elif choice == "2":
        test_webhook_manual()
    else:
        print("Opción no válida. Ejecutando monitor automático...")
        monitor_chatbot()
