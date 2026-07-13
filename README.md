# 📦 Sistema de Controle de Estoque

Projeto de portfólio desenvolvido para aprender backend na prática: API em Python (FastAPI) conectada a um banco de dados MySQL via SQLAlchemy.

> Este projeto está sendo construído do zero, com o código escrito manualmente como exercício de aprendizado — sem gerar o código pronto, apenas orientação sobre os próximos passos.

## Status atual

- [x] Planejamento do modelo de dados (diagrama com Produtos, Categorias, Usuário, Movimentação)
- [x] Ambiente Python configurado (instalação clássica + `venv`)
- [x] MySQL instalado e banco `estoque` criado
- [x] Tabelas criadas via SQL puro (DDL) no DBeaver, com chaves estrangeiras
- [x] Conexão configurada (`database.py`)
- [x] Modelos SQLAlchemy espelhando as tabelas (`models.py`)
- [x] Teste de leitura via SQLAlchemy
- [ ] Rotas da API (CRUD de produtos)
- [ ] Autenticação de usuários
- [ ] Movimentação de estoque (entrada/saída)
- [ ] Relatórios
- [ ] Frontend

## Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python |
| Framework web | FastAPI |
| Servidor | Uvicorn |
| Banco de dados | MySQL |
| ORM | SQLAlchemy |
| Driver do banco | PyMySQL |
| Cliente de banco (GUI) | DBeaver |
| Sistema operacional | Windows |

## Modelo de dados

```
CATEGORIAS                 USUARIO
├── id (PK)                ├── id (PK)
└── nome                   ├── nome
                            ├── email
PRODUTOS                    ├── senha
├── id (PK)                 └── is_admin
├── codigo
├── nome                   MOVIMENTACAO
├── quantidade             ├── id (PK)
├── categoria_id (FK) ──┐  ├── produto_id (FK) ──┐
├── qtd_min             │  ├── usuario_id (FK) ───┼──┐
├── preco_custo         │  ├── tipo (entrada/saida)│  │
└── preco_venda         │  ├── quantidade          │  │
                         │  ├── motivo              │  │
        categorias.id ◄─┘  └── data                │  │
                                  produtos.id ◄──────┘  │
                                  usuario.id  ◄──────────┘
```

## Estrutura do projeto

```
estoque-sistema/
├── venv/            # ambiente virtual (não versionar / não mexer manualmente)
├── main.py          # ponto de entrada da API (rotas do FastAPI)
├── database.py       # configuração da conexão com o MySQL
├── models.py         # classes Python que espelham as tabelas do banco
└── requirements.txt  # (a criar) lista de dependências do projeto
```

## Como rodar o projeto

### 1. Pré-requisitos
- Python instalado (instalador clássico de python.org, com "Add python.exe to PATH" marcado)
- MySQL Server instalado e rodando (porta padrão `3306`)
- Banco de dados `estoque` criado, com as tabelas já definidas (ver seção DDL abaixo)

### 2. Ativar o ambiente virtual

```bash
cd estoque-sistema
venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install fastapi uvicorn sqlalchemy pymysql
```

### 4. Configurar a conexão

No arquivo `database.py`, ajuste a senha do MySQL:

```python
engine = create_engine("mysql+pymysql://root:SUASENHA@localhost:3306/estoque")
```

### 5. Rodar o servidor

```bash
uvicorn main:app --reload
```

Acesse:
- `http://127.0.0.1:8000` → resposta da API
- `http://127.0.0.1:8000/docs` → documentação interativa (Swagger)

## Script SQL (DDL) das tabelas

Este projeto usa a abordagem **database-first**: as tabelas foram criadas manualmente em SQL, e as classes Python em `models.py` foram escritas para espelhar essa estrutura.

```sql
CREATE DATABASE estoque;
USE estoque;

CREATE TABLE categorias(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100)
);

CREATE TABLE usuario(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    email VARCHAR(255),
    senha VARCHAR(255),
    is_admin BOOLEAN
);

CREATE TABLE produtos(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    CODIGO INT,
    NOME VARCHAR(100),
    CATEGORIA_ID INT,
    QTD_MIN INT,
    PRECO_CUSTO DECIMAL(15,2),
    PRECO_VENDA DECIMAL(15,2),
    quantidade INT,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE movimentacao(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    produto_id INT,
    usuario_id INT,
    tipo ENUM('entrada', 'saida'),
    quantidade INT,
    motivo VARCHAR(255),
    data DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);
```

## Próximos passos planejados

- [ ] Rotas CRUD de produtos (`GET`, `POST`, `PUT`, `DELETE`)
- [ ] Cadastro e login de usuários (hash de senha, JWT)
- [ ] Rota de movimentação de estoque, atualizando a quantidade do produto automaticamente
- [ ] Rotas de relatório (resumo, estoque baixo)
- [ ] Frontend simples (HTML/CSS/JS) consumindo a API
- [ ] Adicionar `.env` para não deixar a senha do banco exposta no código
- [ ] Criar `requirements.txt` com as dependências fixadas

## Notas de segurança (antes de publicar o projeto)

- Nunca deixe a senha do banco de dados direto no código-fonte de um projeto público (GitHub) — use variáveis de ambiente (`.env`)
- Senhas de usuário devem sempre ser armazenadas com hash (nunca em texto puro)
