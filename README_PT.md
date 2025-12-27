# Alto da Serra - Sistema de Gestão para Restaurantes

Um sistema de gestão de desktop projetado especificamente para o restaurante 'Alto da Serra', desenvolvido para otimizar o controle de mesas, gerenciamento de pedidos e processamento de pagamentos.

## ✨ Funcionalidades

*   **Gestão de Mesas:** Abertura, fechamento e visualização do status de todas as mesas em tempo real.
*   **Lançamento de Pedidos:** Adição facilitada de itens de consumo para cada mesa.
*   **Controle de Consumo:** Visualização detalhada dos itens consumidos por mesa.
*   **Pagamentos:** Funcionalidade para pagamentos parciais ou totais de contas.
*   **Interface Intuitiva:** Um painel de controle claro e organizado para uma operação eficiente.

## 🛠️ Tecnologias Utilizadas

*   **Frontend:** [Flet](https://flet.dev/) - Framework para criação de aplicações multi-plataforma em Python.
*   **Backend:** [FastAPI](https://fastapi.tiangolo.com/) - Framework web de alta performance para construção de APIs com Python.
*   **Servidor:** [Uvicorn](https://www.uvicorn.org/) - Servidor ASGI para rodar a API FastAPI.
*   **Banco de Dados:** SQLite - Um arquivo de banco de dados (`restaurante.db`) é utilizado para armazenar os dados.

## 📂 Estrutura do Projeto


alto_da_serra/
├── backend/
│   ├── api.py             # Lógica da API (FastAPI)
│   ├── restaurante.db     # Banco de dados SQLite
│   └── ...
├── frontend/
│   ├── login.py           # Tela de Login
│   ├── painel.py          # Painel principal
│   ├── components/        # Componentes da interface (Flet)
│   └── ...
├── requirements.txt       # Dependências do projeto
├── start_local.py         # Script para iniciar a aplicação localmente
└── README.md


## 🚀 Como Começar

Siga as instruções abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

*   [Python 3.8+](https://www.python.org/downloads/)

### Instalação

1.  Clone o repositório para a sua máquina local.
2.  Navegue até o diretório raiz do projeto.
3.  Crie e ative um ambiente virtual (recomendado):
    bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    
4.  Instale as dependências necessárias:
    bash
    pip install -r requirements.txt
    

### Executando a Aplicação

Para iniciar o backend e o frontend simultaneamente, execute o script `start_local.py`:

bash
python start_local.py


O script irá:
1.  Iniciar o servidor backend em `http://127.0.0.1:8000`.
2.  Abrir a aplicação desktop (frontend).

## 🐳 Docker

O projeto também pode ser executado em um contêiner Docker. O `Dockerfile` presente na raiz do projeto contém as instruções para buildar a imagem.
*Ainda a ser implementado em detalhe.*
