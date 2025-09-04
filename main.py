import os
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

# Funções principais de negócio importadas do nosso módulo 'app'.
from app.functions import (
    ler_conteudo_py,
    ler_conteudo_pas,
    gerar_resposta_ia_document,
    criar_docx_formatado
)


app = Flask(__name__)

# Define constantes para os diretórios e extensões permitidas.
UPLOAD_FOLDER = 'uploads'
DOCS_FOLDER = 'docs'
ALLOWED_EXTENSIONS = {'py', 'pas'}

# Aplica as configurações ao app Flask.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOCS_FOLDER'] = DOCS_FOLDER

# Garante que as pastas de trabalho existam ao iniciar.
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOCS_FOLDER, exist_ok=True)


# --- Rotas da Aplicação ---

def allowed_file(filename):
    """Helper para validar a extensão dos arquivos enviados."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           

@app.route('/')
def index():
    """Rota principal: exibe a página de upload (index.html)."""
    return render_template('index.html')


@app.route('/gerar', methods=['POST'])
def gerar_documentacao():
    """Recebe os arquivos, processa um a um e retorna a página de resultados."""
    # Validação inicial da requisição.
    if 'arquivos' not in request.files:
        return "Erro: Nenhum campo de arquivo na requisição", 400
    
    # Coleta os arquivos e o contexto do formulário.
    files = request.files.getlist('arquivos')
    contexto_adicional = request.form.get('contexto', 'Nenhum.')
    
    sucessos, erros = [], []

    # Itera sobre cada arquivo enviado.
    for file in files:
        if not file or not allowed_file(file.filename):
            continue

        filename_seguro = secure_filename(file.filename)
        caminho_salvo = os.path.join(app.config['UPLOAD_FOLDER'], filename_seguro)
        
        try:
            # Salva o arquivo no início do bloco 'try'
            file.save(caminho_salvo)

            # Lê o conteúdo do arquivo com a função apropriada.
            if filename_seguro.lower().endswith('.py'):
                resultado_leitura = ler_conteudo_py(caminho_salvo)
            else:
                resultado_leitura = ler_conteudo_pas(caminho_salvo)
            
            # Tratamento de erro na leitura.
            if isinstance(resultado_leitura, str):
                erros.append(f"Arquivo '{filename_seguro}': {resultado_leitura}")
                continue
            
            conteudo_codigo, nome_base = resultado_leitura
            
            # Gera a documentação via IA.
            print(f"DEBUG: Enviando o arquivo '{nome_base}' para a IA. Aguardando resposta...")
            documentacao_ia = gerar_resposta_ia_document(conteudo_codigo, nome_base, contexto_adicional)
            print(f"DEBUG: Resposta da IA para '{nome_base}' recebida. Tamanho: {len(documentacao_ia)} caracteres.")
            
            # Tratamento de erro da API da IA.
            if documentacao_ia.startswith("Erro ao gerar resposta da IA"):
                erros.append(f"Arquivo '{filename_seguro}': {documentacao_ia}")
                continue

            # Cria o arquivo .docx.
            nome_docx = f"DOC_{nome_base}.docx"
            print(f"DEBUG: Criando o arquivo DOCX para '{nome_base}'...")
            if criar_docx_formatado(documentacao_ia, nome_docx, app.config['DOCS_FOLDER']):
                sucessos.append(nome_docx)
                print(f"DEBUG: Arquivo '{nome_docx}' criado com sucesso.")
            else:
                erros.append(f"Arquivo '{filename_seguro}': Falha ao salvar o arquivo .docx.")

        finally:
            # Este bloco será executado SEMPRE, garantindo a exclusão do arquivo.
            if os.path.exists(caminho_salvo):
                os.remove(caminho_salvo)
                print(f"DEBUG: Arquivo temporário '{caminho_salvo}' excluído.")

    # Retorna a página de resultados com as listas de sucessos e erros.
    return render_template('resultados.html', sucessos=sucessos, erros=erros)


@app.route('/download/<filename>')
def download_file(filename):
    """Rota dinâmica para permitir o download dos arquivos .docx gerados."""
    return send_from_directory(app.config['DOCS_FOLDER'], filename, as_attachment=True)

# Bloco de execução principal: inicia o servidor Flask em modo debug.
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5001)