#!/usr/bin/env python3
"""
Verificador interactivo para diagnosticar problemas con Twilio WhatsApp
"""

def verificador_interactivo():
    print("🔧 VERIFICADOR INTERACTIVO - TWILIO WHATSAPP")
    print("="*60)
    print("Te voy a hacer algunas preguntas para diagnosticar el problema\n")
    
    # Paso 1: Configuración en Twilio
    print("1️⃣ CONFIGURACIÓN EN TWILIO CONSOLE")
    print("-"*40)
    
    q1 = input("¿Entraste a https://console.twilio.com/? (s/n): ").lower().strip()
    if q1 != 's':
        print("❌ Primero necesitas entrar a la consola de Twilio")
        return
    
    q2 = input("¿Fuiste a Messaging → Try it out → Send a WhatsApp message? (s/n): ").lower().strip()
    if q2 != 's':
        print("❌ Necesitas ir a esa sección específica")
        return
    
    print("\n📋 En 'Webhook configuration for Sandbox':")
    webhook_url = input("¿Qué URL pusiste? ").strip()
    expected_url = "https://chatbot-production-ec53.up.railway.app/webhook"
    
    if webhook_url != expected_url:
        print(f"❌ URL incorrecta!")
        print(f"   Tienes: {webhook_url}")
        print(f"   Debe ser: {expected_url}")
        return
    else:
        print("✅ URL correcta")
    
    method = input("¿Qué método HTTP seleccionaste? (GET/POST): ").upper().strip()
    if method != "POST":
        print("❌ Debe ser POST, no GET")
        return
    else:
        print("✅ Método correcto")
    
    q3 = input("¿Hiciste clic en 'Save Configuration'? (s/n): ").lower().strip()
    if q3 != 's':
        print("❌ Debes guardar la configuración")
        return
    
    # Paso 2: Configuración en WhatsApp
    print("\n2️⃣ CONFIGURACIÓN EN WHATSAPP")
    print("-"*40)
    
    q4 = input("¿Agregaste +1 415 523 8886 a tus contactos de WhatsApp? (s/n): ").lower().strip()
    if q4 != 's':
        print("❌ Necesitas agregar este número a tus contactos primero")
        return
    
    join_message = input("¿Qué mensaje enviaste exactamente? ").strip()
    if join_message.lower() != "join helpful-spider":
        print(f"❌ Mensaje incorrecto!")
        print(f"   Enviaste: '{join_message}'")
        print("   Debe ser exactamente: 'join helpful-spider'")
        print("   (todo en minúsculas, con el espacio)")
        return
    else:
        print("✅ Mensaje correcto")
    
    q5 = input("¿Recibiste un mensaje de confirmación de Twilio? (s/n): ").lower().strip()
    if q5 != 's':
        print("❌ PROBLEMA IDENTIFICADO: No recibiste confirmación")
        print("\n🔧 SOLUCIONES:")
        print("1. Verifica que tu número esté en formato correcto")
        print("2. Algunos países tienen restricciones con Twilio sandbox")
        print("3. Intenta desde otro número")
        print("4. Verifica que tu cuenta de Twilio esté activa")
        return
    
    # Paso 3: Prueba de mensajes
    print("\n3️⃣ PRUEBA DE MENSAJES")
    print("-"*40)
    
    q6 = input("¿Intentaste enviar un mensaje de prueba después de la confirmación? (s/n): ").lower().strip()
    if q6 == 's':
        test_message = input("¿Qué mensaje enviaste? ").strip()
        q7 = input("¿Recibiste respuesta del bot? (s/n): ").lower().strip()
        
        if q7 == 's':
            print("🎉 ¡EXCELENTE! Tu chatbot está funcionando")
        else:
            print("❌ El bot no respondió")
            print("\n🔧 DIAGNÓSTICOS ADICIONALES:")
            print("1. Verifica los logs en Railway")
            print("2. Puede haber un delay, espera 30 segundos")
            print("3. Intenta con mensajes simples: 'hola', 'test'")
    else:
        print("📋 SIGUIENTE PASO: Envía un mensaje de prueba")
        print("   Recomendado: 'hola' o 'test'")
    
    print(f"\n{'='*60}")
    print("📊 DIAGNÓSTICO COMPLETADO")
    print("Si todo está configurado correctamente y sigue sin funcionar:")
    print("1. Revisa los logs en Railway")
    print("2. Verifica tu cuenta de Twilio")
    print("3. Prueba con otro número de teléfono")

def mostrar_logs_railway():
    print("\n📊 CÓMO VER LOGS EN RAILWAY:")
    print("="*40)
    print("1. Ve a https://railway.app/")
    print("2. Abre tu proyecto")
    print("3. Ve a la pestaña 'Deployments'")
    print("4. Haz clic en el deployment activo")
    print("5. Ve a 'Logs'")
    print("6. Envía un mensaje desde WhatsApp")
    print("7. Deberías ver actividad en los logs")
    print("\n🔍 Busca líneas como:")
    print("   - 'Mensaje recibido desde'")
    print("   - 'Respuesta enviada'")
    print("   - Cualquier error en rojo")

if __name__ == "__main__":
    verificador_interactivo()
    mostrar_logs_railway()
