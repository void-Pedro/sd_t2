# Usar imagem base oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o código fonte para o container
COPY . .

# Instalar dependências
RUN pip install redis paho-mqtt

# Comando para rodar o programa
CMD ["python", "linha_producao.py"]
