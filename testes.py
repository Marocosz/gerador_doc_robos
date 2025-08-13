from functions import ler_conteudo_py

str1, nome_arquivo = ler_conteudo_py(
    "c:\\Users\\marcos.rodrigues\\Documents\\Projetos\\gerador_doc_robos\\main.py")


# Troca crases para evitar quebrar bloco de código markdown
str1_safe = str1.replace("```", "'''")

# Troca três aspas duplas por aspas simples triplas para não confundir delimitadores
str1_safe = str1_safe.replace('"""', "'''")


INSTRUCOES_IA = f"""
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
{nome_arquivo}

**2. CÓDIGO-FONTE DO SCRIPT PYTHON:**
{str1}

Descreva o que acontece quando uma entrada (ex: um e-mail) não corresponde a nenhum dos clientes configurados. Qual é o fluxo de exceção ou o caminho alternativo?
"""

print(nome_arquivo)