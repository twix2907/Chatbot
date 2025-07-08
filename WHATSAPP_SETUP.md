# Configuración para WhatsApp Business
# ==================================

# 1. NGROK (Para desarrollo local)
# Descargar desde: https://ngrok.com/download
# Instalar y ejecutar: ngrok http 5000
# Esto te dará una URL pública como: https://abc123.ngrok.io

# 2. DIALOGFLOW CONFIGURATION
# ===========================
# En tu proyecto de Dialogflow:
# - Ve a Integrations → WhatsApp
# - O usa Webhooks para conectar directamente

# 3. WHATSAPP BUSINESS API
# ========================
# Opciones disponibles:

# OPCIÓN A: Twilio WhatsApp (Más fácil para empezar)
# --------------------------------------------------
# 1. Crear cuenta en Twilio.com
# 2. Ir a Console → WhatsApp → Senders
# 3. Configurar webhook URL: https://tu-url.ngrok.io/webhook
# 4. El teléfono vendrá en formato: "whatsapp:+51987654321"

# OPCIÓN B: Meta WhatsApp Cloud API (Gratuito)
# --------------------------------------------
# 1. Crear cuenta de desarrollador en developers.facebook.com
# 2. Crear app de WhatsApp Business
# 3. Configurar webhook URL: https://tu-url.ngrok.io/webhook
# 4. Obtener token de acceso y configurar

# OPCIÓN C: WhatsApp Business API (Empresarial)
# ---------------------------------------------
# Requiere aprobación de Meta y proveedor oficial

# 4. VARIABLES DE ENTORNO NECESARIAS
# ==================================
# Agregar a tu archivo .env:

# Para Twilio:
# TWILIO_ACCOUNT_SID=tu_account_sid
# TWILIO_AUTH_TOKEN=tu_auth_token
# TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Para Meta WhatsApp:
# WHATSAPP_TOKEN=tu_token_de_acceso
# WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id
# WHATSAPP_VERIFY_TOKEN=tu_verify_token

# Para Dialogflow:
# GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
# DIALOGFLOW_PROJECT_ID=tu_project_id

# 5. PASOS PARA CONFIGURAR
# ========================

# PASO 1: Exponer tu webhook localmente
# ngrok http 5000

# PASO 2: Configurar Dialogflow
# - Crear proyecto en console.dialogflow.com
# - Importar intents y entities
# - Configurar webhook: https://tu-url.ngrok.io/webhook

# PASO 3: Configurar WhatsApp
# - Elegir proveedor (Twilio/Meta)
# - Configurar número de WhatsApp
# - Conectar con Dialogflow

# PASO 4: Probar
# - Enviar mensaje a tu número de WhatsApp
# - Verificar que llegue al webhook
# - Verificar respuesta del bot

# 6. NÚMEROS DE PRUEBA
# ====================
# Twilio: +1 415 523 8886 (sandbox)
# Meta: Configurar número de prueba en dashboard

# 7. COMANDOS ÚTILES
# ==================
# Iniciar servidor: python app.py
# Exponer con ngrok: ngrok http 5000
# Ver logs: tail -f logs/webhook.log
