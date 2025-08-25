# Gerador de Documentação de Código com IA

API Web que utiliza Inteligência Artificial para analisar arquivos de código-fonte em Python (.py) e Pascal (.pas) e gerar uma documentação técnica completa em formato .docx. O objetivo é automatizar e agilizar o processo de documentação, tornando-o mais eficiente para desenvolvedores e equipes.

## ⚙️ Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/2.3.x/)
- [LangChain](https://python.langchain.com/)
- Python-DOCX
- Python-Dotenv

## 📑 Tópicos

- [1 - Estrutura](#1-estrutura)
- [2 - Funcionalidades](#2-funcionalidades)
- [3 - Frontend](#3-frontend)
- [4 - Suporte](#4-suporte)

## <a id="1-estrutura"></a>1 - Estrutura 🏗️

A aplicação foi desenvolvida em Python 3.12+. A estrutura foi organizada em módulos para promover legibilidade, escalabilidade e facilidade de manutenção.

### 📁 Estrutura de Diretórios

```text
📂 gerador_doc_robos/
├── 📂 app/
│ ├── 🐍 functions.py
│ └── 🐍 prompts.py
├── 📂 docs/
├── 📂 templates/
│ ├── 🌐 index.html
│ └── 🌐 resultados.html
├── 📂 uploads/
├── 🐍 main.py
├── 📄 .env
├── 📄 .gitignore
└── 📄 requirements.txt
```

### 📦 Organização dos Módulos

- `main.py`: O coração da aplicação. Contém o servidor web Flask, define as rotas (`/, /gerar, /download`), e orquestra todo o processo de upload, análise e geração de documentos.
- `app/functions.py`: Contém a lógica de negócio principal, incluindo as funções para ler arquivos `.py` e `.pas`, a comunicação com a API do Gemini para gerar a documentação, e a criação do arquivo `.docx` formatado.
- `app/prompts.py`: Armazena o prompt detalhado que instrui a Inteligência Artificial sobre como analisar o código e formatar a resposta.
- `templates/`: Contém os arquivos HTML da interface do usuário.
  - `index.html`: A página inicial com o formulário de upload.
  - `resultados.html`: A página que exibe os links para download dos documentos gerados ou as mensagens de erro.
- `uploads/`: Pasta temporária para onde os arquivos de código são enviados antes do processamento. Os arquivos são excluídos automaticamente após o uso.
- `docs/`: Pasta de saída onde os arquivos `.docx` gerados são salvos.

## <a id="2-funcionalidades"></a>2 - Funcionalidades 🚀

A aplicação web possui uma funcionalidade central exposta através de algumas rotas simples.

### `GET /`

**Descrição:** Exibe a página principal da aplicação com o formulário para upload de arquivos.

**Resposta:** Página HTML (index.html).

### `POST /gerar`

**Descrição:** Rota principal que recebe os arquivos de código para processamento.

**Parâmetros (multipart/form-data):**
-
  - **arquivos:** Um ou mais arquivos com extensão `.py` ou `.pas` para serem analisados
  - **contexto:** Um campo de texto opcional com contexto adicional para a IA.

**Fluxo:**

1. Salva os arquivos temporariamente na pasta `uploads/`.
2. Lê o conteúdo de cada arquivo.
3. Envia o conteúdo para a IA do Gemini junto com o prompt.
4. Recebe a documentação gerada pela IA.
5. Cria um arquivo .docx formatado na pasta `docs/`.
6. Exclui o arquivo temporário da pasta `uploads/`.
7. Renderiza a página resultados.html com os links para download ou mensagens de erro.
8. Resposta: Página HTML (resultados.html).

### `GET /download/<filename>`

**Descrição:** Permite o download de um documento .docx gerado.

**Parâmetros de rota:**
-
   - **filename (string):** O nome do arquivo a ser baixado (ex: DOC_meu_script.py.docx).
   - **Resposta:** O arquivo .docx solicitado.

## <a id="3-frontend"></a>3 - Frontend 🌐

A interface do usuário é simples e funcional, projetada para ser intuitiva.

### Tela Inicial
A tela inicial apresenta um formulário claro onde o usuário pode:
-
   - Selecionar um ou mais arquivos de código (`.py` ou `.pas`).
   - Adicionar um contexto opcional em uma caixa de texto para guiar a IA.
   - Clicar no botão "Gerar Documentação" para iniciar o processo.

### Tela de Espera
Após o envio, o formulário é substituído por um indicador de carregamento animado e uma mensagem "Gerando documentação, por favor aguarde...". Isso informa ao usuário que o processamento está em andamento, o que é crucial para operações que podem levar vários segundos.

### Tela de Resultados
Ao final do processo, o usuário é direcionado para uma página de resultados que exibe:
-
   - Uma lista de "Documentos Gerados com Sucesso", com um link para download para cada arquivo.
   - Uma lista de "Ocorreram Erros", detalhando qualquer falha que tenha acontecido durante o processamento de algum arquivo.
   - Um botão para "Voltar e Gerar Nova Documentação".

A comunicação entre o frontend e o backend é feita através de requisições HTTP padrão, com o JavaScript gerenciando a exibição do indicador de carregamento para melhorar a experiência do usuário.

## <a id="4-suporte"></a>4 - Suporte 🛠

Se tiver dúvidas, sugestões ou encontrar algum erro, sinta-se à vontade para abrir uma issue no repositório do projeto.