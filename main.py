estoque = {}

while True:
    print("\n1 - Entrada de Produto ")
    print("2 - Saída do Produto")
    print("3 - Ver estoque ")
    print("4 - Sair ")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        produto = input("Produto: ").lower()
        quantidade = int(input("Quantidade de entrada: "))

        if produto in estoque:
            estoque[produto] += quantidade
        else:
            estoque[produto] = quantidade
            print("Estoque atualizado!")

    elif opcao == "2":
        produto = input("Produto: ").lower()
        quantidade = int(input("Quantidade de saída: "))
        hora = float(input("Horário de saída: "))

        if produto in estoque and estoque[produto] >= quantidade:
            estoque[produto] -= quantidade
            print("Saída confirmada!")
        else:
            print("Produto inexistente ou estoque insuficiente!")

    elif opcao == "3":
        print("\nEstoque:")

        if estoque:
            for produto, quantidade in estoque.items():
                print(f"{produto}: {quantidade}")
        else:
            print("Estoque Vazio ou Produto não cadastrado")

    else:
        print("Opção Inválida.")
        break
