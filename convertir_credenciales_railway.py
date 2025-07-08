#!/usr/bin/env python3
"""
Script para convertir credenciales de Google Cloud a base64 para Railway
"""
import base64
import json
import os

def convertir_credenciales_a_base64():
    print("🔐 CONVERTIR CREDENCIALES DE GOOGLE CLOUD PARA RAILWAY")
    print("="*60)
    
    # Pedir la ruta del archivo de credenciales
    while True:
        archivo_json = input("\n📁 Ruta del archivo JSON de credenciales: ").strip()
        
        if os.path.exists(archivo_json):
            break
        else:
            print(f"❌ Archivo no encontrado: {archivo_json}")
            print("   Asegúrate de que la ruta sea correcta")
    
    try:
        # Leer el archivo JSON
        with open(archivo_json, 'r', encoding='utf-8') as f:
            json_content = f.read()
        
        # Validar que es un JSON válido
        json.loads(json_content)
        
        # Convertir a base64
        base64_content = base64.b64encode(json_content.encode('utf-8')).decode('utf-8')
        
        print(f"\n✅ Archivo leído correctamente")
        print(f"📏 Tamaño original: {len(json_content)} caracteres")
        print(f"📏 Tamaño en base64: {len(base64_content)} caracteres")
        
        # Mostrar información del JSON
        json_data = json.loads(json_content)
        print(f"\n📋 INFORMACIÓN DEL ARCHIVO:")
        print(f"   Project ID: {json_data.get('project_id', 'No encontrado')}")
        print(f"   Client Email: {json_data.get('client_email', 'No encontrado')}")
        print(f"   Type: {json_data.get('type', 'No encontrado')}")
        
        # Guardar en archivo para copiar fácilmente
        output_file = "credenciales_base64.txt"
        with open(output_file, 'w') as f:
            f.write(base64_content)
        
        print(f"\n💾 Base64 guardado en: {output_file}")
        print(f"\n🚀 CONFIGURACIÓN PARA RAILWAY:")
        print("="*50)
        print("Ve a tu proyecto en Railway → Variables y agrega:")
        print()
        print("Variable: GOOGLE_APPLICATION_CREDENTIALS_JSON")
        print("Valor: (copia el contenido del archivo credenciales_base64.txt)")
        print()
        print("Variables adicionales:")
        print(f"DIALOGFLOW_PROJECT_ID={json_data.get('project_id', 'tu-project-id')}")
        print("DIALOGFLOW_LANGUAGE_CODE=es-ES")
        print("DIALOGFLOW_ENABLED=true")
        print("DIALOGFLOW_SESSION_ID=default-session")
        
        print(f"\n📝 INSTRUCCIONES:")
        print("1. Abre Railway Dashboard")
        print("2. Ve a tu proyecto")
        print("3. Clic en la pestaña 'Variables'")
        print("4. Agrega cada variable una por una")
        print("5. Para GOOGLE_APPLICATION_CREDENTIALS_JSON:")
        print(f"   - Copia TODO el contenido de {output_file}")
        print("   - Es una línea muy larga, asegúrate de copiarla completa")
        print("6. Redeploya tu aplicación")
        
        print(f"\n✅ ¡Listo! Ahora tu app podrá usar Dialogflow en Railway")
        
    except json.JSONDecodeError:
        print("❌ Error: El archivo no es un JSON válido")
    except Exception as e:
        print(f"❌ Error procesando archivo: {e}")

def verificar_variables_railway():
    print("\n🔍 VERIFICAR VARIABLES EN RAILWAY")
    print("="*40)
    print("Después de configurar las variables, verifica:")
    print()
    print("1. Ve a Railway Dashboard → Tu proyecto → Variables")
    print("2. Deberías ver estas variables:")
    print("   ✅ DIALOGFLOW_PROJECT_ID")
    print("   ✅ DIALOGFLOW_LANGUAGE_CODE")
    print("   ✅ DIALOGFLOW_ENABLED")
    print("   ✅ DIALOGFLOW_SESSION_ID")
    print("   ✅ GOOGLE_APPLICATION_CREDENTIALS_JSON")
    print()
    print("3. Redeploya tu aplicación")
    print("4. Prueba el endpoint: https://tu-app.railway.app/dialogflow-status")

if __name__ == "__main__":
    print("🎯 CONFIGURACIÓN DE DIALOGFLOW PARA RAILWAY")
    print("="*50)
    print("1. Convertir credenciales a base64")
    print("2. Ver instrucciones de verificación")
    print("="*50)
    
    opcion = input("Elige una opción (1 o 2): ").strip()
    
    if opcion == "1":
        convertir_credenciales_a_base64()
    elif opcion == "2":
        verificar_variables_railway()
    else:
        print("Opción no válida")
        convertir_credenciales_a_base64()
