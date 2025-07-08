#!/usr/bin/env python3
"""
Script para preparar el proyecto para subir a GitHub
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=".")
        if result.returncode == 0:
            print(f"✅ {description} - Exitoso")
            if result.stdout.strip():
                print(f"   📋 {result.stdout.strip()}")
        else:
            print(f"❌ {description} - Error")
            if result.stderr.strip():
                print(f"   ⚠️  {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {description} - Error: {str(e)}")
        return False

def check_git_status():
    """Verificar estado de git"""
    print("🔍 VERIFICANDO ESTADO DE GIT")
    print("=" * 50)
    
    # Verificar si git está instalado
    if not run_command("git --version", "Verificar instalación de git"):
        print("❌ Git no está instalado. Instalar desde: https://git-scm.com/")
        return False
    
    # Verificar si ya hay un repositorio
    if os.path.exists(".git"):
        print("✅ Repositorio git ya existe")
        run_command("git status", "Estado del repositorio")
        return True
    else:
        print("ℹ️  No hay repositorio git inicializado")
        return False

def create_gitignore():
    """Crear archivo .gitignore"""
    print("📝 Creando .gitignore")
    
    gitignore_content = """# Variables de entorno
.env
.env.local
.env.production

# Virtual environment
.venv/
venv/
env/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

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
logs/

# Database
*.db
*.sqlite3

# Temporary files
*.tmp
*.temp
temp/

# Google Cloud credentials (si los usas)
credentials.json
service-account-key.json

# Jupyter Notebooks
.ipynb_checkpoints

# Testing
.pytest_cache/
.coverage
htmlcov/
"""
    
    try:
        with open(".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore_content)
        print("✅ .gitignore creado")
        return True
    except Exception as e:
        print(f"❌ Error creando .gitignore: {str(e)}")
        return False

def create_readme():
    """Crear README.md para GitHub"""
    print("📝 Creando README.md")
    
    readme_content = """# Panadería Jos & Mar - Backend WhatsApp Bot

🍞 Backend Flask para chatbot de pedidos de panadería integrado con WhatsApp vía Twilio.

## 🚀 Características

- **WhatsApp Integration**: Usando Twilio WhatsApp API
- **Gestión de Pedidos**: Sistema completo de pedidos con múltiples productos
- **Base de Datos**: MySQL con catálogo de productos y historial de pedidos
- **NLP**: Procesamiento de texto libre para extraer productos y cantidades
- **Logging**: Registro completo de conversaciones
- **Railway Ready**: Configurado para despliegue en Railway

## 📋 Funcionalidades

### Para Clientes (vía WhatsApp):
- 📱 Consultar productos disponibles
- 💰 Consultar precios
- 🛒 Realizar pedidos con múltiples productos
- 📊 Consultar historial de pedidos
- ❓ Ayuda y soporte

### Para la Panadería:
- 📈 Registro automático de clientes
- 🗄️ Gestión de pedidos en base de datos
- 📝 Logs de todas las conversaciones
- 📊 Historial completo de pedidos

## 🛠️ Tecnologías

- **Backend**: Flask (Python)
- **Base de Datos**: MySQL
- **WhatsApp**: Twilio API
- **NLP**: Procesamiento de texto personalizado
- **Deployment**: Railway
- **Environment**: Python 3.8+

## 📦 Instalación Local

