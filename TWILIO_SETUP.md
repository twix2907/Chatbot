# 🚀 GUÍA RÁPIDA: WHATSAPP CON TWILIO (MÁS FÁCIL)
# ===============================================

## ¿POR QUÉ EMPEZAR CON TWILIO?
- ✅ No requiere validación de negocio
- ✅ Setup en 5 minutos
- ✅ Sandbox gratuito para pruebas
- ✅ Sin problemas de redirección
- ✅ Perfecto para testing inicial

## 📋 PASOS PARA TWILIO WHATSAPP

### 1️⃣ CREAR CUENTA TWILIO
1. Ve a: https://www.twilio.com
2. Click "Sign up for free"
3. Completa el registro con tu teléfono
4. Verifica tu número

### 2️⃣ CONFIGURAR WHATSAPP SANDBOX
1. En Twilio Console, ve a:
   - Develop > Messaging > Try it out > Send a WhatsApp message
2. Verás algo como:
   ```
   Join sandbox: whatsapp:+1415238886
   Send: join <código-único>
   ```
3. Desde tu WhatsApp personal:
   - Envía mensaje a +1415238886
   - Escribe: join followed-cat (o tu código)

### 3️⃣ CONFIGURAR WEBHOOK
1. En Twilio Console > WhatsApp sandbox settings
2. Configura:
   ```
   Webhook URL: https://tu-proyecto.up.railway.app/webhook
   HTTP Method: POST
   ```
3. Click "Save"

### 4️⃣ PROBAR TU CHATBOT
1. Desde tu WhatsApp, envía al número Twilio:
   ```
   Hola
   ```
2. Deberías recibir respuesta de tu bot:
   ```
   🥖 ¡Hola! Bienvenido a la Panadería Jos & Mar...
   ```

### 5️⃣ PROBAR PEDIDOS
```
Tú: "Quiero 2 francés y 1 torta de chocolate"
Bot: "✅ ¡Pedido #X registrado! Total: S/35.60..."
```

## 🔧 PREPARAR RAILWAY PRIMERO

Antes de configurar WhatsApp, asegurémonos que Railway funcione:

### A. Subir a GitHub:
```bash
git add .
git commit -m "Chatbot listo para Railway"
git remote add origin https://github.com/TU-USUARIO/panaderia-chatbot.git
git push -u origin main
```

### B. Desplegar en Railway:
1. railway.app > New Project > Deploy from GitHub
2. Conectar repositorio
3. Agregar MySQL service
4. Configurar variables de entorno

### C. Probar endpoints:
```
https://tu-proyecto.up.railway.app/health
https://tu-proyecto.up.railway.app/info
```

## 📱 SCRIPT DE VERIFICACIÓN

Crea este archivo para probar tu deployment:
