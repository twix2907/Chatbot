# Panadería Jos & Mar - Backend WhatsApp Bot

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
   .venv\Scripts\activate  # Windows
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
