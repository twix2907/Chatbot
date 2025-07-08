#!/usr/bin/env python3
"""
Script de diagnóstico específico para el problema de WhatsApp sin respuesta
"""
import requests
import time

def diagnosticar_problema_whatsapp():
    railway_url = "https://chatbot-production-ec53.up.railway.app"
    
    print("🔍 DIAGNÓSTICO ESPECÍFICO - SIN RESPUESTA EN WHATSAPP")
    print("="*60)
    print("HTTP 200 ✅ pero sin respuesta en WhatsApp ❌")
    print("="*60)
    
    # Test exacto como lo envía Twilio
    print("\n1️⃣ SIMULANDO MENSAJE EXACTO DE TWILIO...")
    print("-"*50)
    
    test_data = {
        'From': 'whatsapp:+51999999999',
        'To': 'whatsapp:+14155238886',
        'Body': 'Hola',
        'MessageSid': 'SM_test_diagnostico',
        'AccountSid': 'AC_test',
        'MessagingServiceSid': 'MG_test'
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'TwilioProxy/1.1'
    }
    
    try:
        print(f"📤 Enviando exactamente como Twilio...")
        print(f"   Data: {test_data}")
        print(f"   Headers: {headers}")
        
        response = requests.post(
            f"{railway_url}/webhook", 
            data=test_data, 
            headers=headers, 
            timeout=15
        )
        
        print(f"\n📨 RESPUESTA:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print(f"   Content-Type: {response.headers.get('Content-Type')}")
        print(f"   Content Length: {len(response.text)}")
        
        if response.status_code == 200:
            print("   ✅ HTTP 200 - OK")
            
            # Verificar formato TwiML
            response_text = response.text
            print(f"\n📝 CONTENIDO DE LA RESPUESTA:")
            print(f"   Texto completo: {repr(response_text)}")
            
            if '<?xml' in response_text and '<Response>' in response_text:
                print("   ✅ Formato TwiML correcto")
                
                if '<Message>' in response_text and '</Message>' in response_text:
                    print("   ✅ Elemento Message encontrado")
                    
                    # Extraer mensaje
                    start = response_text.find('<Message>') + 9
                    end = response_text.find('</Message>')
                    if start > 8 and end > start:
                        message_content = response_text[start:end]
                        print(f"   💬 Contenido del mensaje: {repr(message_content)}")
                        
                        if len(message_content.strip()) > 0:
                            print("   ✅ Mensaje no está vacío")
                        else:
                            print("   ❌ PROBLEMA: Mensaje está vacío")
                    else:
                        print("   ❌ PROBLEMA: No se pudo extraer contenido del mensaje")
                else:
                    print("   ❌ PROBLEMA: No hay elemento <Message> en TwiML")
            else:
                print("   ❌ PROBLEMA: Respuesta no está en formato TwiML")
                print("   Expected: <?xml...><Response><Message>...")
                print(f"   Got: {response_text[:200]}...")
        else:
            print(f"   ❌ Error HTTP: {response.status_code}")
            print(f"   Error content: {response.text}")
    
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    # Verificar con otros mensajes
    print(f"\n2️⃣ PROBANDO OTROS MENSAJES...")
    print("-"*50)
    
    test_messages = ['hola', 'productos', 'test', 'ayuda']
    
    for msg in test_messages:
        print(f"\n   Probando: '{msg}'")
        test_data['Body'] = msg
        
        try:
            response = requests.post(
                f"{railway_url}/webhook", 
                data=test_data, 
                headers=headers, 
                timeout=10
            )
            
            if response.status_code == 200:
                if '<Message>' in response.text:
                    start = response.text.find('<Message>') + 9
                    end = response.text.find('</Message>')
                    if start > 8 and end > start:
                        content = response.text[start:end]
                        print(f"      ✅ Respuesta: {content[:60]}...")
                    else:
                        print("      ❌ Sin contenido en mensaje")
                else:
                    print("      ❌ Sin elemento Message")
            else:
                print(f"      ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"      ❌ Error: {str(e)[:40]}...")
        
        time.sleep(1)  # Esperar entre requests
    
    print(f"\n{'='*60}")
    print("📊 DIAGNÓSTICO COMPLETADO")
    print("='*60")
    
    print("\n🔧 POSIBLES CAUSAS DEL PROBLEMA:")
    print("1. ❓ Configuración incorrecta en Twilio Console")
    print("2. ❓ Webhook URL no actualizada en Twilio")
    print("3. ❓ Sandbox de Twilio no configurado correctamente")
    print("4. ❓ Número no registrado en el sandbox")
    print("5. ❓ Delay en la entrega de mensajes de Twilio")
    
    print("\n💡 SIGUIENTES PASOS:")
    print("1. Verifica la configuración exacta en Twilio Console")
    print("2. Revisa los logs en Railway mientras envías un mensaje")
    print("3. Confirma que recibiste la confirmación del sandbox")
    print("4. Prueba enviar mensajes simples como 'test'")

if __name__ == "__main__":
    diagnosticar_problema_whatsapp()
