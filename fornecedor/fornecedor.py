import paho.mqtt.client as mqtt
import redis
import json

# Conectar ao Redis
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# Conectar ao Broker MQTT
client = mqtt.Client("Fornecedor")
MQTT_BROKER = "mqtt_broker"

# Estoque do fornecedor
fornecedor_estoque = {
    "parte1": 1000,
    "parte2": 1000,
    "parte3": 1000,
}

# Função que processa o pedido de reabastecimento
def on_message(client, userdata, message):
    data = json.loads(message.payload)
    parte = data["parte"]
    quantidade = data["quantidade"]
    print(f"Pedido de {quantidade} unidades de {parte} recebido")

    if fornecedor_estoque.get(parte, 0) >= quantidade:
        fornecedor_estoque[parte] -= quantidade
        r.hincrby("almoxarifado", parte, quantidade)  # Atualiza o estoque no Redis
        print(f"Reabastecido com sucesso. Estoque atual de {parte}: {fornecedor_estoque[parte]}")
    else:
        print(f"Estoque insuficiente para {parte}. Pedido não atendido.")

# Callback para conexão
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker MQTT")
    client.subscribe("reabastecimento")

client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER)

client.loop_forever()
