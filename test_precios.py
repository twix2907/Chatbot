import requests

# Probar consulta de precios
payload = {
    "queryResult": {
        "intent": {
            "displayName": "ConsultarPrecios"
        },
        "queryText": "¿Cuánto cuesta la torta tres leches?",
        "parameters": {
            "producto": "tres leches"
        }
    }
}

try:
    response = requests.post("http://localhost:5000/webhook", json=payload)
    print("=== CONSULTA DE PRECIO ===")
    print("Status:", response.status_code)
    print("Response:", response.json()["fulfillmentText"])
    print()
    
    # Probar con otro producto
    payload["queryResult"]["queryText"] = "¿Cuánto cuesta el pan francés?"
    payload["queryResult"]["parameters"]["producto"] = "francés"
    
    response = requests.post("http://localhost:5000/webhook", json=payload)
    print("=== CONSULTA DE PRECIO 2 ===")
    print("Status:", response.status_code)
    print("Response:", response.json()["fulfillmentText"])
    
except Exception as e:
    print("Error:", e)
