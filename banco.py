import sqlite3

def conectar():
    return sqlite3.connect("estoque.db")


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    senha TEXT NOT NULL,
    perfil TEXT NOT NULL
)
""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    estoque_minimo INTEGER NOT NULL
)
""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        tipo TEXT,
        quantidade INTEGER,
        data TEXT
    )
    """)
    
    conn.commit()
    conn.close()

def criar_admin_padrao():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
    admin = cursor.fetchone()

    if not admin:
        cursor.execute("""
        INSERT INTO usuarios (usuario, senha, perfil) 
        VALUES ('admin', 'admin', 'admin')
        """)
    conn.commit()
    conn.close()


