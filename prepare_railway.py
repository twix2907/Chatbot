#!/usr/bin/env python3
"""
Script para preparar el proyecto para despliegue en Railway
"""
import os
import subprocess
import json

def verificar_archivos_necesarios():
    print("🔍 VERIFICANDO ARCHIVOS NECESARIOS PARA RAILWAY")
    print("=" * 50)
    
    archivos_requeridos = {
        "app.py": "Webhook principal de Flask",
        "requirements.txt": "Dependencias de Python", 
        "Procfile": "Comando de inicio para Railway",
        ".env.example": "Ejemplo de variables de entorno",
        "README.md": "Documentación del proyecto",
        "database.py": "Gestor de base de datos"
    }
    
    archivos_faltantes = []
    
    for archivo, descripcion in archivos_requeridos.items():
        if os.path.exists(archivo):
            print(f"✅ {archivo} - {descripcion}")
        else:
            print(f"❌ {archivo} - {descripcion} (FALTANTE)")
            archivos_faltantes.append(archivo)
    
    return archivos_faltantes

def crear_archivo_env_example():
    print("\n📝 CREANDO .env.example")
    
    env_example_content = """# VARIABLES DE ENTORNO PARA RAILWAY
# ===================================

# Base de datos MySQL (Railway las proporciona automáticamente)
DB_HOST=containers-us-west-xxx.railway.app
DB_PORT=6543
DB_NAME=railway
DB_USER=root
DB_PASSWORD=tu-password-de-railway

# Token de verificación para WhatsApp
WEBHOOK_VERIFY_TOKEN=panaderia_jos_mar_2025

# Puerto (Railway lo asigna automáticamente)
PORT=5000

# Configuración de Flask
FLASK_ENV=production
FLASK_DEBUG=false

# WhatsApp Configuration (Meta Cloud API)
WHATSAPP_TOKEN=tu-token-de-meta
WHATSAPP_PHONE_NUMBER_ID=tu-phone-number-id

# Twilio Configuration (Alternativo)
TWILIO_ACCOUNT_SID=tu-twilio-sid
TWILIO_AUTH_TOKEN=tu-twilio-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
"""
    
    with open(".env.example", "w", encoding="utf-8") as f:
        f.write(env_example_content)
    
    print("✅ .env.example creado")

def actualizar_app_para_railway():
    print("\n🔧 ACTUALIZANDO app.py PARA RAILWAY")
    
    # Leer el archivo actual
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Verificar si ya tiene las configuraciones de Railway
    if "PORT" in content and "0.0.0.0" in content:
        print("✅ app.py ya está configurado para Railway")
        return
    
    # Agregar configuración de puerto para Railway
    railway_config = """
# Configuración para Railway
port = int(os.getenv('PORT', 5000))
"""
    
    # Actualizar la línea de app.run
    content = content.replace(
        "app.run(debug=True)",
        "app.run(host='0.0.0.0', port=port, debug=False)"
    )
    
    # Agregar configuración de puerto después de los imports
    if "port = int(os.getenv('PORT', 5000))" not in content:
        import_end = content.find("from database import DatabaseManager")
        if import_end != -1:
            next_line = content.find("\n", import_end) + 1
            content = content[:next_line] + railway_config + content[next_line:]
    
    with open("app.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ app.py actualizado para Railway")

def crear_railway_json():
    print("\n📋 CREANDO railway.json")
    
    railway_config = {
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "gunicorn app:app",
            "healthcheckPath": "/health",
            "healthcheckTimeout": 300,
            "restartPolicyType": "ON_FAILURE"
        }
    }
    
    with open("railway.json", "w", encoding="utf-8") as f:
        json.dump(railway_config, f, indent=2)
    
    print("✅ railway.json creado")

def verificar_git():
    print("\n🔧 VERIFICANDO CONFIGURACIÓN DE GIT")
    
    try:
        # Verificar si git está inicializado
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository ya está inicializado")
            return True
        else:
            return False
    except FileNotFoundError:
        print("❌ Git no está instalado o no está en PATH")
        return False

def inicializar_git():
    print("\n🚀 INICIALIZANDO GIT REPOSITORY")
    
    try:
        # Crear .gitignore si no existe
        if not os.path.exists(".gitignore"):
            gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
env.bak/
venv.bak/

# Environment variables
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Database
*.db
*.sqlite

# Railway
.railway/
"""
            with open(".gitignore", "w", encoding="utf-8") as f:
                f.write(gitignore_content)
            print("✅ .gitignore creado")
        
        # Inicializar git
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit - Panadería Jos & Mar Chatbot"], check=True)
        
        print("✅ Git repository inicializado")
        print("💡 Próximo paso: crear repositorio en GitHub y hacer push")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error configurando git: {e}")

def mostrar_pasos_finales():
    print("\n" + "="*60)
    print("🎯 PROYECTO LISTO PARA RAILWAY!")
    print("="*60)
    print("\n📋 PRÓXIMOS PASOS:")
    print("\n1️⃣ SUBIR A GITHUB:")
    print("   • Crear repositorio en github.com")
    print("   • git remote add origin https://github.com/tu-usuario/panaderia-chatbot")
    print("   • git push -u origin main")
    
    print("\n2️⃣ DESPLEGAR EN RAILWAY:")
    print("   • Ve a railway.app")
    print("   • New Project > Deploy from GitHub")
    print("   • Selecciona tu repositorio")
    print("   • Agrega servicio MySQL")
    
    print("\n3️⃣ CONFIGURAR VARIABLES:")
    print("   • Copia credenciales de MySQL de Railway")
    print("   • Agrega variables de entorno en Railway")
    print("   • Usa .env.example como referencia")
    
    print("\n4️⃣ CONFIGURAR WHATSAPP:")
    print("   • Meta Developers > WhatsApp > Webhook")
    print("   • URL: https://tu-app.up.railway.app/webhook")
    print("   • Verify Token: panaderia_jos_mar_2025")
    
    print("\n5️⃣ PROBAR:")
    print("   • https://tu-app.up.railway.app/health")
    print("   • Enviar mensaje de WhatsApp")
    print("   • Verificar logs en Railway")
    
    print(f"\n🎉 ¡Tu chatbot estará live en Railway!")

def main():
    print("🚀 PREPARACIÓN PARA RAILWAY - PANADERÍA JOS & MAR")
    print("="*60)
    
    # 1. Verificar archivos
    archivos_faltantes = verificar_archivos_necesarios()
    
    # 2. Crear archivos faltantes
    if ".env.example" in archivos_faltantes or not os.path.exists(".env.example"):
        crear_archivo_env_example()
    
    # 3. Actualizar app.py
    actualizar_app_para_railway()
    
    # 4. Crear railway.json
    crear_railway_json()
    
    # 5. Configurar git
    if not verificar_git():
        respuesta = input("\n¿Inicializar git repository? (y/n): ")
        if respuesta.lower() == 'y':
            inicializar_git()
    
    # 6. Mostrar pasos finales
    mostrar_pasos_finales()

if __name__ == "__main__":
    main()
