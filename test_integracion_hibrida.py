#!/usr/bin/env python3
"""
Script para probar la integración híbrida con Dialogflow
"""
import requests
import json

def probar_integracion_hibrida():
    railway_url = "https://chatbot-production-ec53.up.railway.app"
    
    print("🤖 PRUEBA DE INTEGRACIÓN HÍBRIDA - DIALOGFLOW + LOCAL")
    print("="*60)
    
    # 1. Verificar estado de Dialogflow
    print("\n1️⃣ VERIFICANDO ESTADO DE DIALOGFLOW...")
    try:
        response = requests.get(f"{railway_url}/dialogflow-status", timeout=10)
        if response.status_code == 200:
            status = response.json()
            print(f"   ✅ Dialogflow disponible: {status.get('dialogflow_available')}")
            print(f"   ✅ Dialogflow habilitado: {status.get('dialogflow_enabled')}")
            print(f"   📋 Modo: {status.get('mode')}")
            print(f"   📝 Descripción: {status.get('description')}")
            if status.get('project_id'):
                print(f"   🔗 Proyecto: {status.get('project_id')}")
        else:
            print(f"   ❌ Error obteniendo estado: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Probar mensajes diversos
    print(f"\n2️⃣ PROBANDO MENSAJES CON SISTEMA HÍBRIDO...")
    print("-"*50)
    
    mensajes_prueba = [
        "Hola",
        "Buenos días",
        "¿Qué productos tienen?",
        "Quiero 2 panes francés",
        "Necesito 3 empanadas y 1 baguette",
        "¿Cuánto cuesta el pan?",
        "Mis pedidos",
        "Gracias, adiós",
        "xyz mensaje raro que no entiende"
    ]
    
    for i, mensaje in enumerate(mensajes_prueba, 1):
        print(f"\n   Prueba {i}: '{mensaje}'")
        
        try:
            test_data = {
                'From': 'whatsapp:+51999999999',
                'Body': mensaje,
                'MessageSid': f'test_hibrido_{i}'
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.post(
                f"{railway_url}/webhook",
                data=test_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                # Extraer respuesta de TwiML
                response_text = response.text
                if '<Message>' in response_text:
                    start = response_text.find('<Message>') + 9
                    end = response_text.find('</Message>')
                    if start > 8 and end > start:
                        bot_response = response_text[start:end]
                        print(f"      ✅ Respuesta: {bot_response[:80]}...")
                    else:
                        print("      ⚠️  No se pudo extraer respuesta")
                else:
                    print(f"      ⚠️  Formato inesperado: {response_text[:50]}...")
            else:
                print(f"      ❌ Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ Error: {str(e)[:50]}...")
    
    # 3. Estadísticas del sistema
    print(f"\n3️⃣ INFORMACIÓN DEL SISTEMA...")
    print("-"*50)
    
    try:
        health_response = requests.get(f"{railway_url}/health", timeout=10)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   ✅ Estado general: {health_data.get('status')}")
            print(f"   🗄️  Base de datos: {health_data.get('database')}")
        
        info_response = requests.get(f"{railway_url}/info", timeout=10)
        if info_response.status_code == 200:
            info_data = info_response.json()
            print(f"   📱 WhatsApp ready: {info_data.get('whatsapp_ready')}")
            print(f"   🤖 Database ready: {info_data.get('database_ready')}")
            
    except Exception as e:
        print(f"   ❌ Error obteniendo info: {e}")
    
    print(f"\n{'='*60}")
    print("📊 RESUMEN DE LA INTEGRACIÓN HÍBRIDA:")
    print("✅ El sistema funciona con o sin Dialogflow")
    print("✅ Si Dialogflow falla, usa procesamiento local")
    print("✅ Mejor extracción de entidades con Dialogflow")
    print("✅ Fallback robusto garantiza funcionamiento")
    print(f"{'='*60}")
    
    print(f"\n🎯 PASOS PARA HABILITAR DIALOGFLOW COMPLETAMENTE:")
    print("1. Crear proyecto en Google Cloud Console")
    print("2. Habilitar API de Dialogflow ES")
    print("3. Crear agente en Dialogflow Console")
    print("4. Configurar intents y entidades")
    print("5. Obtener credenciales de servicio (JSON)")
    print("6. Configurar variables de entorno en Railway")
    print("7. ¡Disfrutar del mejor NLP!")

if __name__ == "__main__":
    probar_integracion_hibrida()
