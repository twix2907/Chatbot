# 🤖 INTEGRACIÓN CON DIALOGFLOW - PANADERÍA JOS & MAR

## 📋 PASOS PARA INTEGRAR DIALOGFLOW

### 1️⃣ CREAR PROYECTO EN GOOGLE CLOUD
1. Ve a: https://console.cloud.google.com/
2. Crea un nuevo proyecto: `panaderia-jos-mar-chatbot`
3. Habilita la API de Dialogflow ES
4. Crea credenciales de servicio (JSON)

### 2️⃣ CONFIGURAR DIALOGFLOW CONSOLE
1. Ve a: https://dialogflow.cloud.google.com/
2. Crea un nuevo agente
3. Nombre: `Panaderia Jos Mar Bot`
4. Proyecto: selecciona el que creaste
5. Idioma: Español (es)

### 3️⃣ CREAR INTENTS EN DIALOGFLOW

#### Intent: Saludo
- **Training phrases:**
  - Hola
  - Buenos días
  - Buenas tardes
  - Hey
  - Hi
  - Saludos

#### Intent: Consultar Productos
- **Training phrases:**
  - Qué productos tienen
  - Muéstrame el catálogo
  - Productos disponibles
  - Qué venden
  - Menu
  - Carta

#### Intent: Realizar Pedido
- **Training phrases:**
  - Quiero 2 panes francés
  - Necesito 3 empanadas
  - Deseo ordenar 1 baguette
  - Pedir 2 tortas
- **Entities:**
  - @numero: cantidad
  - @producto: nombre del producto

#### Intent: Consultar Precios
- **Training phrases:**
  - Cuánto cuesta el pan francés
  - Precio del baguette
  - Qué precio tiene
  - Cuánto vale

#### Intent: Consultar Pedidos
- **Training phrases:**
  - Mis pedidos
  - Historial de pedidos
  - Pedidos anteriores
  - Mis compras

### 4️⃣ CONFIGURAR WEBHOOK
En Dialogflow Console:
1. Ve a Fulfillment
2. Habilita Webhook
3. URL: `https://chatbot-production-ec53.up.railway.app/webhook`
4. Habilita para todos los intents

### 5️⃣ INTEGRAR CON TWILIO
En Twilio Console:
1. Ve a Phone Numbers → Manage → WhatsApp senders
2. Webhook URL: `URL_DE_DIALOGFLOW_WEBHOOK`
3. HTTP Method: POST

---

## 📁 ARCHIVOS NECESARIOS

### requirements.txt (agregar)
```
google-cloud-dialogflow==2.21.0
```

### .env (agregar)
```
DIALOGFLOW_PROJECT_ID=panaderia-jos-mar-chatbot
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
```

---

## 🔧 CONFIGURACIÓN DE CÓDIGO

El código actual ya está preparado para Dialogflow. Solo necesitas:

1. **Configurar las variables de entorno**
2. **Subir las credenciales de Google Cloud**
3. **Crear los intents en Dialogflow**
4. **Configurar el webhook en Dialogflow**

---

## 🎯 VENTAJAS DE USAR DIALOGFLOW

✅ **Mejor comprensión de lenguaje natural**
✅ **Manejo automático de sinónimos**
✅ **Extracción de entidades mejorada**
✅ **Conversaciones más fluidas**
✅ **Soporte para múltiples idiomas**
✅ **Análisis de sentimientos**
✅ **Integración con Google Assistant**

---

## 🚀 SIGUIENTE PASO

¿Quieres que configure el código para usar Dialogflow como opción principal?
