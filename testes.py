import sys
import os
from app.functions import *
from app.prompts import *

caminho_completo = "C:\\Users\\marcos.rodrigues\\Downloads\\uPrincipal.pas"
print(f"Lendo o arquivo: {caminho_completo}")
str_codigo_fonte, nome_arquivo = ler_conteudo_pas(caminho_completo)

if not str_codigo_fonte or not nome_arquivo:
    print(f"Erro ao ler o arquivo: {caminho_completo}")
    sys.exit(1)

str_codigo_safe = str_codigo_fonte.replace("```", "'''").replace('"""', "'''")

resp = gerar_resposta_ia_document(str_codigo_safe, nome_arquivo, contexto_adicional="Nesse caso, o código é da linguagem Pascal, então o contexto é diferente do Python. Mas utilize a mesma lógica de análise e documentação.")

criar_docx_formatado(resp, nome_arquivo.split(".")[0])
