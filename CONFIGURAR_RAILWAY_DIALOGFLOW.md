# 🚀 CONFIGURAR DIALOGFLOW EN RAILWAY

## 📋 VARIABLES DE ENTORNO NECESARIAS

### 1️⃣ **En Railway Dashboard:**

Ve a tu proyecto en Railway → **Variables** y agrega:

```env
# Dialogflow Configuration
DIALOGFLOW_PROJECT_ID=panaderia-jos-mar-2025
DIALOGFLOW_LANGUAGE_CODE=es-ES
DIALOGFLOW_ENABLED=true
DIALOGFLOW_SESSION_ID=default-session

# Google Credentials (JSON en base64)
GOOGLE_APPLICATION_CREDENTIALS_JSON=tu_json_completo_en_base64
```

### 2️⃣ **OBTENER EL JSON DE CREDENCIALES:**

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Selecciona tu proyecto de Dialogflow
3. Ve a **IAM & Admin** → **Service Accounts**
4. Crea una nueva Service Account o usa una existente
5. Descarga el archivo JSON de credenciales

### 3️⃣ **CONVERTIR JSON A BASE64:**

Usa el script que vamos a crear para convertir tu JSON a base64.

---

## 🔧 PASOS DETALLADOS:

### **PASO 1: Crear proyecto en Google Cloud**
1. Ve a https://console.cloud.google.com/
2. Crea un nuevo proyecto: `panaderia-jos-mar-2025`
3. Activa la API de Dialogflow

### **PASO 2: Crear Service Account**
1. Ve a IAM & Admin → Service Accounts
2. Clic en "Create Service Account"
3. Nombre: `panaderia-dialogflow-service`
4. Roles: 
   - Dialogflow API Client
   - Dialogflow API Admin

### **PASO 3: Descargar credenciales**
1. En la Service Account creada
2. Clic en "Keys" → "Add Key" → "Create new key"
3. Selecciona JSON
4. Descarga el archivo

### **PASO 4: Configurar en Railway**
Usa el script de conversión que crearemos.

---

## ⚠️ IMPORTANTE:

- **NUNCA** subas el archivo JSON al repositorio
- Usa variables de entorno en Railway
- El JSON se convierte a base64 para almacenarlo como variable
- Railway automáticamente lo decodificará en tu app

---

## 🧪 VERIFICACIÓN:

Después de configurar, prueba con:
```bash
curl https://tu-app.railway.app/dialogflow-status
```
