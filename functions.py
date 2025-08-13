import os

def ler_conteudo_py(caminho_do_arquivo: str) -> str:
    """
    Lê o conteúdo de um arquivo Python (.py) e o retorna como uma única string,
    preservando toda a formatação original.

    Args:
        caminho_do_arquivo (str): O caminho completo para o arquivo .py que você deseja ler.

    Returns:
        str: O conteúdo do arquivo como uma string. Se o arquivo não for encontrado
             ou ocorrer outro erro, retorna uma mensagem de erro formatada.
    """
    if not caminho_do_arquivo.endswith('.py'):
        return f"Erro: O arquivo '{caminho_do_arquivo}' não parece ser um arquivo Python (.py)."

    try:
        with open(caminho_do_arquivo, 'r', encoding='utf-8') as arquivo:
            # mantendo todas as quebras de linha (\n) e espaços.
            conteudo_string = arquivo.read()
            return conteudo_string, os.path.basename(caminho_do_arquivo)
    except FileNotFoundError:
        return f"Erro: O arquivo no caminho '{caminho_do_arquivo}' não foi encontrado."
    except Exception as e:
        return f"Ocorreu um erro inesperado ao ler o arquivo: {e}"
