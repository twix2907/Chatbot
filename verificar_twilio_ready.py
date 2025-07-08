#!/usr/bin/env python3
"""
Script para verificar que la app esté lista para el despliegue con Twilio WhatsApp
"""
import os
import requests
from dotenv import load_dotenv
import sys

# Cargar variables de entorno
load_dotenv()

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)

def print_status(item, status, details=""):
    icon = "✅" if status else "❌"
    print(f"{icon} {item}")
    if details:
        print(f"   💡 {details}")

def check_required_files():
    """Verificar que existan los archivos necesarios"""
    print_header("VERIFICACIÓN DE ARCHIVOS")
    
    required_files = [
        'app_twilio.py',  # App principal
        'database.py',    # Conexión BD
        'requirements.txt', # Dependencias
        'Procfile',       # Configuración Railway
        '.env.example',   # Template variables
        'TWILIO_WHATSAPP_SETUP.md' # Documentación
    ]
    
    all_good = True
    for file in required_files:
        exists = os.path.exists(file)
        all_good = all_good and exists
        print_status(f"Archivo {file}", exists)
    
    return all_good

def check_environment_variables():
    """Verificar variables de entorno"""
    print_header("VERIFICACIÓN DE VARIABLES DE ENTORNO")
    
    # Variables críticas para funcionamiento
    critical_vars = {
        'MYSQL_HOST': 'Servidor de base de datos',
        'MYSQL_USER': 'Usuario de MySQL', 
        'MYSQL_PASSWORD': 'Contraseña de MySQL',
        'MYSQL_DATABASE': 'Nombre de base de datos',
        'WEBHOOK_VERIFY_TOKEN': 'Token de verificación webhook'
    }
    
    # Variables de Twilio (necesarias para producción)
    twilio_vars = {
        'TWILIO_ACCOUNT_SID': 'Account SID de Twilio',
        'TWILIO_AUTH_TOKEN': 'Auth Token de Twilio'
    }
    
    # Variables opcionales
    optional_vars = {
        'TWILIO_WHATSAPP_NUMBER': 'Número WhatsApp de Twilio',
        'PORT': 'Puerto del servidor'
    }
    
    print("\n📋 Variables Críticas:")
    critical_ok = True
    for var, desc in critical_vars.items():
        value = os.getenv(var)
        has_value = bool(value and value.strip())
        critical_ok = critical_ok and has_value
        
        if has_value and var == 'MYSQL_PASSWORD':
            display_value = "***CONFIGURADO***"
        elif has_value:
            display_value = value[:20] + "..." if len(value) > 20 else value
        else:
            display_value = "NO CONFIGURADO"
            
        print_status(f"{var}: {desc}", has_value, display_value)
    
    print("\n🔧 Variables de Twilio:")
    twilio_ok = True
    for var, desc in twilio_vars.items():
        value = os.getenv(var)
        has_value = bool(value and value.strip())
        twilio_ok = twilio_ok and has_value
        
        if has_value:
            display_value = "***CONFIGURADO***"
        else:
            display_value = "NO CONFIGURADO (configurar en Railway)"
            
        print_status(f"{var}: {desc}", has_value, display_value)
    
    print("\n⚙️ Variables Opcionales:")
    for var, desc in optional_vars.items():
        value = os.getenv(var)
        has_value = bool(value and value.strip())
        display_value = value if has_value else "Usará default"
        print_status(f"{var}: {desc}", True, display_value)
    
    return critical_ok, twilio_ok

