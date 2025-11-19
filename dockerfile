# Base
FROM python:3.12-slim

# Ambiente
WORKDIR /app

# Dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código e arquivos copiados
COPY entrypoint.sh .
COPY . .

# Permissões (entrypoint será excutável)
RUN chmod +x entrypoint.sh

# Rede
EXPOSE 8000

# Ponto de Entrada e Comando
ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8000", "--timeout", "300", "main:app"]