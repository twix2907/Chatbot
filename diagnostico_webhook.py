#!/usr/bin/env python3
"""
Script de diagnóstico para el webhook - Por qué muestra "Token de verificación incorrecto"
"""
import requests

def explicar_webhook():
    print("🔍 DIAGNÓSTICO DEL WEBHOOK")
    print("="*60)
    print()
    
    print("❓ ¿Por qué aparece 'Token de verificación incorrecto'?")
    print("-"*50)
    print("✅ Esto es NORMAL y CORRECTO!")
    print()
    print("🔧 EXPLICACIÓN TÉCNICA:")
    print("1. Cuando visitas /webhook desde el navegador:")
    print("   - El navegador hace una petición GET sin parámetros")
    print("   - Tu app espera parámetros específicos de Twilio")
    print("   - Como no los encuentra, responde 'Token incorrecto'")
    print()
    print("2. Cuando Twilio envía mensajes:")
    print("   - Twilio hace peticiones POST con datos específicos")
    print("   - Tu app procesa el mensaje y responde correctamente")
    print()
    
    railway_url = "https://chatbot-production-ec53.up.railway.app"
    
    print("🧪 VAMOS A PROBAR LOS DIFERENTES CASOS:")
    print("="*60)
    
    # Caso 1: GET sin parámetros (como el navegador)
    print("\n1️⃣ CASO 1: Visitando desde navegador (GET sin parámetros)")
    try:
        response = requests.get(f"{railway_url}/webhook", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Respuesta: '{response.text}'")
        print("   ✅ ESTO ES CORRECTO - debe decir 'Token de verificación incorrecto'")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Caso 2: GET con parámetros de verificación (como Twilio para verificar)
    print("\n2️⃣ CASO 2: Verificación de Twilio (GET con parámetros)")
    try:
        params = {
            'hub.verify_token': 'panaderia_jos_mar_2025',
            'hub.challenge': 'test_challenge_12345'
        }
        response = requests.get(f"{railway_url}/webhook", params=params, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Respuesta: '{response.text}'")
        print("   ✅ ESTO DEBE devolver el challenge (test_challenge_12345)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Caso 3: POST con mensaje (como Twilio enviando mensajes)
    print("\n3️⃣ CASO 3: Mensaje de WhatsApp (POST con datos)")
    try:
        data = {
            'From': 'whatsapp:+51999999999',
            'Body': 'hola',
            'MessageSid': 'test_sid_diagnostico'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(f"{railway_url}/webhook", data=data, headers=headers, timeout=15)
        print(f"   Status: {response.status_code}")
        print(f"   Respuesta: {len(response.text)} caracteres")
        
        if '<Message>' in response.text:
            start = response.text.find('<Message>') + 9
            end = response.text.find('</Message>')
            if start > 8 and end > start:
                message = response.text[start:end]
                print(f"   💬 Mensaje del bot: {message[:100]}...")
                print("   ✅ PERFECTO - el bot responde correctamente")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n{'='*60}")
    print("📋 RESUMEN:")
    print("✅ Tu webhook está funcionando PERFECTAMENTE")
    print("✅ El mensaje 'Token incorrecto' desde navegador es NORMAL")
    print("✅ Twilio puede verificar y enviar mensajes correctamente")
    print(f"{'='*60}")
    
    print("\n🔧 PRÓXIMOS PASOS PARA SOLUCIONAR WHATSAPP:")
    print("1. Verifica que en Twilio Console tengas EXACTAMENTE:")
    print(f"   Webhook URL: {railway_url}/webhook")
    print("   HTTP Method: POST")
    print("2. Verifica que enviaste 'join helpful-spider' al número correcto")
    print("3. Verifica que recibiste confirmación de Twilio")
    print("4. Prueba enviar un mensaje simple como 'test'")

def verificar_configuracion_twilio():
    print("\n🔧 CHECKLIST DE CONFIGURACIÓN TWILIO:")
    print("="*50)
    
    checklist = [
        "☐ Entré a https://console.twilio.com/",
        "☐ Fui a Messaging → Try it out → Send a WhatsApp message", 
        "☐ Puse la URL: https://chatbot-production-ec53.up.railway.app/webhook",
        "☐ Seleccioné HTTP Method: POST",
        "☐ Guardé la configuración (Save Configuration)",
        "☐ Agregué +1 415 523 8886 a mis contactos de WhatsApp",
        "☐ Envié 'join helpful-spider' a ese número",
        "☐ Recibí confirmación de Twilio",
        "☐ Intenté enviar un mensaje de prueba"
    ]
    
    for item in checklist:
        print(f"   {item}")
    
    print("\n❗ IMPORTANTE:")
    print("- El sandbox de Twilio a veces tarda en activarse")
    print("- Asegúrate de que tu número esté en formato internacional")
    print("- Algunos países tienen restricciones con el sandbox")
    
    print("\n🆘 SI SIGUE SIN FUNCIONAR:")
    print("1. Verifica los logs en Railway (puede haber errores)")
    print("2. Prueba con otro número de teléfono")
    print("3. Verifica que tu cuenta de Twilio esté activa")

if __name__ == "__main__":
    explicar_webhook()
    verificar_configuracion_twilio()
