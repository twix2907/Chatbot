# 📋 VARIABLES PARA RAILWAY - DIALOGFLOW

## 🔧 VARIABLES QUE DEBES AGREGAR EN RAILWAY:

### 1️⃣ **Variables de Dialogflow:**
```
DIALOGFLOW_PROJECT_ID=panaderiajosymar
DIALOGFLOW_LANGUAGE_CODE=es-ES
DIALOGFLOW_ENABLED=true
DIALOGFLOW_SESSION_ID=default-session
```

### 2️⃣ **Credenciales de Google Cloud:**
```
GOOGLE_APPLICATION_CREDENTIALS_JSON=[contenido del archivo credenciales_base64.txt]
```

---

## 🚀 **PASOS PARA CONFIGURAR EN RAILWAY:**

### **PASO 1: Abrir Railway Dashboard**
1. Ve a https://railway.app/
2. Abre tu proyecto
3. Clic en la pestaña **"Variables"**

### **PASO 2: Agregar variables una por una**

**Variable 1:**
- Nombre: `DIALOGFLOW_PROJECT_ID`
- Valor: `panaderiajosymar`

**Variable 2:**
- Nombre: `DIALOGFLOW_LANGUAGE_CODE`
- Valor: `es-ES`

**Variable 3:**
- Nombre: `DIALOGFLOW_ENABLED`
- Valor: `true`

**Variable 4:**
- Nombre: `DIALOGFLOW_SESSION_ID`
- Valor: `default-session`

**Variable 5 (LA MÁS IMPORTANTE):**
- Nombre: `GOOGLE_APPLICATION_CREDENTIALS_JSON`
- Valor: [Copia TODO el contenido del archivo `credenciales_base64.txt`]

### **PASO 3: Verificar**
- Asegúrate de que todas las variables estén guardadas
- Railway se redesplegaré automáticamente

### **PASO 4: Probar**
- Ve a: `https://tu-app.railway.app/dialogflow-status`
- Deberías ver: `"status": "ready"`

---

## ⚠️ **MUY IMPORTANTE:**

### **Para GOOGLE_APPLICATION_CREDENTIALS_JSON:**
1. Abre el archivo `credenciales_base64.txt`
2. Copia **TODO** el contenido (es una línea muy larga)
3. Pégalo completo en Railway
4. **NO agregues espacios ni saltos de línea**

### **Ejemplo del contenido base64:**
```
eyJ0eXBlIjoic2VydmljZV9hY2NvdW50IiwicHJvamVjdF9pZCI6InBhbmFkZXJpYWpvc3ltYXIiLCJwcml2YXR...
```
(será mucho más largo)

---

## 🧪 **VERIFICACIÓN:**

Después de configurar todas las variables:

1. **Endpoint de verificación:**
   ```
   GET https://tu-app.railway.app/dialogflow-status
   ```

2. **Respuesta esperada:**
   ```json
   {
     "status": "ready",
     "dialogflow_active": true,
     "connection_test": "success",
     "project_id": "panaderiajosymar"
   }
   ```

3. **Si hay error:**
   - Revisa que todas las variables estén correctas
   - Verifica que el base64 esté completo
   - Consulta los logs de Railway

---

## 🎯 **SIGUIENTE PASO:**

Una vez configurado en Railway, tu chatbot usará:
- **Dialogflow** para mejor comprensión de lenguaje
- **Fallback** al sistema local si Dialogflow falla
- **Todas las funcionalidades** actuales de tu panadería

¡Tu chatbot será mucho más inteligente! 🧠🥖
