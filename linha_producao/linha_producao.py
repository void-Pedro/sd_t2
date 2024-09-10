import redis
import time
import random

# Conectar ao Redis
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# Produtos e peças necessárias para fabricação
produtos = {
    "Pv1": {"base": 43, "var": random.randint(20, 33)},
    "Pv2": {"base": 43, "var": random.randint(20, 33)},
    "Pv3": {"base": 43, "var": random.randint(20, 33)},
    "Pv4": {"base": 43, "var": random.randint(20, 33)},
    "Pv5": {"base": 43, "var": random.randint(20, 33)}
}

# Estoque de produtos acabados
estoque_produtos = {
    "Pv1": 100,
    "Pv2": 100,
    "Pv3": 100,
    "Pv4": 100,
    "Pv5": 100
}

# Função para simular pedidos diários de produtos (usado pela fábrica 2)
def simular_pedidos():
    pedidos = {
        "Pv1": random.randint(10, 50),
        "Pv2": random.randint(10, 50),
        "Pv3": random.randint(10, 50),
        "Pv4": random.randint(10, 50),
        "Pv5": random.randint(10, 50)
    }
    print(f"Pedidos do dia (Fábrica 2): {pedidos}")
    return pedidos

# Função para fabricar produtos com base no estoque e pedidos
def fabricar_produtos(pedidos, tipo_fabrica):
    for produto, qtd_pedido in pedidos.items():
        estoque_atual = estoque_produtos[produto]
        if tipo_fabrica == "empurrada":  # Fábrica 1 (empurrada) sempre produz lotes de 48
            qtd_a_produzir = 48
            print(f"Fábrica 1 - Fabricando lote fixo de 48 unidades de {produto}")
        else:  # Fábrica 2 (puxada) produz conforme o pedido
            if estoque_atual < qtd_pedido:
                qtd_a_produzir = qtd_pedido - estoque_atual
                print(f"Fábrica 2 - Fabricando {qtd_a_produzir} unidades de {produto}")
            else:
                print(f"Estoque suficiente de {produto}, sem necessidade de produção.")
                continue

        consumir_partes(produto, qtd_a_produzir)
        estoque_produtos[produto] += qtd_a_produzir
        estoque_produtos[produto] -= qtd_pedido

# Função para consumir partes do almoxarifado para fabricar produtos
def consumir_partes(produto, quantidade):
    partes_necessarias = produtos[produto]
    total_partes = (partes_necessarias["base"] + partes_necessarias["var"]) * quantidade

    for parte in ["parte1", "parte2", "parte3"]:  # Simulação de uso de várias partes
        estoque_atual = int(r.hget("almoxarifado", parte) or 0)
        if estoque_atual >= total_partes:
            r.hincrby("almoxarifado", parte, -total_partes)
            print(f"Consumido {total_partes} unidades de {parte}. Estoque restante: {estoque_atual - total_partes}")
        else:
            print(f"Estoque insuficiente de {parte} para fabricar {produto}. Necessário reabastecimento.")
            # Almoxarifado vai reabastecer se necessário

# Função principal para a fábrica 1 (empurrada)
def fabricar_fabrica_1():
    while True:
        pedidos = {produto: 48 for produto in estoque_produtos.keys()}  # Produção empurrada: 48 unidades por produto
        fabricar_produtos(pedidos, "empurrada")
        print(f"Estoque atual de produtos acabados (Fábrica 1): {estoque_produtos}")
        time.sleep(10)  # Simula o tempo entre os dias

# Função principal para a fábrica 2 (puxada)
def fabricar_fabrica_2():
    while True:
        pedidos = simular_pedidos()  # Produção puxada: pedidos diários aleatórios
        fabricar_produtos(pedidos, "puxada")
        print(f"Estoque atual de produtos acabados (Fábrica 2): {estoque_produtos}")
        time.sleep(10)  # Simula o tempo entre os dias

if __name__ == "__main__":
    # Aqui você pode escolher qual fábrica rodar (empurrada ou puxada)
    #fabricar_fabrica_1()  # Descomente para rodar a fábrica 1
    fabricar_fabrica_2()  # Descomente para rodar a fábrica 2
