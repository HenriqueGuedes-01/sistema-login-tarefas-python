import json
import os

ARQUIVO_DADOS = "dados.json"


def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return {}

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()
            if not conteudo:
                return {}
            return json.loads(conteudo)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def salvar_dados(usuarios):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)


def criar_conta(usuarios):
    print("\n=== CRIAR CONTA ===")
    usuario = input("Digite um nome de usuário: ").strip()

    if not usuario:
        print("O nome de usuário não pode ficar vazio.")
        return

    if usuario in usuarios:
        print("Esse usuário já existe.")
        return

    senha = input("Digite uma senha: ").strip()

    if not senha:
        print("A senha não pode ficar vazia.")
        return

    usuarios[usuario] = {
        "senha": senha,
        "tarefas": []
    }

    salvar_dados(usuarios)
    print("Conta criada com sucesso!")


def login(usuarios):
    print("\n=== LOGIN ===")
    usuario = input("Usuário: ").strip()
    senha = input("Senha: ").strip()

    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        print(f"Login realizado com sucesso. Bem-vindo, {usuario}!")
        menu_usuario(usuario, usuarios)
    else:
        print("Usuário ou senha incorretos.")


def adicionar_tarefa(usuario, usuarios):
    print("\n=== ADICIONAR TAREFA ===")
    tarefa = input("Digite a tarefa: ").strip()

    if not tarefa:
        print("A tarefa não pode ficar vazia.")
        return

    usuarios[usuario]["tarefas"].append({
        "descricao": tarefa,
        "concluida": False
    })

    salvar_dados(usuarios)
    print("Tarefa adicionada com sucesso!")


def listar_tarefas(usuario, usuarios):
    print("\n=== SUAS TAREFAS ===")
    tarefas = usuarios[usuario]["tarefas"]

    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    todas_concluidas = True

    for i, tarefa in enumerate(tarefas, start=1):
        status = "[X]" if tarefa["concluida"] else "[ ]"
        print(f"{i}. {tarefa['descricao']} {status}")

        if not tarefa["concluida"]:
            todas_concluidas = False

    if todas_concluidas:
        print("\n🎉 Parabéns, você concluiu todas as tarefas!")


def concluir_tarefa(usuario, usuarios):
    print("\n=== CONCLUIR TAREFA ===")
    tarefas = usuarios[usuario]["tarefas"]

    if not tarefas:
        print("Você não tem tarefas para concluir.")
        return

    listar_tarefas(usuario, usuarios)

    try:
        numero = int(input("Digite o número da tarefa que deseja concluir: "))
        indice = numero - 1

        if 0 <= indice < len(tarefas):
            if tarefas[indice]["concluida"]:
                print("Essa tarefa já está concluída.")
                return

            tarefas[indice]["concluida"] = True
            salvar_dados(usuarios)
            print("Tarefa marcada como concluída!")

            if all(tarefa["concluida"] for tarefa in tarefas):
                print("🎉 Parabéns, você concluiu todas as tarefas!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Digite um número válido.")


def editar_tarefa(usuario, usuarios):
    print("\n=== EDITAR TAREFA ===")
    tarefas = usuarios[usuario]["tarefas"]

    if not tarefas:
        print("Nenhuma tarefa cadastrada para editar.")
        return

    listar_tarefas(usuario, usuarios)

    try:
        numero = int(input("Digite o número da tarefa que deseja editar: "))
        indice = numero - 1

        if 0 <= indice < len(tarefas):
            nova_descricao = input("Digite a nova descrição da tarefa: ").strip()

            if not nova_descricao:
                print("A descrição não pode ficar vazia.")
                return

            tarefas[indice]["descricao"] = nova_descricao
            salvar_dados(usuarios)
            print("Tarefa editada com sucesso!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Digite um número válido.")


def remover_tarefa(usuario, usuarios):
    print("\n=== REMOVER TAREFA ===")
    tarefas = usuarios[usuario]["tarefas"]

    if not tarefas:
        print("Nenhuma tarefa cadastrada para remover.")
        return

    listar_tarefas(usuario, usuarios)

    try:
        numero = int(input("Digite o número da tarefa que deseja remover: "))
        indice = numero - 1

        if 0 <= indice < len(tarefas):
            tarefa_removida = tarefas.pop(indice)
            salvar_dados(usuarios)
            print(f"Tarefa '{tarefa_removida['descricao']}' removida com sucesso!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Digite um número válido.")


def menu_usuario(usuario, usuarios):
    while True:
        print("\n=== MENU DO USUÁRIO ===")
        print("1. Adicionar tarefa")
        print("2. Listar tarefas")
        print("3. Concluir tarefa")
        print("4. Editar tarefa")
        print("5. Remover tarefa")
        print("6. Sair da conta")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            adicionar_tarefa(usuario, usuarios)
        elif opcao == "2":
            listar_tarefas(usuario, usuarios)
        elif opcao == "3":
            concluir_tarefa(usuario, usuarios)
        elif opcao == "4":
            editar_tarefa(usuario, usuarios)
        elif opcao == "5":
            remover_tarefa(usuario, usuarios)
        elif opcao == "6":
            print("Saindo da conta...")
            break
        else:
            print("Opção inválida.")


def menu_principal():
    usuarios = carregar_dados()

    while True:
        print("\n=== SISTEMA DE LOGIN E TAREFAS ===")
        print("1. Criar conta")
        print("2. Fazer login")
        print("3. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            criar_conta(usuarios)
        elif opcao == "2":
            login(usuarios)
        elif opcao == "3":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida.")


menu_principal()