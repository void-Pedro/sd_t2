import paho.mqtt.client as mqtt
import redis
import json

# Conectar ao Redis
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# Conectar ao Broker MQTT
client = mqtt.Client("Almoxarifado")
MQTT_BROKER = "mqtt_broker"

# Níveis críticos de estoque
limite_critico = {
    "parte1": 200,
    "parte2": 150,
    "parte3": 100,
}

def monitorar_estoque():
    for parte, limite in limite_critico.items():
        quantidade = int(r.hget("almoxarifado", parte) or 0)
        print(f"Estoque de {parte}: {quantidade}")
        if quantidade < limite:
            # Pedido de reabastecimento
            pedido = json.dumps({"parte": parte, "quantidade": limite - quantidade})
            client.publish("reabastecimento", pedido)
            print(f"Pedido de reabastecimento enviado para {parte}")

# Callback para conexão
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker MQTT")

client.on_connect = on_connect
client.connect(MQTT_BROKER)

# Loop principal para monitorar o estoque
while True:
    monitorar_estoque()
