# GUÍA COMPLETA: DESPLEGAR CHATBOT EN RAILWAY PARA WHATSAPP
# ========================================================

## 🚀 VENTAJAS DE RAILWAY
- ✅ URL permanente (no cambia como ngrok)
- ✅ SSL automático (HTTPS)
- ✅ Deploy automático desde GitHub
- ✅ Base de datos MySQL incluida
- ✅ Logs en tiempo real
- ✅ Escalamiento automático

## 📋 PREPARACIÓN PARA RAILWAY

### 1. VERIFICAR ARCHIVOS NECESARIOS
- ✅ app.py (webhook principal)
- ✅ requirements.txt (dependencias)
- ✅ Procfile (comando de inicio)
- ✅ .env (variables de entorno - ejemplo)
- ✅ README.md (documentación)

### 2. CONFIGURAR GIT (SI NO ESTÁ CONFIGURADO)
```bash
git init
git add .
git commit -m "Initial commit - Panadería Jos & Mar Chatbot"
```

### 3. SUBIR A GITHUB
1. Crear repositorio en GitHub
2. Conectar repositorio local:
```bash
git remote add origin https://github.com/tu-usuario/panaderia-chatbot.git
git branch -M main
git push -u origin main
```

## 🔧 PASOS PARA DESPLEGAR EN RAILWAY

### 1. CREAR CUENTA EN RAILWAY
- Ve a: https://railway.app
- Regístrate con GitHub (recomendado)
- Verifica tu cuenta

### 2. CREAR NUEVO PROYECTO
1. Click en "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Conecta tu repositorio del chatbot
4. Railway detectará automáticamente que es una app Python

### 3. CONFIGURAR BASE DE DATOS MYSQL
1. En tu proyecto Railway, click "New Service"
2. Selecciona "Database" > "MySQL"
3. Railway creará automáticamente una instancia MySQL
4. Copia las credenciales de conexión

### 4. CONFIGURAR VARIABLES DE ENTORNO
En Railway, ve a Variables y agrega:
```
DB_HOST=containers-us-west-xxx.railway.app
DB_PORT=7691
DB_NAME=railway
DB_USER=root
DB_PASSWORD=tu-password-generado
WEBHOOK_VERIFY_TOKEN=panaderia_jos_mar_2025
```

### 5. CONFIGURAR DOMINIO PERSONALIZADO (OPCIONAL)
1. En Settings > Domains
2. Generar dominio: ej. panaderia-chatbot.up.railway.app
3. O conectar tu propio dominio

## 📱 CONECTAR CON WHATSAPP

### OPCIÓN A: META WHATSAPP CLOUD API (GRATIS - RECOMENDADO)
1. Ve a: https://developers.facebook.com
2. Crear App > Tipo "Business"
3. Agregar producto "WhatsApp"
4. Configurar Webhook:
   - URL: https://tu-app.up.railway.app/webhook
   - Verify Token: panaderia_jos_mar_2025
5. Suscribirse a eventos: messages, message_status

### OPCIÓN B: TWILIO WHATSAPP (FÁCIL PARA PRUEBAS)
1. Crear cuenta en twilio.com
2. Console > Messaging > Try WhatsApp
3. Configurar Webhook: https://tu-app.up.railway.app/webhook
4. Seguir instrucciones del sandbox

## 🔧 COMANDOS ÚTILES

### Verificar deployment:
```bash
curl https://tu-app.up.railway.app/health
```

### Ver logs en Railway:
- Click en tu servicio > Ver logs en tiempo real

### Actualizar código:
```bash
git add .
git commit -m "Actualización del chatbot"
git push
# Railway desplegará automáticamente
```

## 🧪 TESTING

### 1. Probar Health Check:
```
GET https://tu-app.up.railway.app/health
```

### 2. Probar Webhook:
```
POST https://tu-app.up.railway.app/webhook
```

### 3. Enviar mensaje de WhatsApp:
- Usar número configurado en Meta/Twilio
- Probar intents: saludo, productos, pedidos

## 📊 MONITOREO

### Logs importantes a reviever:
- Conexiones a BD exitosas
- Requests de WhatsApp recibidos
- Respuestas enviadas
- Errores de procesamiento

### Métricas en Railway:
- CPU usage
- Memory usage
- Request count
- Response times

## 🔧 TROUBLESHOOTING

### Error de conexión a BD:
- Verificar variables de entorno
- Revisar logs de MySQL en Railway
- Confirmar que las tablas existen

### Webhook no recibe mensajes:
- Verificar URL en configuración WhatsApp
- Comprobar que el verify token coincida
- Revisar logs de Railway

### Respuestas lentas:
- Optimizar queries de BD
- Revisar uso de memoria
- Considerar upgrade de plan Railway

## 💡 TIPS ADICIONALES

1. **Backup de BD**: Railway hace backups automáticos
2. **SSL**: Automático, no requiere configuración
3. **Scaling**: Automático según tráfico
4. **Custom Domains**: Disponible en planes pagos
5. **Team Access**: Invitar colaboradores fácilmente

## 🎯 SIGUIENTE PASO
Ejecutar script de preparación para Railway...
