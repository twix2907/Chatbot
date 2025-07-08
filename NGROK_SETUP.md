# INSTALACIÓN Y CONFIGURACIÓN DE NGROK PARA WHATSAPP
# ==================================================

# 1. DESCARGAR NGROK
# ------------------
# Ve a: https://ngrok.com/download
# Descarga ngrok para Windows
# Extrae el archivo ngrok.exe

# 2. INSTALAR NGROK (OPCIONAL - USANDO CHOCOLATEY)
# ------------------------------------------------
# Si tienes Chocolatey instalado:
# choco install ngrok

# O usando winget:
# winget install ngrok

# 3. CONFIGURAR NGROK
# -------------------
# 1. Regístrate en ngrok.com (gratis)
# 2. Obtén tu authtoken desde el dashboard
# 3. Ejecuta: ngrok authtoken TU_TOKEN_AQUI

# 4. EXPONER TU WEBHOOK
# ---------------------
# Ejecutar en una terminal separada:
# ngrok http 5000

# Esto te dará una URL como:
# https://abc123.ngrok.io

# 5. CONFIGURAR EN DIALOGFLOW
# ---------------------------
# 1. Ve a tu proyecto en console.dialogflow.com
# 2. Ve a Fulfillment
# 3. Habilita Webhook
# 4. URL: https://tu-url.ngrok.io/webhook
# 5. Guarda

# 6. CONFIGURAR WHATSAPP
# ----------------------

# OPCIÓN A: TWILIO WHATSAPP (RECOMENDADO PARA EMPEZAR)
# ----------------------------------------------------
# 1. Crea cuenta en twilio.com
# 2. Ve a Console > Develop > Messaging > Try it out > Send a WhatsApp message
# 3. Únete al sandbox de WhatsApp siguiendo las instrucciones
# 4. En Sandbox settings, configura:
#    - Webhook URL: https://tu-url.ngrok.io/webhook
#    - HTTP Method: POST
# 5. Prueba enviando un mensaje al número de Twilio

# OPCIÓN B: META WHATSAPP CLOUD API (GRATUITO)
# --------------------------------------------
# 1. Ve a developers.facebook.com
# 2. Crea una app de WhatsApp Business
# 3. Configura webhook: https://tu-url.ngrok.io/webhook
# 4. Token de verificación: panaderia_jos_mar_2025
# 5. Suscríbete a eventos de mensajes

# 7. PRUEBAS
# ----------
# 1. Envía mensaje de WhatsApp al número configurado
# 2. Verifica que llegue a tu webhook
# 3. Revisa los logs en la consola

# 8. COMANDOS PARA TESTING
# ------------------------
# Terminal 1: python app.py
# Terminal 2: ngrok http 5000
# Terminal 3: Monitorear logs

# 9. PARA PRODUCCIÓN
# ------------------
# - Usar Railway, Heroku, o servidor VPS
# - Configurar dominio propio
# - Usar certificado SSL válido
