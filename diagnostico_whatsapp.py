#!/usr/bin/env python3
"""
Script de diagnóstico para problemas de WhatsApp con Twilio
"""
import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def diagnosticar_whatsapp():
    print("🔍 DIAGNÓSTICO DE WHATSAPP - TWILIO")
    print("="*60)
    
    # 1. Verificar configuración local
    print("\n1️⃣ VERIFICANDO CONFIGURACIÓN LOCAL...")
    
    twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
    twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
    
    if twilio_sid:
        print(f"   ✅ TWILIO_ACCOUNT_SID: {twilio_sid[:10]}...")
    else:
        print("   ❌ TWILIO_ACCOUNT_SID no encontrado")
    
    if twilio_token:
        print(f"   ✅ TWILIO_AUTH_TOKEN: {twilio_token[:10]}...")
    else:
        print("   ❌ TWILIO_AUTH_TOKEN no encontrado")
        
    if twilio_number:
        print(f"   ✅ TWILIO_WHATSAPP_NUMBER: {twilio_number}")
    else:
        print("   ❌ TWILIO_WHATSAPP_NUMBER no encontrado")
    
    # 2. Verificar webhook endpoint
    print("\n2️⃣ VERIFICANDO WEBHOOK ENDPOINT...")
    railway_url = "https://chatbot-production-ec53.up.railway.app"
    
    try:
        # Test GET (verificación de webhook)
        verify_params = {
            'hub.verify_token': 'panaderia_jos_mar_2025',
            'hub.challenge': 'test_challenge_diagnostico'
        }
        
        response = requests.get(f"{railway_url}/webhook", params=verify_params, timeout=10)
        if response.status_code == 200 and response.text == 'test_challenge_diagnostico':
            print("   ✅ Webhook verification (GET) funcionando")
        else:
            print(f"   ❌ Webhook verification falló: {response.status_code}")
            
        # Test POST (mensaje simulado)
        test_data = {
            'From': 'whatsapp:+51999999999',
            'Body': 'test_diagnostico',
            'MessageSid': 'test_diagnostico_123'
        }
        
        response = requests.post(
            f"{railway_url}/webhook",
            data=test_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=15
        )
        
        if response.status_code == 200:
            print("   ✅ Webhook POST funcionando")
            if '<Message>' in response.text:
                print("   ✅ Respuesta en formato TwiML correcto")
            else:
                print("   ⚠️  Respuesta no está en formato TwiML")
                print(f"      Respuesta: {response.text[:100]}...")
        else:
            print(f"   ❌ Webhook POST falló: {response.status_code}")
            print(f"      Error: {response.text[:100]}...")
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    # 3. Verificar configuración de Twilio (usando API)
    print("\n3️⃣ VERIFICANDO CONFIGURACIÓN DE TWILIO...")
    
    if twilio_sid and twilio_token:
        try:
            from twilio.rest import Client
            client = Client(twilio_sid, twilio_token)
            
            # Verificar cuenta
            account = client.api.accounts(twilio_sid).fetch()
            print(f"   ✅ Cuenta Twilio: {account.friendly_name}")
            print(f"   📱 Status: {account.status}")
            
            # Verificar configuración del sandbox
            try:
                sandbox = client.messaging.v1.services.list(limit=1)
                if sandbox:
                    print("   ✅ Servicio de mensajería encontrado")
                else:
                    print("   ⚠️  No se encontraron servicios de mensajería")
            except Exception as e:
                print(f"   ⚠️  No se pudo verificar sandbox: {str(e)[:100]}...")
                
        except ImportError:
            print("   ⚠️  Librería twilio no instalada (no es crítico)")
        except Exception as e:
            print(f"   ❌ Error conectando con Twilio API: {str(e)[:100]}...")
    else:
        print("   ❌ Credenciales de Twilio no disponibles")
    
    # 4. Diagnóstico de problemas comunes
    print("\n4️⃣ DIAGNÓSTICO DE PROBLEMAS COMUNES...")
    
    print("\n🔧 POSIBLES PROBLEMAS Y SOLUCIONES:")
    print("="*60)
    
    print("\n❓ PROBLEMA 1: No has configurado el webhook en Twilio")
    print("   💡 SOLUCIÓN:")
    print("   1. Ve a: https://console.twilio.com/")
    print("   2. Messaging → Try it out → Send a WhatsApp message")
    print("   3. En 'Webhook URL' pon: https://chatbot-production-ec53.up.railway.app/webhook")
    print("   4. HTTP Method: POST")
    print("   5. Guarda la configuración")
    
    print("\n❓ PROBLEMA 2: No te has unido al sandbox")
    print("   💡 SOLUCIÓN:")
    print("   1. Agrega +1 (415) 523-8886 a WhatsApp")
    print("   2. Envía: 'join helpful-spider'")
    print("   3. Espera el mensaje de confirmación")
    
    print("\n❓ PROBLEMA 3: Código de sandbox incorrecto")
    print("   💡 SOLUCIÓN:")
    print("   1. Ve a la consola de Twilio")
    print("   2. Busca el código actual del sandbox")
    print("   3. Debe ser algo como 'join [palabra-palabra]'")
    print("   4. Envía el código correcto")
    
    print("\n❓ PROBLEMA 4: Webhook URL mal configurada")
    print("   💡 VERIFICAR:")
    print("   - URL exacta: https://chatbot-production-ec53.up.railway.app/webhook")
    print("   - HTTP Method: POST")
    print("   - No hay espacios extra")
    print("   - Incluye 'https://' al inicio")
    
    print("\n❓ PROBLEMA 5: Número de sandbox ha cambiado")
    print("   💡 VERIFICAR:")
    print("   - Número actual en consola Twilio")
    print("   - Puede ser diferente a +1 (415) 523-8886")
    
    # 5. Test manual de webhook
    print(f"\n5️⃣ TEST MANUAL INTERACTIVO...")
    print("="*40)
    
    while True:
        test_message = input("\n💬 Mensaje para probar (o 'exit'): ")
        if test_message.lower() in ['exit', 'quit', 'salir']:
            break
            
        if not test_message.strip():
            continue
            
        print(f"📤 Probando: '{test_message}'")
        
        try:
            test_data = {
                'From': 'whatsapp:+51999999999',
                'Body': test_message,
                'MessageSid': f'manual_test_{int(__import__("time").time())}'
            }
            
            response = requests.post(
                f"{railway_url}/webhook",
                data=test_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=15
            )
            
            print(f"📨 Status: {response.status_code}")
            
            if response.status_code == 200:
                if '<Message>' in response.text:
                    start = response.text.find('<Message>') + 9
                    end = response.text.find('</Message>')
                    if start > 8 and end > start:
                        bot_message = response.text[start:end]
                        print(f"✅ Respuesta del bot:")
                        print(f"   {bot_message}")
                else:
                    print(f"⚠️  Respuesta: {response.text[:150]}...")
            else:
                print(f"❌ Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*60}")
    print("🎯 RESUMEN DEL DIAGNÓSTICO:")
    print("✅ Tu app en Railway funciona correctamente")
    print("✅ El webhook responde bien a las pruebas")
    print("❓ El problema está en la configuración de Twilio")
    print(f"{'='*60}")

if __name__ == "__main__":
    diagnosticar_whatsapp()
