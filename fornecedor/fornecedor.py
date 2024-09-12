
import redis
import time
import json

class Parte:
    def __init__(self, nome, quantidade_inicial, nivel_critico):
        self.nome = nome
        self.quantidade = quantidade_inicial
        self.nivel_critico = nivel_critico  # Quando o estoque chegar nesse nível, é necessário reabastecer

    def precisa_reabastecer(self):
        return self.quantidade <= self.nivel_critico

class Fornecedor:
    def __init__(self, redis_host='bancoRedis', redis_port=6379, numero_de_partes=100):
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
        self.estoque = self.gerar_estoque(numero_de_partes)

    def gerar_estoque(self, numero_de_partes):
        estoque = {}
        for i in range(1, numero_de_partes + 1):
            nome_parte = f"parte_{i}"
            # Cada parte pode ter uma quantidade inicial e nível crítico diferente, se necessário
            quantidade_inicial = 1000  # Configuração padrão de estoque inicial
            nivel_critico = 100  # Nível abaixo do qual é necessário reabastecer
            estoque[nome_parte] = Parte(nome_parte, quantidade_inicial, nivel_critico)
        return estoque

    def monitorar_estoque(self):
        # Verifica constantemente o estoque
        for parte in self.estoque.values():
            if parte.precisa_reabastecer():
                print(f"Estoque baixo para {parte.nome}: {parte.quantidade}. Emitindo pedido de reabastecimento.")
                self.emitir_pedido_reabastecimento(parte)
            else:
                print(f"Estoque de {parte.nome} está OK: {parte.quantidade} unidades.")

    def emitir_pedido_reabastecimento(self, parte):
        pedido = {'parte': parte.nome, 'quantidade': 500}
        print(f"Emitindo pedido de reabastecimento para {parte.nome}")
        self.redis_client.publish('pedidos_reabastecimento', json.dumps(pedido))

    def ouvir_pedidos_almoxarifado(self):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe('pedidos_compra_almoxarifado')  # Canal correto para pedidos do almoxarifado
        print("Aguardando pedidos do almoxarifado...")
        
        for mensagem in pubsub.listen():
            if mensagem['type'] == 'message':
                pedido = json.loads(mensagem['data'])
                self.processar_pedido(pedido)
    
    def processar_pedido(self, pedido):
        parte_nome = pedido['parte']
        quantidade = pedido['quantidade']
        
        parte = self.estoque.get(parte_nome)
        if parte and parte.quantidade >= quantidade:
            print(f"Processando pedido de {quantidade} unidades da {parte.nome}")
            parte.quantidade -= quantidade
            self.enviar_reabastecimento(pedido)
        else:
            print(f"Estoque insuficiente para {parte_nome}. Pedido não pode ser processado.")
    
    def enviar_reabastecimento(self, pedido):
        print(f"Enviando {pedido['quantidade']} unidades da {pedido['parte']} para o almoxarifado.")
        # Atualiza o estoque no Redis para o almoxarifado
        self.redis_client.publish('estoque_almoxarifado', json.dumps(pedido))
    
    def run(self):
        try:
            while True:
                self.monitorar_estoque()  # Verifica se o estoque está baixo
                self.ouvir_pedidos_almoxarifado()  # Ouve os pedidos do almoxarifado
                time.sleep(5)  # Intervalo de monitoramento
        except KeyboardInterrupt:
            print("Fornecedor encerrado.")

if __name__ == '__main__':
    fornecedor = Fornecedor()
    fornecedor.run()