1. **Clonar repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/panaderia-backend.git
   cd panaderia-backend
   ```

2. **Crear virtual environment**:
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:
   ```bash
   cp .env.example .env
   # Editar .env con tus credenciales
   ```

5. **Ejecutar aplicación**:
   ```bash
   python app_twilio.py
   ```

## 🚀 Despliegue en Railway

1. **Crear proyecto en Railway**
2. **Conectar repositorio de GitHub**
3. **Agregar MySQL service**
4. **Configurar variables de entorno**
5. **Configurar webhook en Twilio**

Ver `TWILIO_WHATSAPP_SETUP.md` para instrucciones detalladas.

## 🔧 Configuración

### Variables de Entorno Requeridas:
- `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`
- `WEBHOOK_VERIFY_TOKEN`

### Scripts Útiles:
- `verificar_twilio_ready.py`: Verificar que todo esté configurado
- `test_twilio_connection.py`: Probar conexión con Twilio
- `mostrar_variables.py`: Revisar variables de entorno

## 📱 Uso

1. **Activar Twilio WhatsApp Sandbox**:
   - Enviar `join helpful-spider` a `+1 415 523 8886`

2. **Comandos disponibles**:
   - `productos` - Ver catálogo completo
   - `precio [producto]` - Consultar precio específico
   - `hacer pedido` - Iniciar nuevo pedido
   - `mis pedidos` - Ver historial
   - `ayuda` - Obtener ayuda

## 🗄️ Base de Datos

### Tablas:
- `clientes`: Información de clientes
- `productos`: Catálogo de productos (25 productos)
- `pedidos`: Pedidos realizados
- `pedido_detalle`: Detalles de cada pedido
- `chat_logs`: Logs de conversaciones

## 📝 Documentación

- `TWILIO_WHATSAPP_SETUP.md`: Configuración completa de Twilio
- `RAILWAY_SETUP.md`: Guía de despliegue en Railway
- `ESTADO_ACTUAL.md`: Estado actual del proyecto

## 🤝 Contribuir

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📞 Contacto

**Panadería Jos & Mar**
- WhatsApp: A través del bot implementado
- Desarrollado para: Gestión automatizada de pedidos

---

⚡ **Powered by**: Flask + Twilio + Railway + MySQL

🍞 **Hecho con amor para la mejor panadería del barrio**
"""
    
    try:
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        print("✅ README.md creado")
        return True
    except Exception as e:
        print(f"❌ Error creando README.md: {str(e)}")
        return False

def initialize_git():
    """Inicializar repositorio git"""
    print("\n🔧 INICIALIZANDO GIT")
    print("=" * 50)
    
    steps = [
        ("git init", "Inicializar repositorio git"),
        ("git add .", "Agregar todos los archivos"),
        ("git commit -m 'Initial commit: Panadería Jos & Mar Backend - Twilio WhatsApp Bot'", "Crear commit inicial")
    ]
    
    for command, description in steps:
        if not run_command(command, description):
            return False
    
    print("\n✅ Git inicializado correctamente")
    return True

def show_next_steps():
    """Mostrar próximos pasos"""
    print("\n📋 PRÓXIMOS PASOS")
    print("=" * 50)
    
    steps = [
        "1. 🌐 Crear repositorio en GitHub:",
        "   - Ir a https://github.com/new",
        "   - Nombre: panaderia-backend",
        "   - Descripción: Backend Flask para chatbot WhatsApp de panadería",
        "   - Público o Privado (tu elección)",
        "   - NO inicializar con README (ya lo tenemos)",
        "",
        "2. 📤 Conectar y subir código:",
        "   git remote add origin https://github.com/TU-USUARIO/panaderia-backend.git",
        "   git branch -M main",
        "   git push -u origin main",
        "",
        "3. 🚀 Desplegar en Railway:",
        "   - Ir a https://railway.app/new",
        "   - Connect to GitHub repository",
        "   - Seleccionar tu repositorio",
        "   - Agregar MySQL service",
        "   - Configurar variables de entorno",
        "",
        "4. 📱 Configurar Twilio WhatsApp:",
        "   - Webhook URL: https://tu-app.railway.app/webhook",
        "   - Probar con WhatsApp Sandbox",
        "",
        "Variables de Twilio para Railway:",
        "TWILIO_ACCOUNT_SID=TU_ACCOUNT_SID_AQUI",
        "TWILIO_AUTH_TOKEN=TU_AUTH_TOKEN_AQUI",
        "WEBHOOK_VERIFY_TOKEN=panaderia_jos_mar_2025"
    ]
    
    for step in steps:
        print(step)

def main():
    print("🚀 PREPARACIÓN PARA GITHUB")
    print("=" * 50)
    
    # Verificar estado de git
    git_exists = check_git_status()
    
    # Crear archivos necesarios
    gitignore_ok = create_gitignore()
    readme_ok = create_readme()
    
    if not git_exists:
        # Inicializar git
        git_ok = initialize_git()
        if not git_ok:
            print("❌ Error inicializando git")
            return
    
    # Mostrar próximos pasos
    show_next_steps()
    
    print(f"\n{'='*50}")
    print("🎉 ¡PROYECTO PREPARADO PARA GITHUB!")
    print("✅ .gitignore creado")
    print("✅ README.md creado")
    print("✅ Git inicializado")
    print("✅ Commit inicial creado")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
