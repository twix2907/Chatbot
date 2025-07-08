# 📱 GUÍA PARA PROBAR DESDE WHATSAPP

## 🎯 TU APP ESTÁ LISTA
✅ **URL de tu webhook:** `https://chatbot-production-ec53.up.railway.app/webhook`
✅ **Estado:** Funcionando correctamente
✅ **Base de datos:** Conectada
✅ **Catálogo de productos:** Cargado

---

## 🔧 PASO 1: CONFIGURAR TWILIO WEBHOOK

### 1.1 Ir a la consola de Twilio
1. Abre tu navegador y ve a: https://console.twilio.com/
2. Inicia sesión con tu cuenta

### 1.2 Configurar el webhook
1. Ve a **Messaging** → **Try it out** → **Send a WhatsApp message**
2. En la sección **"Webhook configuration for Sandbox"**:
   - **Webhook URL:** `https://chatbot-production-ec53.up.railway.app/webhook`
   - **HTTP Method:** `POST`
   - **Content-Type:** `application/x-www-form-urlencoded`
3. Haz clic en **"Save Configuration"**

---

## 📱 PASO 2: ACTIVAR TU TELÉFONO EN EL SANDBOX

### 2.1 Unirse al sandbox
1. Desde tu teléfono, abre WhatsApp
2. Agrega el número: **+1 (415) 523-8886** a tus contactos
3. Envía el mensaje: **`join helpful-spider`**
4. Espera a recibir el mensaje de confirmación de Twilio

### 2.2 Confirmación exitosa
Deberías recibir un mensaje como:
```
✅ Your sandbox is now connected! 
You can now send messages to this number.
```

---

## 🧪 PASO 3: PROBAR EL CHATBOT

### 3.1 Comandos básicos para probar:

#### Saludo inicial
```
hola
```
**Respuesta esperada:** Mensaje de bienvenida con opciones

#### Ver catálogo de productos
```
productos
```
**Respuesta esperada:** Lista completa de productos con precios

#### Hacer un pedido
```
quiero 2 francés
```
**Respuesta esperada:** Confirmación del pedido

#### Múltiples productos
```
quiero 1 baguette y 3 ciabatti
```

#### Consultar historial
```
mi historial
```

#### Ayuda
```
ayuda
```

### 3.2 Ejemplos de conversación completa:

**Usuario:** `hola`
**Bot:** 🥖 ¡Hola! Bienvenido a la Panadería Jos & Mar...

**Usuario:** `productos`
**Bot:** 🥖 **PRODUCTOS DISPONIBLES - PANADERÍA JOS & MAR**...

**Usuario:** `quiero 2 francés y 1 baguette`
**Bot:** 🛒 **RESUMEN DE TU PEDIDO:**...

---

## 🔍 PASO 4: VERIFICAR QUE TODO FUNCIONA

### 4.1 Indicadores de éxito:
- ✅ Recibes respuesta inmediata del bot
- ✅ Las respuestas están en español
- ✅ Los productos se muestran con precios correctos
- ✅ Los pedidos se confirman con detalles
- ✅ El bot mantiene el contexto de la conversación

### 4.2 Si algo no funciona:
1. Verifica que enviaste `join helpful-spider` correctamente
2. Revisa que el webhook esté configurado en Twilio
3. Espera unos segundos entre mensajes
4. Prueba con mensajes simples primero (`hola`, `productos`)

---

## 🚀 PASO 5: COMANDOS AVANZADOS PARA PROBAR

### Pedidos específicos:
```
quiero 2 francés
quiero 1 baguette y 3 empanadas
necesito 5 ciabatti
```

### Consultas:
```
precios
mi historial
mis pedidos
ayuda
```

### Texto libre (el bot intentará extraer productos):
```
Buenos días, quisiera comprar pan francés para el desayuno
Hola, necesito empanadas para una reunión
```

---

## 📊 MONITOREO

### Logs en tiempo real:
Para ver los logs de tu aplicación en Railway:
1. Ve a tu proyecto en Railway
2. Ve a la pestaña **"Deployments"**
3. Haz clic en el deployment activo
4. Ve a **"Logs"** para ver la actividad en tiempo real

### Base de datos:
Cada conversación se guarda en la tabla `chat_logs` con:
- Número de teléfono
- Mensaje del usuario
- Respuesta del bot
- Timestamp

---

## 🎉 ¡LISTO PARA USAR!

Tu chatbot de la Panadería Jos & Mar ya está completamente funcional:

✅ **Desplegado en Railway**
✅ **Integrado con Twilio WhatsApp**
✅ **Base de datos MySQL funcionando**
✅ **Catálogo de productos cargado**
✅ **Sistema de pedidos activo**
✅ **Logs de conversación guardándose**

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Problema: No recibo respuesta del bot
**Solución:** 
- Verifica que enviaste `join helpful-spider`
- Revisa la configuración del webhook en Twilio
- Espera unos segundos

### Problema: Respuestas raras o vacías
**Solución:**
- Prueba comandos simples como `hola` o `productos`
- Verifica los logs en Railway

### Problema: El bot no entiende mi pedido
**Solución:**
- Usa formato simple: `quiero 2 francés`
- Consulta la lista de productos con `productos`

---

**¿Necesitas ayuda?** Revisa los logs en Railway o contacta al desarrollador.
