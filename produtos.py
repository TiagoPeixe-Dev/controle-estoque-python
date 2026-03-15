from banco import conectar
from datetime import datetime

def cadastrar_produto():
    conn = conectar()
    cursor = conn.cursor()

    nome = input("Nome do produto: ")

    cursor.execute(
        "SELECT * FROM produtos WHERE nome= ?",
        (nome,)
    )


    produto_existente = cursor.fetchone()

    if produto_existente:
        print("Erro: produto já cadastrado.\n")
        conn.close()
        return

    try:
        quantidade = int(input("Quantidade inicial: "))
        estoque_minimo = int(input("Estoque mínimo: "))
    except ValueError:
        print("Erro: quantidade deve ser número.")
        conn.close()
        return
    cursor.execute(
        "INSERT INTO produtos (nome, quantidade, estoque_minimo) VALUES (?,?,?)",
        (nome, quantidade, estoque_minimo)
    )

    conn.commit()
    conn.close()

    print("Produto cadastrado com sucesso.\n")

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    print("\n=============== ESTOQUE ===============")

    print(f"{'ID':<5}{'PRODUTO':<20}{'QUANTIDADE':<15}{'MINIMO':<10}{'ALERTA'}")
    print("-" * 60)

    for p in produtos:
        id_produto, nome, quantidade, minimo = p

        alerta = ""
        if quantidade < minimo:
            alerta = "\u26A0"
            print(f"{alerta} ATENÇÃO: ESTOQUE BAIXO! {alerta}")

        print(f"{id_produto:<5}{nome:<20}{quantidade:<15}{minimo:<10}{alerta}")

    print()

    conn.close()


def entrada_produto():
    conn = conectar()
    cursor = conn.cursor()

    listar_produtos()

    try:
        id_produto = int(input("ID do produto: "))
        quantidade = int(input("Quantidade de entrada: "))
    except ValueError:
        print("Erro: valor deve ser número.")
        conn.close()
        return
    
    cursor.execute(
        "SELECT * FROM produtos WHERE id=?",
        (id_produto,)
    )

    produto = cursor.fetchone()

    if not produto:
        print("Erro: produto não encontrado.")
        conn.close()
        return

    cursor.execute(
        "UPDATE produtos SET quantidade = quantidade + ? WHERE id=?",
        (quantidade, id_produto)
    )

    cursor.execute(
        "INSERT INTO movimentacoes (produto_id, tipo, quantidade, data) VALUES (?,?,?,?)",
        (id_produto, "entrada", quantidade, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()

    print("Entrada registrada.\n")

def saida_produto():
    conn = conectar()
    cursor = conn.cursor()

    listar_produtos()

    try:
        id_produto = int(input("ID do produto: "))
        quantidade = int(input("Quantidade de saída: "))
    except ValueError:
        print("Erro: valor deve ser número.")
        conn.close()
        return
    
    cursor.execute(
        "SELECT quantidade FROM produtos WHERE id=?",
        (id_produto,)
    )

    resultado = cursor.fetchone()

    if not resultado:
        print("Produto não encontrado.")
        conn.close()
        return
    estoque_atual = resultado[0]

    if quantidade > estoque_atual:
        print("Erro: estoque insuficiente")
        conn.close()
        return
    
    cursor.execute(
        "UPDATE produtos SET quantidade = quantidade - ? WHERE id=?",
        (quantidade, id_produto)
    )

    cursor.execute(
        "INSERT INTO movimentacoes (produto_id, tipo, quantidade, data) VALUES (?,?,?,?)",
        (id_produto, "saida", quantidade, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()

    print("Saída registrada.\n")

def listar_movimentacoes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT m.id, p.nome, m.tipo, m.quantidade, m.data
    FROM movimentacoes m
    JOIN produtos p ON m.produto_id = p.id
    ORDER BY m.data DESC
    """)

    movimentacoes = cursor.fetchall()

    print("\n=========== HISTÓRICO DE MOVIMENTAÇÕES ===========")

    print(f"{'ID':<5}{'PRODUTO':<20}{'TIPO':<10}{'QTD':<10}{'DATA'}")
    print("-" * 60)

    for m in movimentacoes:
        id_mov, produto, tipo, quantidade, data = m
        print(f"{id_mov:<5}{produto:<20}{tipo:<10}{quantidade:<10}{data}")

    print()

    conn.close()

def editar_produto():
    conn = conectar()
    cursor = conn.cursor()

    listar_produtos()

    try:
        id_produto = int(input("Digite o ID do produto que deseja editar: "))
    except ValueError:
        print("Erro: ID deve ser número.")
        conn.close()
        return

    cursor.execute(
        "SELECT * FROM produtos WHERE id=?",
        (id_produto,)
    )

    produto = cursor.fetchone()

    if not produto:
        print("Produto não encontrado.")
        conn.close()
        return

    print("\nDigite os novos dados do produto:")

    nome = input("Novo nome: ")

    try:
        quantidade = int(input("Nova quantidade: "))
        estoque_minimo = int(input("Novo estoque mínimo: "))
    except ValueError:
        print("Erro: valores devem ser números.")
        conn.close()
        return

    cursor.execute(
        "UPDATE produtos SET nome=?, quantidade=?, estoque_minimo=? WHERE id=?",
        (nome, quantidade, estoque_minimo, id_produto)
    )

    conn.commit()
    conn.close()

    print("Produto atualizado com sucesso.\n")

def excluir_produto():
    conn = conectar()
    cursor = conn.cursor()

    listar_produtos()

    try:
        id_produto = int(input("Digite o ID do produto que deseja excluir: "))
    except ValueError:
        print("Erro: ID deve ser número.")
        conn.close()
        return

    cursor.execute(
        "SELECT * FROM produtos WHERE id=?",
        (id_produto,)
    )

    produto = cursor.fetchone()

    if not produto:
        print("Produto não encontrado.")
        conn.close()
        return

    confirmacao = input("Tem certeza que deseja excluir este produto? (s/n): ")

    if confirmacao.lower() != "s":
        print("Exclusão cancelada.")
        conn.close()
        return

    cursor.execute(
        "DELETE FROM produtos WHERE id=?",
        (id_produto,)
    )

    conn.commit()
    conn.close()

    print("Produto excluído com sucesso.\n")