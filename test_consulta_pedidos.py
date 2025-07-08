import requests

payload = {
    "queryResult": {
        "intent": {
            "displayName": "ConsultarPedidosPrevios"
        },
        "queryText": "¿Cuáles son mis pedidos?",
        "parameters": {}
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
    print("Response:")
    print(response.json()["fulfillmentText"])
except Exception as e:
    print("Error:", e)
