#!/usr/bin/env python3
"""
Script para mostrar todas las variables de entorno que necesita la aplicación
"""
import os
from dotenv import load_dotenv

def mostrar_variables_entorno():
    print("🔧 VARIABLES DE ENTORNO REQUERIDAS PARA TU APP")
    print("=" * 60)
    
    # Cargar .env local para referencia
    load_dotenv()
    
    # Variables críticas para la aplicación
    variables_requeridas = {
        "Base de datos MySQL": {
            "MYSQL_HOST": {
                "descripcion": "Servidor de MySQL (Railway lo proporciona)",
                "ejemplo": "containers-us-west-xxx.railway.app",
                "actual": os.getenv('MYSQL_HOST', 'NO CONFIGURADO')
            },
            "MYSQL_PORT": {
                "descripcion": "Puerto de MySQL (Railway lo proporciona)", 
                "ejemplo": "6543",
                "actual": os.getenv('MYSQL_PORT', 'NO CONFIGURADO')
            },
            "MYSQL_USER": {
                "descripcion": "Usuario de MySQL (Railway: root)",
                "ejemplo": "root",
                "actual": os.getenv('MYSQL_USER', 'NO CONFIGURADO')
            },
            "MYSQL_PASSWORD": {
                "descripcion": "Contraseña de MySQL (Railway la genera)",
                "ejemplo": "abc123xyz789",
                "actual": "***CONFIGURADO***" if os.getenv('MYSQL_PASSWORD') else 'NO CONFIGURADO'
            },
            "MYSQL_DATABASE": {
                "descripcion": "Nombre de BD (Railway: railway)",
                "ejemplo": "railway", 
                "actual": os.getenv('MYSQL_DATABASE', 'NO CONFIGURADO')
            }
        },
        "Servidor Flask": {
            "PORT": {
                "descripcion": "Puerto del servidor (Railway lo asigna)",
                "ejemplo": "5000",
                "actual": os.getenv('PORT', '5000 (default)')
            },
            "FLASK_DEBUG": {
                "descripcion": "Modo debug (false para producción)",
                "ejemplo": "false",
                "actual": os.getenv('FLASK_DEBUG', 'false (default)')
            }
        },
        "Twilio WhatsApp": {
            "WEBHOOK_VERIFY_TOKEN": {
                "descripcion": "Token para verificar webhook de Twilio",
                "ejemplo": "panaderia_jos_mar_2025",
                "actual": os.getenv('WEBHOOK_VERIFY_TOKEN', 
                                  os.getenv('WHATSAPP_VERIFY_TOKEN', 'panaderia_jos_mar_2025 (default)'))
            },
            "TWILIO_ACCOUNT_SID": {
                "descripcion": "Account SID de Twilio",
                "ejemplo": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "actual": "***CONFIGURADO***" if os.getenv('TWILIO_ACCOUNT_SID') else 'NO CONFIGURADO'
            },
            "TWILIO_AUTH_TOKEN": {
                "descripcion": "Auth Token de Twilio",
                "ejemplo": "your_auth_token_here",
                "actual": "***CONFIGURADO***" if os.getenv('TWILIO_AUTH_TOKEN') else 'NO CONFIGURADO'
            }
        }
    }
    
    # Mostrar variables por categoría
    for categoria, variables in variables_requeridas.items():
        print(f"\n📂 {categoria.upper()}:")
        print("-" * 40)
        
        for var_name, var_info in variables.items():
            status = "✅" if "NO CONFIGURADO" not in var_info['actual'] else "❌"
            print(f"{status} {var_name}")
            print(f"   📝 {var_info['descripcion']}")
            print(f"   💡 Ejemplo: {var_info['ejemplo']}")
            print(f"   🔧 Actual: {var_info['actual']}")
            print()
    
    # Variables opcionales
    print("📋 VARIABLES OPCIONALES (no críticas):")
    print("-" * 40)
    
    variables_opcionales = {
        "WHATSAPP_TOKEN": "Token de acceso de Meta WhatsApp API",
        "WHATSAPP_PHONE_NUMBER_ID": "ID del número de teléfono de WhatsApp",
        "DIALOGFLOW_PROJECT_ID": "ID del proyecto de Dialogflow",
        "GOOGLE_APPLICATION_CREDENTIALS": "Credenciales de Google Cloud"
    }
    
    for var_name, descripcion in variables_opcionales.items():
        valor = os.getenv(var_name, 'No configurado')
        print(f"• {var_name}: {descripcion}")
        print(f"  Valor: {valor}")
        print()
    
    # Generar configuración para Railway
    print("🚀 CONFIGURACIÓN PARA RAILWAY:")
    print("=" * 40)
    print("Copia estas variables en Railway > Variables:")
    print()
    
    railway_vars = [
        "# Estas las copia de Railway MySQL Service:",
        "MYSQL_HOST=<host-generado-por-railway>",
        "MYSQL_PORT=<puerto-generado-por-railway>", 
        "MYSQL_USER=root",
        "MYSQL_PASSWORD=<password-generado-por-railway>",
        "MYSQL_DATABASE=railway",
        "",
        "# Configuración del servidor:",
        "FLASK_DEBUG=false",
        "",
        "# WhatsApp webhook:", 
        "WEBHOOK_VERIFY_TOKEN=panaderia_jos_mar_2025"
    ]
    
    for line in railway_vars:
        print(line)
    
    # Verificar si hay problemas
    print("\n⚠️  VERIFICACIÓN DE PROBLEMAS:")
    print("-" * 40)
    
    problemas = []
    
    # Verificar variables críticas de BD
    bd_vars = ['MYSQL_HOST', 'MYSQL_PORT', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE']
    for var in bd_vars:
        if not os.getenv(var):
            problemas.append(f"❌ {var} no está configurado")
    
    # Verificar inconsistencia de tokens
    webhook_token = os.getenv('WEBHOOK_VERIFY_TOKEN')
    whatsapp_token = os.getenv('WHATSAPP_VERIFY_TOKEN')
    
    if not webhook_token and not whatsapp_token:
        problemas.append("❌ No hay token de verificación configurado")
    elif webhook_token != whatsapp_token and (webhook_token and whatsapp_token):
        problemas.append("⚠️  Inconsistencia: WEBHOOK_VERIFY_TOKEN ≠ WHATSAPP_VERIFY_TOKEN")
    
    if problemas:
        for problema in problemas:
            print(problema)
    else:
        print("✅ No se detectaron problemas críticos")

if __name__ == "__main__":
    mostrar_variables_entorno()
