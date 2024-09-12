import redis
import time
import random
import json

r = redis.StrictRedis(host='bancoRedis', port=6379, db=0)

# Definir níveis de estoque
NIVEL_VERDE = 150
NIVEL_AMARELO = 80
NIVEL_VERMELHO = 30

def definir_cor(quantidade):
    if quantidade >= NIVEL_VERDE:
        return 'green'
    elif NIVEL_AMARELO <= quantidade < NIVEL_VERDE:
        return 'yellow'
    else:
        return 'red'

def verificar_estoque():
    for i in range(1, 101):
        dados_peca = r.get(f'parte_{i}')
        if dados_peca:
            dados_peca = json.loads(dados_peca)
            quantidade = dados_peca['quantidade']
            cor = definir_cor(quantidade)
            dados_peca['cor'] = cor
            r.set(f'parte_{i}', json.dumps(dados_peca))
            
            print(f'Peça {i} - {quantidade} unidades, Cor: {cor}')
            
            # Se tiver com poucas peças faz a solicitação (joga no redis)
            if quantidade < NIVEL_VERMELHO:
                chave_solicitacao = f'solicitacao_{i}'
                if not r.exists(chave_solicitacao):
                    r.setex(chave_solicitacao, 3600, 'Pendente')
        else:
            print(f'Peça {i} - Estoque não definido.')

def inicializar_estoque():
    for i in range(1, 101):
        quantidade_inicial = random.randint(30, 100)
        cor_inicial = definir_cor(quantidade_inicial)
        dados_peca = json.dumps({'quantidade': quantidade_inicial, 'cor': cor_inicial})
        r.set(f'parte_{i}', dados_peca)
    print("Estoque inicializado para 100 peças.")

if __name__ == "__main__":
    inicializar_estoque()

    while True:
        verificar_estoque()
        time.sleep(10)
