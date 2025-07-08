# 🚀 GUÍA: USAR TWILIO WHATSAPP CON TU CHATBOT
# ============================================

## ✅ VENTAJAS DE TWILIO SOBRE META
- ✅ No necesita validación de negocio
- ✅ Setup en 5 minutos
- ✅ Sandbox gratuito para pruebas
- ✅ Sin problemas de redirección
- ✅ Excelente documentación

## 📋 PASOS PARA CONFIGURAR TWILIO

### 1️⃣ CREAR CUENTA TWILIO
1. Ve a: https://www.twilio.com
2. Click "Try Twilio for free"
3. Completa registro:
   - Email
   - Nombre completo
   - Número de teléfono (verificación)
4. Verifica tu número con el código SMS

### 2️⃣ CONFIGURAR WHATSAPP SANDBOX
1. En Twilio Console, navega a:
   ```
   Develop > Messaging > Try it out > Send a WhatsApp message
   ```

2. Verás instrucciones como:
   ```
   To use your sandbox:
   1. Join sandbox by sending: join <palabra-código>
   2. To: whatsapp:+1415238886
   ```

3. Desde tu WhatsApp personal:
   - Agrega contacto: +1 415 238 886
   - Envía mensaje: join <tu-palabra-código>
   - Ejemplo: "join autumn-cloud"

### 3️⃣ CONFIGURAR WEBHOOK EN TWILIO
1. En la misma página de sandbox, busca "Sandbox Configuration"
2. Configura:
   ```
   When a message comes in:
   https://tu-proyecto.up.railway.app/webhook
   
   HTTP Method: POST
   ```
3. Click "Save"

### 4️⃣ ACTUALIZAR TU APP PARA TWILIO
Tu app ya está lista, pero vamos a agregar mejor soporte para Twilio.

## 🔧 VARIABLES NECESARIAS PARA TWILIO

Para Railway, solo necesitas estas variables mínimas:

```
# Base de datos MySQL (Railway las proporciona)
MYSQL_HOST=<railway-host>
MYSQL_PORT=<railway-port>
MYSQL_USER=root
MYSQL_PASSWORD=<railway-password>
MYSQL_DATABASE=railway

# Webhook verification
WEBHOOK_VERIFY_TOKEN=panaderia_jos_mar_2025

# Flask config
FLASK_DEBUG=false
```

## 📱 TESTING CON TWILIO

### Flujo de prueba:
1. **Saludo:**
   ```
   Tú: Hola
   Bot: 🥖 ¡Hola! Bienvenido a la Panadería Jos & Mar...
   ```

2. **Consultar productos:**
   ```
   Tú: ¿Qué productos tienen?
   Bot: 🥖 PRODUCTOS DISPONIBLES - PANADERÍA JOS & MAR...
   ```

3. **Hacer pedido:**
   ```
   Tú: Quiero 2 francés y 1 torta de chocolate
   Bot: ✅ ¡Pedido #X registrado! Total: S/35.60...
   ```

## 🎯 PRÓXIMO PASO: DESPLEGAR EN RAILWAY

¿Quieres que procedamos a:
1. Subir código a GitHub
2. Desplegar en Railway
3. Configurar Twilio WhatsApp
4. ¡Probar tu chatbot!

## 💡 NOTA SOBRE COSTOS TWILIO

- **Sandbox**: Completamente GRATIS
- **Producción**: ~$0.005 por mensaje (muy barato)
- **Número dedicado**: ~$1/mes (opcional)

¡Twilio es perfecto para empezar y escalar después!
