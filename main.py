import os
from banco import criar_tabelas, criar_admin_padrao
from usuarios import login, cadastrar_usuario
from produtos import (
    cadastrar_produto,
    listar_produtos,
    entrada_produto,
    saida_produto,
    listar_movimentacoes,
    editar_produto,
    excluir_produto
)


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPressione ENTER para continuar...")

def menu(perfil):
    while True:
        limpar_tela()

        print("1 - Listar produtos")
        print("2 - Cadastrar produto")
        print("3 - Entrada de estoque")
        print("4 - Saída de estoque")
        print("5 - Ver movimentações")
        print("6 - Editar produto")
        print("7 - Excluir produto")
        print("8 - Cadastrar usuário")
        print("9 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_produtos()
            pausar()

        elif opcao == "2":
            cadastrar_produto()
            pausar()

        elif opcao == "3":
            entrada_produto()
            pausar()

        elif opcao == "4":
            saida_produto()
            pausar()

        elif opcao == "5":
            listar_movimentacoes()
            pausar()

        elif opcao == "6":
            editar_produto()
            pausar()

        elif opcao == "7":
            excluir_produto()
            pausar()

        elif opcao == "8":
            cadastrar_usuario(perfil)
            pausar()

        elif opcao == "9":
            print("Encerrando sistema...")
            break

        else:
            print("Opção inválida.\n")


def main():
    criar_tabelas()
    criar_admin_padrao()

    print("=== LOGIN DO SISTEMA ===")

    usuario_logado = None

    while not usuario_logado:
        usuario_logado = login()

    usuario, perfil = usuario_logado

    menu(perfil)


if __name__ == "__main__":
    main()