# 1. Base
FROM python:3.12-slim

# 2. Ambiente
WORKDIR /app

# 3. Dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Código
# ADICIONE A LINHA ABAIXO para copiar nosso novo script
COPY entrypoint.sh .
COPY . .

# 5. Permissões
# ADICIONE A LINHA ABAIXO para tornar o script executável
RUN chmod +x entrypoint.sh

# 6. Rede
EXPOSE 8000

# 7. Ponto de Entrada e Comando
# ADICIONE A LINHA ENTRYPOINT e mantenha o CMD
ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "main:app"]