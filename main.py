from dotenv import load_dotenv
import os
import mysql.connector
from decimal import Decimal, InvalidOperation

load_dotenv()


nome_banco = os.getenv("DB_NAME")
senha_banco = os.getenv("DB_PASSWORD")
user_banco = os.getenv("DB_USER")
host_banco = os.getenv("DB_HOST")

conexão = mysql.connector.connect(
    host=host_banco,
    user=user_banco,
    password=senha_banco,
    database=nome_banco
)

cursor = conexão.cursor()


def buscar_produto(codigo):
    cursor.execute(
        """
        SELECT id, codigo, nome, preco, quantidade
        FROM Produtos
        WHERE codigo = %s
        """,
        (codigo,)
    )

    return cursor.fetchone()



def mostrar_estoque():

    cursor.execute(
        """
        SELECT nome, codigo, preco, quantidade
        FROM Produtos
        ORDER BY nome
        """
    )

    produtos = cursor.fetchall()

    print("\n========== ESTOQUE ==========")

    if not produtos:
        print("Não há produtos cadastrados.")
        return

    for produto in produtos:

        nome = produto[0]
        codigo = produto[1]
        preco = produto[2]
        quantidade = produto[3]

        print(
            f"Nome: {nome} | "
            f"Código: {codigo} | "
            f"Preço: R$ {preco:.2f} | "
            f"Quantidade: {quantidade}"
        )



def entrada_produto():

    codigo = input(
        "Digite o código do produto: "
    ).strip()

    produto = buscar_produto(codigo)

    if not produto:
        print("Produto não encontrado.")
        return

    nome = produto[2]
    quantidade_atual = produto[4]

    print(f"\nProduto: {nome}")
    print(f"Quantidade atual: {quantidade_atual}")

    try:
        quantidade = int(
            input("Quantidade a ser adicionada: ")
        )
    except ValueError:
        print("Digite uma quantidade válida.")
        return

    if quantidade <= 0:
        print("A quantidade deve ser maior que 0.")
        return

    nova_quantidade = quantidade_atual + quantidade

    cursor.execute(
        """
        UPDATE Produtos
        SET quantidade = %s
        WHERE codigo = %s
        """,
        (nova_quantidade, codigo)
    )

    conexão.commit()

    print("\nEntrada de produto concluída.")
    print(
        f"Nova quantidade de {nome}: "
        f"{nova_quantidade}"
    )



def saida_produto():

    codigo = input(
        "Digite o código do produto: "
    ).strip()

    produto = buscar_produto(codigo)

    if not produto:
        print("Produto não encontrado.")
        return

    nome = produto[2]
    quantidade_atual = produto[4]

    print(f"\nProduto: {nome}")
    print(f"Quantidade atual: {quantidade_atual}")

    try:
        quantidade = int(
            input("Quantidade a ser retirada: ")
        )
    except ValueError:
        print("Digite uma quantidade válida.")
        return

    if quantidade <= 0:
        print("A quantidade deve ser maior que 0.")
        return

    if quantidade > quantidade_atual:
        print(
            "Quantidade solicitada para retirada é maior "
            "do que a quantidade em estoque!"
        )
        return

    nova_quantidade = quantidade_atual - quantidade

    cursor.execute(
        """
        UPDATE Produtos
        SET quantidade = %s
        WHERE codigo = %s
        """,
        (nova_quantidade, codigo)
    )

    conexão.commit()

    print("\nRetirada de produto concluída.")
    print(
        f"Nova quantidade em estoque de {nome}: "
        f"{nova_quantidade}"
    )



