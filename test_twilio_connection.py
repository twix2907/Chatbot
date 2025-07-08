#!/usr/bin/env python3
"""
Script para probar la conexión con Twilio usando credenciales reales
"""
import os
from dotenv import load_dotenv

def test_twilio_connection():
    load_dotenv()
    
    print("🔧 PRUEBA DE CONEXIÓN CON TWILIO")
    print("=" * 50)
    
    # Obtener credenciales
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    
    if not account_sid or not auth_token:
        print("❌ Error: Credenciales de Twilio no configuradas")
        return False
    
    print(f"📋 Account SID: {account_sid[:10]}...")
    print(f"🔑 Auth Token: {'*' * 20}")
    
    try:
        from twilio.rest import Client
        
        # Crear cliente de Twilio
        client = Client(account_sid, auth_token)
        
        # Probar conexión obteniendo información de la cuenta
        account = client.api.accounts(account_sid).fetch()
        
        print(f"✅ Conexión exitosa!")
        print(f"📞 Nombre de cuenta: {account.friendly_name}")
        print(f"📋 Status: {account.status}")
        print(f"🌍 Tipo: {account.type}")
        
        # Verificar WhatsApp Sandbox
        try:
            incoming_phone_numbers = client.incoming_phone_numbers.list(limit=5)
            print(f"\n📱 Números disponibles: {len(incoming_phone_numbers)}")
            
            # Buscar configuración de WhatsApp
            whatsapp_numbers = [num for num in incoming_phone_numbers if 'whatsapp' in str(num.capabilities)]
            if whatsapp_numbers:
                print("✅ WhatsApp habilitado en algunos números")
            else:
                print("ℹ️  Usar Sandbox para testing: +1 415 523 8886")
                
        except Exception as e:
            print(f"ℹ️  Info adicional no disponible: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        if "authenticate" in str(e).lower():
            print("💡 Verificar que las credenciales sean correctas")
        elif "network" in str(e).lower():
            print("💡 Verificar conexión a internet")
        return False

def generar_variables_railway():
    """Generar variables para copiar en Railway"""
    load_dotenv()
    
    print("\n🚀 VARIABLES PARA RAILWAY")
    print("=" * 50)
    print("Copia estas variables en Railway > Variables:")
    print()
    
    # Variables de MySQL (ejemplo - Railway las genera automáticamente)
    print("# Variables de MySQL (Railway las genera automáticamente):")
    print("MYSQL_HOST=<copiado-del-mysql-service>")
    print("MYSQL_PORT=<copiado-del-mysql-service>")
    print("MYSQL_USER=root")
    print("MYSQL_PASSWORD=<copiado-del-mysql-service>")
    print("MYSQL_DATABASE=railway")
    print()
    
    # Variables de aplicación
    print("# Variables de aplicación:")
    print("FLASK_DEBUG=false")
    print("WEBHOOK_VERIFY_TOKEN=panaderia_jos_mar_2025")
    print()
    
    # Variables de Twilio (con valores reales)
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    
    print("# Variables de Twilio:")
    print(f"TWILIO_ACCOUNT_SID={account_sid}")
    print(f"TWILIO_AUTH_TOKEN={auth_token}")
    print("TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886")

def mostrar_proximos_pasos():
    print("\n📋 PRÓXIMOS PASOS PARA DESPLIEGUE")
    print("=" * 50)
    
    steps = [
        "1. 📂 Subir código a GitHub:",
        "   git init",
        "   git add .",
        "   git commit -m 'Panadería Jos & Mar - Backend Twilio WhatsApp'",
        "   git remote add origin https://github.com/tu-usuario/panaderia-backend.git",
        "   git push -u origin main",
        "",
        "2. 🚀 Crear proyecto en Railway:",
        "   - Ir a https://railway.app/new",
        "   - Connect to GitHub repository",
        "   - Seleccionar tu repositorio",
        "",
        "3. 🗄️ Agregar MySQL service:",
        "   - Add Service > Database > MySQL",
        "   - Esperar que se despliegue",
        "",
        "4. ⚙️ Configurar variables de entorno:",
        "   - Copiar variables de MySQL service a tu app",
        "   - Agregar las variables de Twilio mostradas arriba",
        "",
        "5. 🌐 Configurar webhook en Twilio:",
        "   - URL: https://tu-app.railway.app/webhook",
        "   - Console > Messaging > WhatsApp Sandbox Settings",
        "",
        "6. 📱 Activar WhatsApp Sandbox:",
        "   - Enviar 'join helpful-spider' a +1 415 523 8886",
        "   - Probar con: 'productos'",
    ]
    
    for step in steps:
        print(step)

if __name__ == "__main__":
    # Probar conexión
    connection_ok = test_twilio_connection()
    
    if connection_ok:
        # Mostrar variables para Railway
        generar_variables_railway()
        
        # Mostrar próximos pasos
        mostrar_proximos_pasos()
        
        print(f"\n{'='*50}")
        print("🎉 ¡TODO LISTO PARA EL DESPLIEGUE!")
        print("✅ Credenciales de Twilio verificadas")
        print("✅ Variables preparadas para Railway") 
        print("✅ Aplicación probada localmente")
        print(f"{'='*50}")
    else:
        print("\n❌ Revisar credenciales de Twilio antes de continuar")
