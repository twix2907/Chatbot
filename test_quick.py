#!/usr/bin/env python3
"""
Test rápido para verificar que tu app desplegada funcione
"""
import requests

def test_quick(url):
    """Test rápido de la app"""
    if not url.startswith('https://'):
        url = 'https://' + url
    
    print(f"🔗 Testing: {url}")
    
    try:
        # Test básico de salud
        response = requests.get(f"{url}/health", timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data.get('status')}")
            print(f"🗄️ Database: {data.get('database')}")
            print(f"📝 Message: {data.get('message')}")
            print("\n🎉 ¡Tu app está funcionando!")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando: {e}")
        return False

# Ejemplo de uso:
# test_quick("tu-app-xxx.railway.app")

if __name__ == "__main__":
    url = input("🌐 Ingresa la URL de tu app Railway: ").strip()
    test_quick(url)
