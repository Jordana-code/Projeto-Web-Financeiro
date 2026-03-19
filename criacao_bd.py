import sqlite3
# Codigo que serviu como teste pra criação do bd - posto dentro do main.py

conn = sqlite3.connect("financas.db")
cursor = conn.cursor()

print("Criando tabelas...")


cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS info_financeira (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    salario REAL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS gastos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    tipo TEXT, -- Aqui vai 'Essencial', 'Lazer', 'Dividas' ou 'Investimento'
    valor REAL,
    data TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
)
""")


usuario_existe = cursor.fetchone()

if not usuario_existe:
    print("Inserindo usuário de teste...")
    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", 
                   ('Usuario Teste', 'teste@email.com', '123456'))

conn.commit()
conn.close()

print("Banco de dados configurado com sucesso!")