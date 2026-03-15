from banco import conectar

def login():
    conn = conectar()
    cursor = conn.cursor()

    usuario = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")

    cursor.execute(
       "SELECT usuario, perfil FROM usuarios WHERE usuario = ? AND senha = ?",
         (usuario, senha)
    )
    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        print(f"Bem-vindo, {usuario}!")
        return resultado  # Retorna o perfil do usuário
    else:
        print("Usuário ou senha incorretos.")
        return None
    
def cadastrar_usuario(perfil_logado):
    if perfil_logado != "admin":
        print("Acesso negado. Apenas administradores podem cadastrar novos usuários.")
        return

    conn = conectar()
    cursor = conn.cursor()

    usuario = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")
    perfil = input("Digite o perfil do usuário admin/comum: ")

    cursor.execute(
        "INSERT INTO usuarios (usuario, senha, perfil) VALUES (?, ?, ?)",
        (usuario, senha, perfil)
    )

    conn.commit()
    conn.close()

    print("Usuário cadastrado com sucesso.")

