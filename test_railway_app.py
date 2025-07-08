#!/usr/bin/env python3
"""
Script para probar tu app desplegada en Railway
"""
import requests
import json

def test_railway_app():
    print("🧪 TESTING DE TU APP EN RAILWAY")
    print("="*50)
    
    # Pedir URL de Railway al usuario
    railway_url = input("🌐 Ingresa la URL de tu app en Railway (ej: https://tu-app-xxx.railway.app): ").strip()
    
    if not railway_url:
        print("❌ URL requerida")
        return
    
    if not railway_url.startswith('https://'):
        railway_url = 'https://' + railway_url
    
    print(f"\n🔗 Testing URL: {railway_url}")
    
    # Test 1: Health check
    print("\n1️⃣ Testing /health endpoint...")
    try:
        response = requests.get(f"{railway_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data.get('status', 'unknown')}")
            print(f"📊 Database: {data.get('database', 'unknown')}")
            print(f"📝 Message: {data.get('message', 'No message')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error connecting to health endpoint: {e}")
        return False
    
    # Test 2: Info endpoint
    print("\n2️⃣ Testing /info endpoint...")
    try:
        response = requests.get(f"{railway_url}/info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ App name: {data.get('name', 'unknown')}")
            print(f"🔢 Version: {data.get('version', 'unknown')}")
            print(f"📱 WhatsApp ready: {data.get('whatsapp_ready', 'unknown')}")
        else:
            print(f"❌ Info endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Webhook verification (GET)
    print("\n3️⃣ Testing webhook verification...")
    try:
        verify_token = "panaderia_jos_mar_2025"
        challenge = "test_challenge_123"
        
        params = {
            'hub.verify_token': verify_token,
            'hub.challenge': challenge
        }
        
        response = requests.get(f"{railway_url}/webhook", params=params, timeout=10)
        if response.status_code == 200 and response.text == challenge:
            print("✅ Webhook verification working")
        else:
            print(f"❌ Webhook verification failed: {response.status_code}")
            print(f"   Expected: {challenge}")
            print(f"   Got: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Simular mensaje de Twilio
    print("\n4️⃣ Testing Twilio webhook simulation...")
    try:
        twilio_data = {
            'From': 'whatsapp:+51999999999',
            'Body': 'productos',
            'MessageSid': 'test_sid_123'
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.post(f"{railway_url}/webhook", data=twilio_data, headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ Twilio webhook simulation successful")
            print(f"📝 Response preview: {response.text[:100]}...")
            if '<Message>' in response.text:
                print("✅ TwiML response detected")
            else:
                print("⚠️  Unexpected response format")
        else:
            print(f"❌ Webhook test failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Mostrar configuración para Twilio
    print(f"\n🔧 CONFIGURACIÓN PARA TWILIO:")
    print("="*50)
    print(f"📋 Webhook URL: {railway_url}/webhook")
    print("📋 HTTP Method: POST")
    print("📋 Content-Type: application/x-www-form-urlencoded")
    print("\n📱 Para activar WhatsApp Sandbox:")
    print("1. Ir a: https://console.twilio.com/")
    print("2. Messaging → Try it out → Send a WhatsApp message")
    print("3. Configurar webhook URL arriba")
    print("4. Enviar 'join helpful-spider' a +1 415 523 8886")
    print("5. Probar con: 'productos'")
    
    return True

if __name__ == "__main__":
    test_railway_app()
