import os
from groq import Groq
from docx import Document
from docx.shared import Inches
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- 1. CONFIGURAÇÃO ---

# NOVO: INSTRUÇÕES PARA A IA SE TORNAR UMA ESPECIALISTA EM DOCUMENTAÇÃO
# Este prompt ensina a IA a analisar código e gerar a documentação no formato exato que queremos.
INSTRUCOES_IA = """
Você é um assistente de IA especializado em analisar código Python e criar documentação técnica detalhada. Sua tarefa é gerar uma documentação para o script que fornecerei, seguindo rigorosamente a estrutura e o formato definidos abaixo.

**ESTRUTURA OBRIGATÓRIA DA DOCUMENTAÇÃO:**

**Documentação – [Nome do Script]**

**Área relacionada**
[Analise o código e o contexto para preencher a área de negócio ou sistema principal]

**Frequência**
[Analise a linha do crontab fornecida para descrever a frequência em linguagem natural]

**Servidor**
[IP do Servidor de Aplicação] (Se não souber, mantenha este texto como placeholder)

**Resumo da aplicação**
[Escreva um parágrafo conciso explicando o objetivo principal e a função do script, com base na análise do código.]

**Funcionamento da aplicação**

**Pré-requisitos**
* **Bibliotecas Python:**
    * [Liste aqui as bibliotecas não nativas importadas (ex: pandas, requests, SQLAlchemy, etc.).]
    * [Liste aqui os módulos nativos do Python utilizados (ex: os, sys, datetime, etc.).]
* **Arquivos Necessários:**
    * [Descreva os arquivos de configuração, módulos externos ou outros arquivos que o script precisa para funcionar, como o módulo 'tools' e o arquivo '.env'.]
* **Parâmetros de Linha de Comando:**
    * [Se o script usar `sys.argv`, descreva aqui quais parâmetros ele espera e em que ordem.]

**Fluxo de Execução Detalhado**
[Descreva o passo a passo lógico do script em parágrafos. Use títulos em negrito para cada etapa principal, como "Inicialização", "Conexão com Banco de Dados", "Processamento em Loop", "Tratamento de Erro", "Finalização", etc. Seja detalhado e técnico.]

**Lógica por Cliente (Opcional)**
[Se o script tiver lógicas diferentes para clientes específicos, detalhe aqui como cada um é identificado e processado. Se não for o caso, omita esta seção.]

**Funções Auxiliares Principais**
[Descreva o propósito de cada função definida no script. Se o script não tiver funções auxiliares próprias e usar apenas as de um módulo externo como o 'tools', declare isso.]


**INFORMAÇÕES QUE VOCÊ DEVE USAR PARA GERAR A DOCUMENTAÇÃO:**

**1. NOME DO SCRIPT:**
[Digite o nome do arquivo, ex: meu_script.py]

**2. CÓDIGO-FONTE DO SCRIPT PYTHON:**
```python
[COLE O CÓDIGO COMPLETO DO SCRIPT AQUI]
Descreva o que acontece quando uma entrada (ex: um e-mail) não corresponde a nenhum dos clientes configurados. Qual é o fluxo de exceção ou o caminho alternativo?
"""

# NOVO: MODELO DE IA MAIS POTENTE
# Analisar código é uma tarefa complexa. Um modelo mais robusto como o Mixtral ou Llama3-70b é recomendado.
modelo_ia = "mixtral-8x7b-32768"

# NOME DO ARQUIVO DE SAÍDA
nome_arquivo_saida = "Documentacao_Script_NFS.docx"

# NOVO: PROMPT DO USUÁRIO AGORA É O CÓDIGO-FONTE A SER DOCUMENTADO
# Simplesmente cole o código completo que você quer documentar aqui dentro.
prompt_usuario = ""

def gerar_conteudo_com_ia(instrucoes: str, prompt: str, modelo: str) -> str:
    """
    Envia o prompt para a API da Groq e retorna a resposta da IA.
    """
    print("🤖 Analisando o código e gerando a documentação com a IA...")
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("A variável de ambiente GROQ_API_KEY não foi definida. Verifique seu arquivo .env.")
            
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": instrucoes,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=modelo,
            temperature=0.2, # Baixa temperatura para a IA seguir as regras mais estritamente
        )
        print("✅ Documentação gerada com sucesso!")
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"❌ Erro ao se comunicar com a API da Groq: {e}")
        return ""

def criar_docx_formatado(conteudo: str, nome_arquivo: str):
    """
    Cria um arquivo .docx formatado a partir de um texto com sintaxe Markdown simples.
    """
    print(f"📄 Criando o arquivo .docx '{nome_arquivo}'...")
    doc = Document()
    doc.core_properties.title = "Documentação de Script"
    doc.core_properties.author = "Gerador de Documentação com IA"

    # Define a margem do documento
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    linhas = conteudo.strip().split('\n')

    for linha in linhas:
        linha_strip = linha.strip()
        if linha_strip.startswith('## '):
            doc.add_heading(linha_strip[3:], level=2)
        elif linha_strip.startswith('# '):
            doc.add_heading(linha_strip[2:], level=1)
        elif linha_strip.startswith('- **`'): # Para a lista de funções
            # Lógica para separar o nome da função da descrição
            partes = linha_strip.split('`**: ')
            if len(partes) > 1:
                nome_funcao = partes[0].replace('- **`', '')
                descricao = partes[1]
                p = doc.add_paragraph(style='List Bullet')
                p.add_run(f'{nome_funcao}`').bold = True
                p.add_run(f': {descricao}')
            else:
                doc.add_paragraph(linha, style='List Bullet')
        elif linha_strip.startswith('- '):
            doc.add_paragraph(linha_strip[2:], style='List Bullet')
        elif linha_strip.startswith('* **'): # Para a lista de clientes
            p = doc.add_paragraph(style='List Bullet')
            p.add_run(linha_strip.replace('* **', '').replace('**', '')).bold = True
        else:
            # Adiciona um parágrafo normal
            doc.add_paragraph(linha)

    try:
        doc.save(nome_arquivo)
        print(f"✅ Documento '{nome_arquivo}' salvo com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao salvar o arquivo .docx: {e}")

if __name__ == "__main__":
    if not prompt_usuario.strip():
        print("❌ Erro: A variável 'prompt_usuario' está vazia. Cole o código a ser documentado dentro dela.")
    else:
        conteudo_gerado = gerar_conteudo_com_ia(INSTRUCOES_IA, prompt_usuario, modelo_ia)
        if conteudo_gerado:
            criar_docx_formatado(conteudo_gerado, nome_arquivo_saida)