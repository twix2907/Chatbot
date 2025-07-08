# 🚀 GUÍA COMPLETA: CONFIGURAR DIALOGFLOW EN RAILWAY

## 📋 PASOS PARA CONFIGURAR DIALOGFLOW

### 1️⃣ **CREAR PROYECTO EN GOOGLE CLOUD**

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto:
   - Nombre: `panaderia-jos-mar-2025`
   - ID del proyecto: `panaderia-jos-mar-2025`
3. Activa las APIs necesarias:
   - Dialogflow ES API
   - Cloud Translation API (opcional)

### 2️⃣ **CREAR SERVICE ACCOUNT**

1. Ve a **IAM & Admin** → **Service Accounts**
2. Clic en **"Create Service Account"**
3. Configuración:
   - **Nombre:** `panaderia-dialogflow-service`
   - **Descripción:** `Service account para el chatbot de la panadería`
4. Asignar roles:
   - `Dialogflow API Client`
   - `Dialogflow API Admin`
   - `Dialogflow Console Agent Editor`

### 3️⃣ **DESCARGAR CREDENCIALES JSON**

1. En la Service Account creada, ve a **"Keys"**
2. Clic en **"Add Key"** → **"Create new key"**
3. Selecciona **JSON**
4. Descarga el archivo (ej: `panaderia-jos-mar-2025-abc123.json`)

### 4️⃣ **CONVERTIR CREDENCIALES PARA RAILWAY**

Ejecuta el script de conversión:
```bash
python convertir_credenciales_railway.py
```

El script te pedirá la ruta del archivo JSON y generará un archivo `credenciales_base64.txt`.

### 5️⃣ **CONFIGURAR VARIABLES EN RAILWAY**

1. Ve a tu proyecto en Railway
2. Clic en la pestaña **"Variables"**
3. Agrega estas variables:

```env
DIALOGFLOW_PROJECT_ID=panaderia-jos-mar-2025
DIALOGFLOW_LANGUAGE_CODE=es-ES
DIALOGFLOW_ENABLED=true
DIALOGFLOW_SESSION_ID=default-session
GOOGLE_APPLICATION_CREDENTIALS_JSON=contenido_del_archivo_credenciales_base64.txt
```

**⚠️ IMPORTANTE:** Para `GOOGLE_APPLICATION_CREDENTIALS_JSON`:
- Copia TODO el contenido del archivo `credenciales_base64.txt`
- Es una línea muy larga, asegúrate de copiarla completa
- No agregues espacios ni saltos de línea

### 6️⃣ **CREAR AGENTE EN DIALOGFLOW**

1. Ve a [Dialogflow Console](https://dialogflow.cloud.google.com/)
2. Crea un nuevo agente:
   - **Nombre:** `Panaderia Jos Mar`
   - **Proyecto:** `panaderia-jos-mar-2025`
   - **Idioma:** `Español - es`
   - **Zona horaria:** `(GMT-05:00) America/Lima`

### 7️⃣ **CREAR INTENTS EN DIALOGFLOW**

Crea estos intents básicos:

#### **Intent: Saludo**
- **Training phrases:**
  - "Hola"
  - "Buenos días"
  - "Buenas tardes"
  - "Hey"
  - "Hola, ¿cómo están?"

#### **Intent: Consultar Productos**
- **Training phrases:**
  - "¿Qué productos tienen?"
  - "Muéstrame el catálogo"
  - "¿Qué panes venden?"
  - "Productos disponibles"

#### **Intent: Realizar Pedido**
- **Training phrases:**
  - "Quiero 2 panes francés"
  - "Necesito una torta"
  - "Quisiera hacer un pedido"
  - "Pedir 3 empanadas"

### 8️⃣ **CONFIGURAR WEBHOOK EN DIALOGFLOW**

1. En Dialogflow Console, ve a **Fulfillment**
2. Activa **Webhook**
3. URL: `https://tu-app.railway.app/webhook`
4. Activa **"Enable webhook for all domains"`

### 9️⃣ **REDEPLEGAR EN RAILWAY**

1. Haz commit de los cambios:
```bash
git add .
git commit -m "Integrar Dialogflow"
git push origin main
```

2. Railway se redesplegaré automáticamente

### 🔟 **VERIFICAR CONFIGURACIÓN**

1. Ve a: `https://tu-app.railway.app/dialogflow-status`
2. Deberías ver:
```json
{
  "status": "ready",
  "dialogflow_active": true,
  "connection_test": "success"
}
```

---

## 🧪 **PRUEBAS**

### **Probar desde Dialogflow Console:**
1. Ve a Dialogflow Console
2. En el simulador, escribe: "Hola"
3. Deberías ver la respuesta de tu chatbot

### **Probar desde WhatsApp:**
1. Envía "Hola" a tu número de Twilio
2. El flujo será: WhatsApp → Twilio → Dialogflow → Tu App → Respuesta

---

## 🔧 **TROUBLESHOOTING**

### **Error de credenciales:**
- Verifica que el base64 esté completo
- Asegúrate de que la Service Account tenga los permisos correctos

### **Error de conexión:**
- Verifica que las APIs estén activadas en Google Cloud
- Comprueba que el PROJECT_ID sea correcto

### **No responde desde Dialogflow:**
- Verifica la URL del webhook en Dialogflow
- Revisa los logs en Railway

---

## ✅ **RESULTADO FINAL**

Tu chatbot tendrá:
- 🧠 **Procesamiento inteligente** con Dialogflow
- 🔄 **Fallback** al sistema local si Dialogflow falla
- 📱 **Integración completa** con WhatsApp via Twilio
- 🗄️ **Base de datos** para pedidos y logs
- 🚀 **Desplegado** en Railway

¡Tu panadería tendrá el chatbot más avanzado! 🥖🤖
