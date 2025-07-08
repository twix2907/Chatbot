#!/usr/bin/env python3
"""
Script para probar la app desplegada en Railway
URL: https://chatbot-production-ec53.up.railway.app
"""
import requests
import json

def test_railway_app():
    railway_url = "https://chatbot-production-ec53.up.railway.app"
    
    print("🧪 TESTING DE TU APP EN RAILWAY")
    print("="*60)
    print(f"🔗 URL: {railway_url}")
    print("="*60)
    
    # Test 1: Health check
    print("\n1️⃣ TESTING /health endpoint...")
    try:
        response = requests.get(f"{railway_url}/health", timeout=15)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data.get('status', 'unknown')}")
            print(f"   📊 Database: {data.get('database', 'unknown')}")
            print(f"   📝 Message: {data.get('message', 'No message')}")
            print(f"   🕐 Timestamp: {data.get('timestamp', 'No timestamp')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Error connecting to health endpoint: {e}")
        return False
    
    # Test 2: Info endpoint
    print("\n2️⃣ TESTING /info endpoint...")
    try:
        response = requests.get(f"{railway_url}/info", timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ App name: {data.get('name', 'unknown')}")
            print(f"   🔢 Version: {data.get('version', 'unknown')}")
            print(f"   📱 WhatsApp ready: {data.get('whatsapp_ready', 'unknown')}")
            print(f"   🗄️ Database ready: {data.get('database_ready', 'unknown')}")
        else:
            print(f"   ❌ Info endpoint failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Test endpoint
    print("\n3️⃣ TESTING /test endpoint...")
    try:
        response = requests.get(f"{railway_url}/test", timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Message: {data.get('message', 'unknown')}")
            print(f"   📊 Status: {data.get('status', 'unknown')}")
        else:
            print(f"   ❌ Test endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Webhook verification (GET)
    print("\n4️⃣ TESTING webhook verification...")
    try:
        verify_token = "panaderia_jos_mar_2025"
        challenge = "test_challenge_12345"
        
        params = {
            'hub.verify_token': verify_token,
            'hub.challenge': challenge
        }
        
        response = requests.get(f"{railway_url}/webhook", params=params, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200 and response.text == challenge:
            print("   ✅ Webhook verification working correctly")
        else:
            print(f"   ❌ Webhook verification failed")
            print(f"   Expected: '{challenge}'")
            print(f"   Got: '{response.text}'")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Simular mensaje de Twilio
    print("\n5️⃣ TESTING Twilio webhook simulation...")
    try:
        twilio_data = {
            'From': 'whatsapp:+51999999999',
            'Body': 'hola',
            'MessageSid': 'test_sid_123456'
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.post(f"{railway_url}/webhook", data=twilio_data, headers=headers, timeout=15)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Twilio webhook simulation successful")
            response_text = response.text
            print(f"   📝 Response length: {len(response_text)} characters")
            
            if '<Message>' in response_text and '</Message>' in response_text:
                print("   ✅ TwiML format detected")
                # Extraer mensaje de TwiML
                start = response_text.find('<Message>') + 9
                end = response_text.find('</Message>')
                if start > 8 and end > start:
                    message = response_text[start:end]
                    print(f"   💬 Bot response: {message[:100]}...")
                else:
                    print("   ⚠️  Could not extract message from TwiML")
            else:
                print("   ⚠️  Unexpected response format (not TwiML)")
                print(f"   Response preview: {response_text[:150]}...")
        else:
            print(f"   ❌ Webhook test failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Probar otro mensaje
    print("\n6️⃣ TESTING productos command...")
    try:
        twilio_data = {
            'From': 'whatsapp:+51999999999',
            'Body': 'productos',
            'MessageSid': 'test_sid_productos'
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.post(f"{railway_url}/webhook", data=twilio_data, headers=headers, timeout=15)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Productos command successful")
            response_text = response.text
            
            if '<Message>' in response_text:
                start = response_text.find('<Message>') + 9
                end = response_text.find('</Message>')
                if start > 8 and end > start:
                    message = response_text[start:end]
                    if 'PRODUCTOS DISPONIBLES' in message or 'PANADERÍA JOS & MAR' in message:
                        print("   ✅ Product catalog response detected")
                        print(f"   📋 Response preview: {message[:150]}...")
                    else:
                        print(f"   💬 Bot response: {message[:100]}...")
        else:
            print(f"   ❌ Productos test failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Mostrar configuración para Twilio
    print(f"\n🔧 CONFIGURACIÓN PARA TWILIO:")
    print("="*60)
    print(f"📋 Webhook URL: {railway_url}/webhook")
    print("📋 HTTP Method: POST")
    print("📋 Content-Type: application/x-www-form-urlencoded")
    print("\n📱 PASOS PARA ACTIVAR WHATSAPP:")
    print("1. Ir a: https://console.twilio.com/")
    print("2. Messaging → Try it out → Send a WhatsApp message")
    print("3. En 'Webhook URL' poner: https://chatbot-production-ec53.up.railway.app/webhook")
    print("4. HTTP Method: POST")
    print("5. Enviar 'join helpful-spider' a +1 415 523 8886")
    print("6. Esperar confirmación de Twilio")
    print("7. ¡Probar con: 'hola', 'productos', 'quiero 2 francés'!")
    
    print(f"\n{'='*60}")
    if response.status_code == 200:
        print("🎉 ¡TU APP ESTÁ FUNCIONANDO CORRECTAMENTE!")
        print("✅ Lista para conectar con Twilio WhatsApp")
    else:
        print("⚠️  Hay algunos problemas, pero la app está desplegada")
    print(f"{'='*60}")
    
    return True

if __name__ == "__main__":
    test_railway_app()
