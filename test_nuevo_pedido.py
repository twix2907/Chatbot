import requests
import json

payload = {
    "queryResult": {
        "intent": {
            "displayName": "RealizarPedido"
        },
        "queryText": "Quiero 3 bizcochos y 2 alfajores",
        "parameters": {
            "producto": ["bizcocho", "alfajor"],
            "cantidad": [3, 2]
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
    print("Status:", response.status_code)
    print("Response:", response.json()["fulfillmentText"])
except Exception as e:
    print("Error:", e)