def corrigir_estoque():

    codigo = input(
        "Digite o código do produto: "
    ).strip()

    produto = buscar_produto(codigo)

    if not produto:
        print("\nProduto não encontrado.")
        return

    print(
        "\nO que precisa corrigir?\n"
        "1 - Código\n"
        "2 - Nome\n"
        "3 - Quantidade\n"
        "4 - Preço"
    )

    correcao = input(
        "Digite uma opção: "
    ).strip()

    
    if correcao == "1":

        codigo_novo = input(
            "Digite o novo código: "
        ).strip()

        if not codigo_novo:
            print("O código não pode ficar vazio.")
            return

        produto_existente = buscar_produto(codigo_novo)

        if produto_existente:
            print("Esse código já está cadastrado.")
            return

        cursor.execute(
            """
            UPDATE Produtos
            SET codigo = %s
            WHERE codigo = %s
            """,
            (codigo_novo, codigo)
        )

        conexão.commit()

        print("Código alterado com sucesso!")
        print(
            f"Código alterado: "
            f"{codigo} → {codigo_novo}"
        )

    
    elif correcao == "2":

        nome_novo = input(
            "Digite o novo nome do produto: "
        ).strip()

        if not nome_novo:
            print("O nome não pode ficar vazio.")
            return

        cursor.execute(
            """
            UPDATE Produtos
            SET nome = %s
            WHERE codigo = %s
            """,
            (nome_novo, codigo)
        )

        conexão.commit()

        print("Nome alterado com sucesso!")

    
    elif correcao == "3":

        try:
            quantidade_nova = int(
                input("Digite a nova quantidade: ")
            )
        except ValueError:
            print("Digite uma quantidade válida.")
            return

        if quantidade_nova < 0:
            print("A quantidade não pode ser negativa.")
            return

        cursor.execute(
            """
            UPDATE Produtos
            SET quantidade = %s
            WHERE codigo = %s
            """,
            (quantidade_nova, codigo)
        )

        conexão.commit()

        print("Quantidade alterada com sucesso!")


    elif correcao == "4":

        try:
            preco_novo = Decimal(
                input(
                    "Digite o novo preço: "
                ).replace(",", ".")
            )
        except InvalidOperation:
            print("Digite um preço válido.")
            return

        if preco_novo < 0:
            print("O preço não pode ser negativo.")
            return

        cursor.execute(
            """
            UPDATE Produtos
            SET preco = %s
            WHERE codigo = %s
            """,
            (preco_novo, codigo)
        )

        conexão.commit()

        print("Preço alterado com sucesso!")

    else:
        print("Opção inválida.")



def menu_estoque():

    while True:

        print("\n================================")
        print("             ESTOQUE")
        print("================================")
        print("1 - Entrada de Produto")
        print("2 - Saída do Produto")
        print("3 - Ver estoque")
        print("4 - Corrigir estoque")
        print("5 - Voltar")
        print("================================")

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        if opcao == "1":

            entrada_produto()

        elif opcao == "2":

            saida_produto()

        elif opcao == "3":

            mostrar_estoque()

        elif opcao == "4":

            corrigir_estoque()

        elif opcao == "5":

            break

        else:

            print("Opção inválida.")



def adicionar_produto(carrinho, codigo):

    produto = buscar_produto(codigo)

    if not produto:
        print("Produto não encontrado.")
        return

    id_produto = produto[0]
    nome = produto[2]
    preco = produto[3]
    quantidade_estoque = produto[4]

    quantidade_no_carrinho = carrinho.get(
        id_produto,
        0
    )

    if quantidade_estoque <= quantidade_no_carrinho:
        print("Produto indisponível.")
        return

    if id_produto in carrinho:

        carrinho[id_produto] += 1

    else:

        carrinho[id_produto] = 1

    print(f"\nProduto: {nome}")
    print(f"Preço: R$ {preco:.2f}")
    print("Produto adicionado à compra.")



def mostrar_carrinho(carrinho):

    print("\n========== COMPRA ==========")

    if not carrinho:
        print("Nenhum produto adicionado.")
        return Decimal("0.00")

    subtotal = Decimal("0.00")

    for id_produto, quantidade in carrinho.items():

        cursor.execute(
            """
            SELECT nome, preco
            FROM Produtos
            WHERE id = %s
            """,
            (id_produto,)
        )

        produto = cursor.fetchone()

        if produto:

            nome = produto[0]
            preco = produto[1]

            valor = preco * quantidade

            subtotal += valor

            print(
                f"{nome} | "
                f"Quantidade: {quantidade} | "
                f"Valor: R$ {valor:.2f}"
            )

    print("-----------------------------")
    print(
        f"Subtotal: R$ {subtotal:.2f}"
    )

    return subtotal



