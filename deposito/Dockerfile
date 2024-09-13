# Usando uma imagem base do Python
FROM python:3.9-alpine

# Definir diretório de trabalho
WORKDIR /app

# Copiar os arquivos necessários para o container
COPY . .

# Instalar dependências, se necessário
RUN pip install redis

# Comando para rodar o depósito
CMD ["python", "deposito.py"]
