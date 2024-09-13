import redis
import json
import time
import random

# Conexão com o Redis
r = redis.StrictRedis(host='redis', port=6379, db=0)

# Função que verifica o estoque de 5 tipos de peças finalizadas
def verificar_estoque():
    tipos_pecas = ["PV1", "PV2", "PV3", "PV4", "PV5"]
    capacidade_producao = {}

    for tipo in tipos_pecas:
        total_pecas_disponiveis = 0
        pecas_completas = 0

        for i in range(1, 101):  # Supondo que cada tipo tenha até 100 partes
            dados_peca = r.get(f'{tipo}_parte_{i}')
            if dados_peca:
                dados_peca = json.loads(dados_peca)
                quantidade = dados_peca['quantidade']
                total_pecas_disponiveis += quantidade

                pecas_necessarias_para_unidade = 43 + random.randint(20, 33)
                pecas_completas += quantidade // pecas_necessarias_para_unidade

        capacidade_producao[tipo] = pecas_completas
        print(f'{tipo} - Total de peças disponíveis: {total_pecas_disponiveis}')
        print(f'{tipo} - Capacidade de produção: {pecas_completas} unidades completas')

    return capacidade_producao

# Loop contínuo para verificar o estoque a cada intervalo de tempo
if __name__ == "__main__":
    while True:
        capacidade = verificar_estoque()
        print(f'Capacidade de produção geral: {capacidade}')
        time.sleep(30)  # Verifica a cada 30 segundos
