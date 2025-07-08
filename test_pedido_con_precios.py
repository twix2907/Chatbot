import requests

# Probar un pedido con productos que tienen precios
payload = {
    "queryResult": {
        "intent": {
            "displayName": "RealizarPedido"
        },
        "queryText": "Quiero 4 panes francés y 1 torta tres leches",
        "parameters": {
            "producto": ["francés", "tres leches"],
            "cantidad": [4, 1]
        }
    },
    "originalDetectIntentRequest": {
        "payload": {
            "From": "whatsapp:+51987654321"
        }
    }
}

try:
    response = requests.post("http://localhost:5000/webhook", json=payload)
    print("=== NUEVO PEDIDO CON PRECIOS ===")
    print("Status:", response.status_code)
    print("Response:")
    print(response.json()["fulfillmentText"])
    
except Exception as e:
    print("Error:", e)
