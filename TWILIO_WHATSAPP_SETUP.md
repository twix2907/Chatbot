# Configuración de Twilio WhatsApp para Panadería Jos & Mar

## 📋 Requisitos Previos

1. **Cuenta de Twilio activa** - [Registrarse en Twilio](https://www.twilio.com/try-twilio)
2. **Proyecto desplegado en Railway** - Ver `RAILWAY_SETUP.md`
3. **Número de teléfono validado** en Twilio

## 🔧 Paso 1: Configurar Twilio WhatsApp Sandbox

### 1.1 Acceder al Console de Twilio
1. Ir a [Twilio Console](https://console.twilio.com/)
2. Navegar a **Messaging > Try it out > Send a WhatsApp message**
3. O ir directamente a: `https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn`

### 1.2 Configurar el Sandbox
1. **Activar el número de WhatsApp Sandbox**:
   - Número sandbox: `+1 415 523 8886`
   - Enviar mensaje: `join <sandbox-keyword>` (ej: `join helpful-spider`)

2. **Configurar el Webhook URL**:
   - Ir a **Messaging > Settings > WhatsApp Sandbox Settings**
   - **Webhook URL**: `https://tu-app-railway.railway.app/webhook`
   - **HTTP Method**: `POST`
   - **Status Callback URL**: (opcional) `https://tu-app-railway.railway.app/status`

## 🔑 Paso 2: Obtener Credenciales de Twilio

### 2.1 Credenciales de Cuenta
1. En Twilio Console, ir a **Account > API Keys & Tokens**
2. Copiar estos valores:
   - **Account SID**: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **Auth Token**: `your_auth_token_here`

### 2.2 Número de WhatsApp
- **Sandbox Number**: `whatsapp:+14155238886`
- **Tu número activado**: Se muestra en la configuración del sandbox

## 🚀 Paso 3: Configurar Variables en Railway

### 3.1 Variables Requeridas
En Railway > Project > Variables, agregar:

```bash
# Twilio WhatsApp (REQUERIDO)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Webhook verification
WEBHOOK_VERIFY_TOKEN=panaderia_jos_mar_2025

# Base de datos (Ya configurado por Railway MySQL)
MYSQL_HOST=containers-us-west-xxx.railway.app
MYSQL_PORT=6543
MYSQL_USER=root
MYSQL_PASSWORD=tu-password-de-railway
MYSQL_DATABASE=railway

# Flask
FLASK_DEBUG=false
PORT=5000
```

### 3.2 Redeploy en Railway
Después de configurar las variables, Railway redesplegará automáticamente.

## 🧪 Paso 4: Probar la Integración

### 4.1 Verificar Webhook
1. **Probar endpoint**: `GET https://tu-app-railway.railway.app/health`
2. **Verificar logs**: Railway > Deployments > View Logs

### 4.2 Probar desde WhatsApp
1. **Activar sandbox**: Enviar `join helpful-spider` a `+1 415 523 8886`
2. **Enviar mensaje de prueba**: `productos`
3. **Verificar respuesta**: El bot debe responder con el catálogo

### 4.3 Comandos de Prueba
```
- productos -> Lista de productos
- precio pan -> Precio del pan
- hacer pedido -> Iniciar pedido
- mis pedidos -> Historial de pedidos
- ayuda -> Ayuda general
```

## 📊 Paso 5: Monitoreo y Debugging

### 5.1 Logs en Railway
```bash
# Ver logs en tiempo real
railway logs

# Filtrar por errores
railway logs | grep ERROR
```

### 5.2 Logs en Twilio
1. Ir a **Monitor > Logs > Messaging**
2. Filtrar por **WhatsApp** messages
3. Revisar **Webhook errors**

### 5.3 Endpoints de Debug
```bash
# Verificar estado de la app
GET https://tu-app-railway.railway.app/health

# Ver información del sistema
GET https://tu-app-railway.railway.app/info

# Probar conexión a BD
GET https://tu-app-railway.railway.app/test
```

## 🔒 Paso 6: Seguridad

### 6.1 Validación de Webhook
La app valida automáticamente:
- **Signature verification**: Usando `TWILIO_AUTH_TOKEN`
- **Token verification**: Usando `WEBHOOK_VERIFY_TOKEN`

### 6.2 Variables Sensibles
⚠️ **NUNCA** exponer en código:
- `TWILIO_AUTH_TOKEN`
- `MYSQL_PASSWORD`
- `WEBHOOK_VERIFY_TOKEN`

## 📱 Paso 7: Migración a Producción

### 7.1 Número de WhatsApp Propio
1. **Solicitar número**: Twilio > Phone Numbers > Buy a Number
2. **Activar WhatsApp**: Configurar WhatsApp para el número comprado
3. **Actualizar variables**: Cambiar `TWILIO_WHATSAPP_NUMBER`

### 7.2 Business Profile
1. **Crear perfil**: Twilio > Messaging > WhatsApp > Business Profile
2. **Configurar info**: Nombre, descripción, logo de la panadería
3. **Verificar negocio**: Proceso de verificación de WhatsApp

## 🆘 Troubleshooting

### Error: "Webhook validation failed"
- Verificar que `WEBHOOK_VERIFY_TOKEN` sea correcto
- Revisar que la URL del webhook sea accesible

### Error: "Failed to authenticate"
- Verificar `TWILIO_ACCOUNT_SID` y `TWILIO_AUTH_TOKEN`
- Asegurarse de que las credenciales sean válidas

### Error: "Database connection failed"
- Verificar variables de MySQL en Railway
- Comprobar que el servicio MySQL esté activo

### Mensajes no llegan
- Verificar que el número esté en el sandbox (desarrollo)
- Revisar logs de Twilio para errores de entrega
- Confirmar que el webhook esté configurado correctamente

### Respuestas no llegan
- Verificar logs de Railway por errores en el webhook
- Probar endpoint `/health` para verificar que la app esté activa
- Revisar formato de respuesta TwiML en logs

## 📞 Soporte

- **Twilio Docs**: https://www.twilio.com/docs/whatsapp
- **Railway Docs**: https://docs.railway.app/
- **Proyecto GitHub**: (configurar después del despliegue)

---

✅ **Estado**: Listo para configurar Twilio WhatsApp
🔧 **Próximo paso**: Obtener credenciales de Twilio y configurar variables en Railway
