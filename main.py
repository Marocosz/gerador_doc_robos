import sys
from app.functions import *



# Caminho do arquivo a ser documentado está definido diretamente no código.
caminho_do_arquivo_alvo = "C:\\Users\\marcos.rodrigues\\Documents\\documentation\\doc_bic_distribui_xml.py"
print(f"Lendo o arquivo alvo: {caminho_do_arquivo_alvo}")


str_codigo_fonte, nome_arquivo = ler_conteudo_py(caminho_do_arquivo_alvo)

# Valida se a leitura do arquivo foi bem-sucedida
if not str_codigo_fonte or not nome_arquivo:
    print(f"Erro ao ler o arquivo: {caminho_do_arquivo_alvo}")
    sys.exit(1)

# Configura a str para evitar conflitos com a formatação do prompt da IA
str_codigo_safe = str_codigo_fonte.replace("```", "'''").replace('"""', "'''")

resp = gerar_resposta_ia_document(str_codigo_safe, nome_arquivo, contexto_adicional="Nenhum.")


criar_docx_formatado(resp, nome_arquivo.split(".")[0])