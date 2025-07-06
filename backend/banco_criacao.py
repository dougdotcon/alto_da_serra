import sqlite3

# Conexão com o banco (cria o arquivo restaurante.db se não existir)
conn = sqlite3.connect("restaurante.db")
cursor = conn.cursor()

# Execução das tabelas
cursor.executescript("""

CREATE TABLE IF NOT EXISTS configuracoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_restaurante TEXT NOT NULL,
    quantidade_mesas INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS tipos_usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    senha TEXT NOT NULL,
    nome TEXT NOT NULL,
    data_nascimento DATE,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    tipo_usuario_id INTEGER NOT NULL,
    FOREIGN KEY (tipo_usuario_id) REFERENCES tipos_usuarios(id)
);

CREATE TABLE IF NOT EXISTS status_mesas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS mesas (
    id TEXT PRIMARY KEY,
    status_id INTEGER NOT NULL,
    cliente TEXT,
    data_abertura DATETIME,
    valor_total REAL DEFAULT 0.0,
    FOREIGN KEY (status_id) REFERENCES status_mesas(id)
);

CREATE TABLE IF NOT EXISTS tipos_quantidade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_barras TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    data_insercao DATETIME DEFAULT CURRENT_TIMESTAMP,
    lote TEXT,
    marca TEXT,
    tipo_quantidade_id INTEGER NOT NULL,
    data_validade DATE,
    preco_custo REAL NOT NULL,
    preco_venda REAL NOT NULL,
    FOREIGN KEY (tipo_quantidade_id) REFERENCES tipos_quantidade(id)
);

CREATE TABLE IF NOT EXISTS consumo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    quantidade REAL NOT NULL,
    total REAL NOT NULL,
    mesa_id TEXT NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    FOREIGN KEY (mesa_id) REFERENCES mesas(id)
);

""")

conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")