def aplicar_promocao(carrinho, subtotal):

    promocao = input(
        "\nDeseja aplicar uma promoção? (S/N): "
    ).strip().lower()

    if promocao != "s":
        return subtotal

    print("\nPromoções disponíveis:")
    print("1 - Leve 3, pague 2")
    print("2 - Nenhuma")

    opcao = input(
        "Escolha uma opção: "
    ).strip()

    if opcao != "1":
        return subtotal

    codigo = input(
        "Digite o código do produto da promoção: "
    ).strip()

    produto = buscar_produto(codigo)

    if not produto:
        print("Produto não encontrado.")
        return subtotal

    id_produto = produto[0]
    preco = produto[3]

    if id_produto not in carrinho:
        print(
            "Esse produto não está na compra."
        )
        return subtotal

    quantidade = carrinho[id_produto]

    if quantidade < 3:
        print(
            "A promoção exige pelo menos "
            "3 unidades do produto."
        )
        return subtotal

    grupos_promocionais = quantidade // 3

    unidades_gratis = grupos_promocionais

    desconto = preco * unidades_gratis

    total = subtotal - desconto

    print("\nPromoção aplicada!")
    print(
        f"Unidades gratuitas: "
        f"{unidades_gratis}"
    )
    print(
        f"Desconto: R$ {desconto:.2f}"
    )

    return total



def finalizar_compra(carrinho):

    if not carrinho:

        print(
            "\nNenhum produto foi adicionado."
        )

        return

    subtotal = mostrar_carrinho(
        carrinho
    )

    total = aplicar_promocao(
        carrinho,
        subtotal
    )

    print("\n================================")
    print(
        f"TOTAL: R$ {total:.2f}"
    )
    print("================================")

    confirmacao = input(
        "Deseja confirmar a compra? (S/N): "
    ).strip().lower()

    if confirmacao != "s":

        print("\nCompra cancelada.")
        return

    for id_produto, quantidade in carrinho.items():

        cursor.execute(
            """
            SELECT nome, quantidade
            FROM Produtos
            WHERE id = %s
            FOR UPDATE
            """,
            (id_produto,)
        )

        produto = cursor.fetchone()

        if not produto:

            conexão.rollback()

            print(
                "Um dos produtos não foi encontrado."
            )

            return

        nome = produto[0]
        estoque_atual = produto[1]

        if quantidade > estoque_atual:

            conexão.rollback()

            print(
                f"Não foi possível finalizar a compra."
                f"\nO produto {nome} não possui "
                f"estoque suficiente."
            )

            return


    for id_produto, quantidade in carrinho.items():

        cursor.execute(
            """
            UPDATE Produtos
            SET quantidade = quantidade - %s
            WHERE id = %s
            """,
            (quantidade, id_produto)
        )

    conexão.commit()

    print("\nCompra finalizada com sucesso!")
    print(
        f"Total da compra: R$ {total:.2f}"
    )
    print("Estoque atualizado.")


def autoatendimento():

    carrinho = {}

    print("\n ===============AUTOATENDIMENTO===================")

    while True:

        codigo = input(
            "\nDigite ou escaneie o código de barras "
            "(ou 'fim' para finalizar): "
        ).strip()

        if codigo.lower() == "fim":
            break

        adicionar_produto(
            carrinho,
            codigo
        )

    if not carrinho:

        print(
            "\nNenhum produto foi adicionado."
        )

        return

    finalizar_compra(
        carrinho
    )

try:

    while True:

        print("\n======== SISTEMA DE AUTOATENDIMENTO ===========")
        print("1 - Gerenciar estoque")
        print("2 - Iniciar compra")
        print("3 - Sair")

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        if opcao == "1":

            menu_estoque()

        elif opcao == "2":

            autoatendimento()

        elif opcao == "3":

            print(
                "\nEncerrando o sistema..."
            )

            break

        else:

            print("Opção inválida.")

finally:

    cursor.close()
    conexão.close()

    print("Sistema encerrado.")