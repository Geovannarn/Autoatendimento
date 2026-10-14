estoque = {}

while True:
    print("\n1 - Entrada de Produto ")
    print("2 - Saída do Produto")
    print("3 - Ver estoque ")
    print("4 - Corrigir estoque ")
    print("5 - Sair ")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        produto = input("Produto: ").lower()
        quantidade = int(input("Quantidade de entrada: "))
        medida = input("Unidade (kg, l, un, ml): ").lower()
        descricao = input("Descrição do produto: ")

        if produto in estoque:
            estoque[produto] += quantidade
            estoque[produto] = {
               
                "Quantidade": quantidade,
                "Medida": medida,
                "Descrição": descricao

            }
        else:
            estoque[produto] = quantidade
            estoque[produto] = {

                "Quantidade": quantidade,
                "Medida": medida,
                "Descrição": descricao

            }
            print("Estoque atualizado!")

    elif opcao == "2":
        produto = input("Produto: ").lower()
        quantidade = int(input("Quantidade de saída: "))
        hora = float(input("Horário de saída: "))
        unidade = input("Unidade (h): ").lower()


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

    elif opcao == "4":
        print("\nProdutos Cadastrados:")

        if estoque:
            for produto, quantidade in estoque.items():
                print(f"{produto}, {quantidade}")

        produto = input("Produto a ser corrigido: ").lower()
        quantidade = float(input("Nova quantidade:"))
        unidade = input("Unidade (kg, un, L...): ").lower()
        descricao = input("Descrição do produto: ")

        if produto in estoque:
            estoque[produto] = quantidade
            print("Estoque corrigido!")

        else:
            print("Produto não encontrado ou não cadastrado!")

    elif opcao == "5":
        print("Saindo do programa...")
        break
    
produtos = []
while True:
        nome = input("Produtos: ")

        if nome.lower() == "fim":
            break 

        Quantidade = int(input("Quantidade: "))
        preco = float(input("Preço: "))

        produtos.append({
            "Nome": nome,
            "Quantidade" : Quantidade,
            "Preço": Preco,
            "Desconto": Desconto,
            "Descrição": Descrição

        })
subtotal = 0

for produto in produtos:
    subtotal += produto["Quantidade"] * produto["Preço"]

    print(f"Subtotal: R$ {subtotal:.2f}")

    desconto = float(input("Desconto: (%): "))
    descricao = input("Descrição: ")
    total = subtotal * (1 - desconto / 100)
    print(f"Desconto: {desconto:.0f}%")
    print(f"Total: R$ {total:.2f}")

