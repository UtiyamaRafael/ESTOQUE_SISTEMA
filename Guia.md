# 🎓 Guia de Aprendizado — Construindo um Sistema de Estoque do Zero

Este guia documenta, passo a passo, todo o caminho para construir um backend de sistema de estoque com **Python + FastAPI + MySQL + SQLAlchemy**, pensado para quem está começando agora. A ideia não é copiar código pronto, e sim **entender o porquê de cada etapa** — cada seção explica o conceito antes do comando.

---

## Sumário

1. [Etapa 1 — Planejamento e modelagem de dados](#etapa-1)
2. [Etapa 2 — Configurando o ambiente Python](#etapa-2)
3. [Etapa 3 — Primeiro servidor com FastAPI](#etapa-3)
4. [Etapa 4 — Instalando e configurando o MySQL](#etapa-4)
5. [Etapa 5 — Criando as tabelas em SQL puro (DDL)](#etapa-5)
6. [Etapa 6 — Conectando o Python ao MySQL](#etapa-6)
7. [Etapa 7 — Mapeando as tabelas com SQLAlchemy (models)](#etapa-7)
8. [Glossário rápido](#glossario)
9. [Erros comuns e como resolver](#erros-comuns)

---

<a name="etapa-1"></a>
## Etapa 1 — Planejamento e modelagem de dados

**Antes de escrever qualquer código**, é essencial saber o que o sistema precisa guardar. Pular essa etapa é a causa mais comum de retrabalho em projetos de iniciantes.

### Perguntas para guiar o planejamento

1. **Quais entidades (tabelas) o sistema precisa?**
   Pense em "substantivos importantes" do domínio: quem usa o sistema, o que é controlado, o que registra eventos.

2. **Que informações (campos) cada entidade precisa ter?**
   Pense no mínimo necessário para a entidade fazer sentido sozinha.

3. **Como as entidades se relacionam?**
   Uma entidade pode "pertencer" a outra? Um produto tem uma categoria. Uma movimentação pertence a um produto e foi feita por um usuário.

### Resultado esperado desta etapa

Um diagrama (pode ser desenhado à mão, ou em ferramentas como [dbdiagram.io](https://dbdiagram.io)) com as tabelas, seus campos e as setas de relacionamento entre elas.

### Modelo usado neste projeto

```
CATEGORIAS (id, nome)
USUARIO (id, nome, email, senha, is_admin)
PRODUTOS (id, codigo, nome, quantidade, categoria_id → FK, qtd_min, preco_custo, preco_venda)
MOVIMENTACAO (id, produto_id → FK, usuario_id → FK, tipo, quantidade, motivo, data)
```

### Conceitos-chave desta etapa

- **Chave primária (Primary Key / PK):** campo único que identifica cada linha de uma tabela (geralmente `id`).
- **Chave estrangeira (Foreign Key / FK):** campo que "aponta" para o `id` de outra tabela, criando um relacionamento. Exemplo: `categoria_id` em `PRODUTOS` aponta para `id` em `CATEGORIAS`.
- **Quando usar uma tabela separada vs. um campo simples:**
  - Se o valor é digitado livremente e pode crescer com o tempo (ex: categorias de produto) → tabela separada.
  - Se o valor é uma lista pequena e fixa, controlada pelo próprio sistema (ex: admin/comum) → campo simples (booleano ou enum), sem precisar de tabela.

---

<a name="etapa-2"></a>
## Etapa 2 — Configurando o ambiente Python (Windows)

### 2.1 Instalar o Python

⚠️ **Atenção:** o site python.org atualmente oferece dois instaladores diferentes — o clássico e o novo "Python Install Manager". **Use o instalador clássico**, pois o novo organiza os arquivos de forma não padrão e pode causar problemas com o `pip` e o `PATH`.

1. Acesse `https://www.python.org/downloads/windows/`
2. Baixe o link **"Windows installer (64-bit)"** de uma versão estável (ex: 3.13.x) — não use o botão amarelo grande da home, que pode levar ao novo instalador.
3. Ao instalar, marque a caixa **"Add python.exe to PATH"** antes de clicar em Install Now.

### 2.2 Verificar a instalação

Feche e abra um terminal novo (o PATH só atualiza em terminais novos), depois rode:

```bash
python --version
pip --version
```

Ambos devem retornar um número de versão, sem erro.

### 2.3 Criar a pasta do projeto e o ambiente virtual

Um **ambiente virtual (venv)** isola as bibliotecas de um projeto, evitando conflitos entre projetos diferentes que usam versões diferentes da mesma biblioteca.

```bash
cd caminho\para\seu\projeto
python -m venv venv
```

### 2.4 Ativar o ambiente virtual

```bash
venv\Scripts\activate
```

Se o terminal passar a mostrar `(venv)` no início da linha, funcionou. **Todo comando `pip install` deve ser rodado com o venv ativo.**

---

<a name="etapa-3"></a>
## Etapa 3 — Primeiro servidor com FastAPI

### 3.1 Instalar as bibliotecas

```bash
pip install fastapi uvicorn
```

- **FastAPI**: framework que define as rotas da API.
- **Uvicorn**: servidor que efetivamente executa a aplicação.

### 3.2 Criar o `main.py`

Na raiz do projeto (não dentro da pasta `venv`):

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def raiz():
    return {"mensagem": "API funcionando"}
```

- `@app.get("/")` é um **decorator**: associa a função abaixo dele à rota `/` usando o método HTTP `GET`.
- O dicionário retornado é convertido automaticamente para JSON.

### 3.3 Rodar o servidor

```bash
uvicorn main:app --reload
```

- `main:app` → "no arquivo `main.py`, use o objeto `app`".
- `--reload` → reinicia o servidor automaticamente a cada alteração salva no código.

Acesse `http://127.0.0.1:8000` (deve mostrar a mensagem) e `http://127.0.0.1:8000/docs` (documentação interativa gerada automaticamente).

---

<a name="etapa-4"></a>
## Etapa 4 — Instalando e configurando o MySQL

### 4.1 Baixar e instalar

1. Acesse `https://dev.mysql.com/downloads/installer/`
2. Baixe o **"mysql-installer-community"** (o arquivo maior, ~500MB — a versão "web" depende de baixar tudo durante a instalação, o que pode falhar).
3. No tipo de instalação, escolha **"Full"** (ou "Developer Default", dependendo da versão do instalador).
4. Defina uma **senha para o usuário `root`** — anote em local seguro, ela será usada em toda conexão.
5. Mantenha a porta padrão **3306**.

### 4.2 Criar o banco de dados

Pode ser feito via terminal (`mysql -u root -p`) ou visualmente pelo **DBeaver**, conectando com host `localhost`, porta `3306`, usuário `root` e a senha definida:

```sql
CREATE DATABASE estoque;
```

---

<a name="etapa-5"></a>
## Etapa 5 — Criando as tabelas em SQL puro (DDL)

### Database-first vs. Code-first

Existem duas abordagens comuns para criar a estrutura de um banco usado com um ORM:

| Abordagem | Como funciona | Vantagem |
|---|---|---|
| **Code-first** | Escreve-se as classes Python primeiro; o ORM gera as tabelas automaticamente | Tudo versionado no código; menos SQL manual |
| **Database-first** | As tabelas são criadas manualmente em SQL; as classes Python são escritas para espelhar essa estrutura | Controle total sobre o SQL; ótima prática de sintaxe SQL pura |

Este projeto usa **database-first**.

### 5.1 Ordem de criação importa

Tabelas que são referenciadas por uma `FOREIGN KEY` precisam existir **antes** da tabela que as referencia. Ordem usada aqui: `categorias` e `usuario` primeiro (não dependem de nada), depois `produtos` (depende de `categorias`), depois `movimentacao` (depende de `produtos` e `usuario`).

### 5.2 Sintaxe base

```sql
CREATE TABLE nome_da_tabela (
    coluna1 TIPO restricoes,
    coluna2 TIPO restricoes,
    PRIMARY KEY (coluna1)
);
```

Tipos comuns usados em MySQL:

| Tipo | Uso |
|---|---|
| `INT` | números inteiros |
| `VARCHAR(n)` | texto com tamanho máximo definido |
| `DECIMAL(p, s)` | números decimais precisos — **sempre usar para dinheiro**, nunca `FLOAT` |
| `BOOLEAN` | verdadeiro/falso |
| `DATETIME` | data e hora |
| `ENUM('valor1', 'valor2', ...)` | lista fixa de valores válidos |
| `AUTO_INCREMENT` | gera o próximo número da chave primária automaticamente |

### 5.3 Chave estrangeira

```sql
FOREIGN KEY (coluna_local) REFERENCES tabela_referenciada(coluna_referenciada)
```

### 5.4 Adicionando coluna ou constraint depois da criação (ALTER TABLE)

```sql
-- Adicionar uma coluna nova:
ALTER TABLE produtos
ADD COLUMN quantidade INT;

-- Adicionar uma ou mais foreign keys numa tabela já existente:
ALTER TABLE movimentacao
ADD FOREIGN KEY (produto_id) REFERENCES produtos(id),
ADD FOREIGN KEY (usuario_id) REFERENCES usuario(id);
```

> `CREATE TABLE` define tudo de uma vez, na criação. `ALTER TABLE` modifica uma tabela que já existe — por isso precisa da palavra `ADD` para deixar explícito o que está sendo adicionado a uma estrutura já existente.

### 5.5 Como confirmar que uma Foreign Key está funcionando de verdade

Não basta o comando rodar sem erro — o teste real é tentar violar a regra de propósito:

```sql
INSERT INTO movimentacao (produto_id, usuario_id, tipo, quantidade)
VALUES (9999, 9999, 'entrada', 10);
```

Se a constraint estiver ativa, o banco deve **recusar** essa inserção com um erro do tipo `"Cannot add or update a child row: a foreign key constraint fails"`. Se aceitar sem reclamar, a constraint não foi aplicada corretamente.

---

<a name="etapa-6"></a>
## Etapa 6 — Conectando o Python ao MySQL

### 6.1 Instalar SQLAlchemy e o driver do MySQL

```bash
pip install sqlalchemy pymysql
```

- **SQLAlchemy**: ORM (Object-Relational Mapping) — permite representar tabelas do banco como classes Python, e trabalhar com dados sem escrever SQL manualmente na maior parte do tempo.
- **PyMySQL**: driver que permite ao SQLAlchemy efetivamente "falar" com um banco MySQL (o SQLAlchemy sozinho não sabe se comunicar com nenhum banco específico).

### 6.2 Criar `database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("mysql+pymysql://root:SUASENHA@localhost:3306/estoque")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

Estrutura da URL de conexão:

```
mysql+pymysql://USUARIO:SENHA@HOST:PORTA/NOME_DO_BANCO
```

| Peça | O que é |
|---|---|
| `engine` | representa a conexão com o banco |
| `SessionLocal` | fábrica de "sessões" — cada conversa com o banco (inserir, buscar, etc.) acontece dentro de uma sessão |
| `Base` | classe da qual todas as classes de tabela (models) devem herdar |

⚠️ Se a senha tiver caracteres especiais (`@`, `#`, `%`), eles podem quebrar a URL de conexão e precisam ser tratados (codificação de URL).

---

<a name="etapa-7"></a>
## Etapa 7 — Mapeando as tabelas com SQLAlchemy (`models.py`)

Cada tabela do banco vira uma classe Python. Cada coluna vira um atributo `Column(...)`.

### 7.1 Exemplo simples (tabela sem foreign key)

```python
from sqlalchemy import Column, Integer, String
from database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
```

- `__tablename__` precisa bater **exatamente** com o nome da tabela no banco.
- `primary_key=True` já implica auto-incremento para colunas `Integer` — não é necessário declarar isso à parte.

### 7.2 Tipos de coluna mais usados

| SQL (MySQL) | SQLAlchemy |
|---|---|
| `INT` | `Integer` |
| `VARCHAR(n)` | `String(n)` |
| `DECIMAL(p, s)` | `Numeric(p, s)` |
| `BOOLEAN` | `Boolean` |
| `DATETIME` | `DateTime` |
| `ENUM(...)` | `Enum(...)` |

### 7.3 Foreign key em SQLAlchemy

```python
from sqlalchemy import ForeignKey

categoria_id = Column(Integer, ForeignKey("categorias.id"))
```

O formato dentro do `ForeignKey(...)` é sempre `"nome_da_tabela.nome_da_coluna"`, em minúsculo, igual ao nome real no banco.

### 7.4 Testando a conexão

Depois de criar todas as classes, é possível testar se o SQLAlchemy consegue de fato consultar o banco:

```python
from database import SessionLocal
from models import Categoria

db = SessionLocal()
categorias = db.query(Categoria).all()
print(categorias)
db.close()
```

Se a tabela estiver vazia, o resultado esperado é `[]` (lista vazia) — isso já confirma que a conexão e o mapeamento estão corretos.

---

<a name="glossario"></a>
## Glossário rápido

| Termo | Significado |
|---|---|
| **ORM** | Object-Relational Mapping — biblioteca que permite manipular um banco de dados usando classes/objetos em vez de SQL puro |
| **DDL** | Data Definition Language — comandos que definem a estrutura do banco (`CREATE`, `ALTER`, `DROP`) |
| **DML** | Data Manipulation Language — comandos que manipulam os dados (`INSERT`, `UPDATE`, `DELETE`, `SELECT`) |
| **venv** | ambiente virtual Python — isola as bibliotecas de um projeto |
| **PATH** | variável do sistema operacional que diz onde procurar programas quando você digita um comando no terminal |
| **PK (Primary Key)** | campo que identifica unicamente cada linha de uma tabela |
| **FK (Foreign Key)** | campo que referencia o `id` de outra tabela, criando um relacionamento |
| **Migration** | (próximo conceito a estudar) forma de versionar alterações na estrutura do banco ao longo do tempo |

---

<a name="erros-comuns"></a>
## Erros comuns e como resolver

### `'pip' não é reconhecido como um comando interno ou externo`
O `pip` não está no PATH do Windows. Tente `python -m pip` no lugar de `pip`, ou reinstale o Python usando o instalador clássico com "Add python.exe to PATH" marcado.

### Erro ao rodar `pip install` sem o venv ativo
As bibliotecas vão para o Python global em vez de ficarem isoladas no projeto. Sempre confirme que aparece `(venv)` no início da linha do terminal antes de instalar algo.

### `Can't connect to MySQL server` (ao rodar o Python)
Verifique se o serviço do MySQL está rodando (pode conferir no "Serviços" do Windows, procurando por "MySQL"), se a porta está correta (3306) e se a senha no `database.py` está certa.

### `Table 'estoque.nome_tabela' doesn't exist`
O `__tablename__` da classe Python não bate exatamente com o nome da tabela no MySQL (atenção a plural/singular e maiúsculas/minúsculas).

### Foreign key aceitando valores inválidos
A constraint pode não ter sido criada de fato. Confirme rodando um `INSERT` de teste com um ID inexistente (ver seção 5.5) e revise a estrutura da tabela no DBeaver (aba "Foreign Keys"/"Constraints").