def check_dependencies():
    """Verificar que las dependencias estén instaladas"""
    print_header("VERIFICACIÓN DE DEPENDENCIAS")
    
    required_packages = [
        'flask',
        'flask_cors', 
        'mysql.connector',
        'dotenv',
        'twilio',
        'requests'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            if package == 'mysql.connector':
                import mysql.connector
            elif package == 'flask_cors':
                import flask_cors
            else:
                __import__(package)
            print_status(f"Paquete {package}", True)
        except ImportError:
            print_status(f"Paquete {package}", False, "Instalar con: pip install -r requirements.txt")
            all_installed = False
    
    return all_installed

def check_app_structure():
    """Verificar estructura de la aplicación"""
    print_header("VERIFICACIÓN DE ESTRUCTURA DE APP")
    
    try:
        # Intentar importar y verificar funciones principales
        sys.path.append('.')
        import app_twilio
        
        # Verificar que existan las funciones principales
        functions_to_check = [
            'webhook',
            'procesar_mensaje_twilio', 
            'extraer_parametros_dialogflow',
            'procesar_intent'
        ]
        
        all_functions = True
        for func_name in functions_to_check:
            has_function = hasattr(app_twilio, func_name)
            all_functions = all_functions and has_function
            print_status(f"Función {func_name}()", has_function)
        
        return all_functions
        
    except Exception as e:
        print_status("Importar app_twilio.py", False, str(e))
        return False

def test_database_connection():
    """Probar conexión a base de datos"""
    print_header("VERIFICACIÓN DE BASE DE DATOS")
    
    try:
        from database import get_db_connection
        conn = get_db_connection()
        
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM productos")
            productos_count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            print_status("Conexión a MySQL", True, f"{productos_count} productos en catálogo")
            return True
        else:
            print_status("Conexión a MySQL", False, "No se pudo conectar")
            return False
            
    except Exception as e:
        print_status("Conexión a MySQL", False, str(e))
        return False

def generate_deployment_checklist():
    """Generar checklist para despliegue"""
    print_header("CHECKLIST PARA DESPLIEGUE EN RAILWAY")
    
    steps = [
        "1. Subir código a GitHub (git init, add, commit, push)",
        "2. Crear proyecto en Railway conectado al repo GitHub", 
        "3. Agregar servicio MySQL en Railway",
        "4. Configurar variables de entorno en Railway:",
        "   - Copiar variables de MySQL del servicio",
        "   - Agregar WEBHOOK_VERIFY_TOKEN=panaderia_jos_mar_2025",
        "   - Agregar TWILIO_ACCOUNT_SID (obtener de Twilio)",
        "   - Agregar TWILIO_AUTH_TOKEN (obtener de Twilio)",
        "5. Esperar el despliegue automático",
        "6. Probar endpoint: https://tu-app.railway.app/health",
        "7. Configurar webhook en Twilio WhatsApp Sandbox",
        "8. Probar integración desde WhatsApp"
    ]
    
    for step in steps:
        print(f"📋 {step}")

def main():
    print("🚀 VERIFICACIÓN DE PREPARACIÓN PARA TWILIO WHATSAPP")
    print("=" * 60)
    
    # Ejecutar todas las verificaciones
    files_ok = check_required_files()
    critical_ok, twilio_ok = check_environment_variables() 
    deps_ok = check_dependencies()
    app_ok = check_app_structure()
    db_ok = test_database_connection()
    
    # Resumen final
    print_header("RESUMEN FINAL")
    
    print_status("Archivos requeridos", files_ok)
    print_status("Variables críticas", critical_ok)
    print_status("Variables de Twilio", twilio_ok, "Configurar en Railway" if not twilio_ok else "")
    print_status("Dependencias instaladas", deps_ok)
    print_status("Estructura de app", app_ok)
    print_status("Conexión a base de datos", db_ok)
    
    # Determinar estado general
    ready_for_basic_deploy = files_ok and critical_ok and deps_ok and app_ok
    ready_for_twilio = ready_for_basic_deploy and twilio_ok
    
    print(f"\n{'='*60}")
    
    if ready_for_twilio:
        print("🎉 ¡TU APP ESTÁ COMPLETAMENTE LISTA PARA TWILIO WHATSAPP!")
        print("✅ Puedes proceder con el despliegue en Railway")
    elif ready_for_basic_deploy:
        print("⚠️  App lista para despliegue básico")
        print("🔧 Configura las variables de Twilio en Railway después del despliegue")
    else:
        print("❌ La app necesita correcciones antes del despliegue")
        
    print(f"{'='*60}")
    
    if ready_for_basic_deploy:
        generate_deployment_checklist()

if __name__ == "__main__":
    main()
