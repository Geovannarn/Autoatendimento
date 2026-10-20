from dotenv import load_dotenv
import os 
import mysql.connector

load_dotenv() 

nome_banco = os.getenv("DB_NAME")
senha_banco = os.getenv("DB_PASSWORD")
user_banco = os.getenv("DB_USER")
host_banco = os.getenv("DB_HOST")

conexão=mysql.connector.connect(
    host=host_banco,
    user=user_banco,
    password=senha_banco,
    database=nome_banco
)

cursor= conexão.cursor()
cursor.execute("SELECT* FROM Produtos")
produtos =cursor.fetchall()
print("\n Produtos cadastrados:")
for produtos in produtos:
        print(produtos)

estoque = {}

while True:
    print("\n1 - Entrada de Produto ")
    print("2 - Saída do Produto")
    print("3 - Ver estoque ")
    print("4 - Corrigir estoque ")
    print("5 - Sair ")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
         codigo = int(input("Digite o código do produto: "))
         cursor.execute(

            "SELECT nome, quantidade FROW Produtos WHERE codigo =%s", (codigo,)
              
         )
        
         produto = cursor.fetchone()
        
         if produto:
                    nome = produto[0]
                    quantidade = produto[1]
                    print(f"\nProduto: {nome}")
                    print(f"Quantidade atual: {quantidade_atual}")

         quantidade = int(input("Quantidade a ser adicionada: "))
         
         if quantidade >0:
                nova_quantidade = quantidade_atual + quantidade  
                cursor.execute(

                    "UPDATE Produtos SET quantidade = %s WHERE codigo = %s", (nova_quantidade, codigo) 

                )
                conexão.commit()
                print(f"\nEntrada de produto concluída. Nova quantidade de {nome}: {nova_quantidade}")
                print("Entrada Concluída")

         else:
            print("Quantia deve ser maior que 0.")

        
         else: 
            print("Produto não encontrado.")


    if opcao =="2":
          codigo = int(input("Digite o código do produto: "))
          cursor.execute(

            "SELECT nome, quantidade FROM Produtos WHERE codigo = %s", (codigo,)
                
          )
          produto = cursor.fetchone()
        
          if produto:
           nome = produto[0]
           quantidade = produto[1]
           print(f"\nProduto: {nome}")
           print(f"Quantidade atual: {quantidade_atual}")

          if quantidade <=0:
                print("Não há estoque disponível para retirada!")

          elif quantidade > quantidade_atual:
                print("Quantidade solicitada para retirada é maior do que a quantidade em estoque!")

          else:
            quantidade = quantidade_atual - quantidade
            cursor.execute(

                "UPDATE Produtos SET quantidade = %s WHERE codigo = %s", (nova_quantidade, codigo ) 
                  
            )
            conexão.commit()
            print("\nRetirada de produto concluída.")
            print(f"Nova quantidade em estoque de {nome}: {nova_quantidade}")

    else: 
            print("\n Produto não encontrado.")

    if opcao == "3":
          cursor.execute(

          "SELECT nome, codigo, preco, quantidade FROM Produtos"
          
          )
          produto = cursor.fetchall()

          print("\n===ESTOQUE==== ")
        
          if produtos:
                for produto in produtos:
                      nome = produto [0]
                      quantidade = produto [1]
                      codigo = produto [2]
                      preco = produto [3]
                      print(

                              f"nome: {nome}"
                              f"quantidade: {quantidade}"
                              f"codigo: {codigo}"
                              f"preco: {preco}"         
                              
                              )
          else:
            print("Não há produto cadastrados")


    if opcao == "4":
          codigo = int(input(("Digite o código do produto:")))
          cursor.execute(

                "SELECT nome, codigo, quantidade, preco FROM Produtos WHERE codigo = %s", (codigo,)

          )
          produto = cursor.fetchone()
          if produto:
                nome = produto [0]
                codigo = produto [1]
                quantidade = produto [2]
                preco = produto [3]
                print(

                "\nO que precisa corrigir?"
                "1- Código"
                "2- Nome"
                "3- Quantidade"
                "4- Preço"
                
                )
                coreção= int(input("Digite uma opção: "))
                if opcao == "1":
                      código_anterior =(int(input("Digite o código anterior: ")))
                      código_atual = (int(input("Digite o código novo")))
                      cursor.execute(

                            "UPDATE Produtos SET codigo =%s WHERE codigo = %s "(codigo_atual, código_anterior)
                            
                      )
                      conexão.commit()
                      print("Novo Código inserido com sucesso! ")
                      print(f"Código aduterado no estoque {código_anterior}: {código_atual}")
                
                elif opcao == "2":
                     nome_anterior = input("Digite o nome atual do produto: ")
                     nome_atual = input("Digite o novo nome do produto: ")
                     cursor.execute(

                        "UPDATE Produtos SET nome = %s WHERE nome =%s " (nome_atual, nome_anterior)
                           
                     )
                     conexão.commit()
                     print("Novo nome inserido com sucesso!")
                     print(f"Nome aduterado no estoque {nome_anterior}: {nome_atual}")

                elif opcao == "3":
                     quatidade_anterior = float(input("Digite o valor da quantidade errada inserida: "))
                     quantidade_nova = float(input("Digite o valor da nova quantidade a ser inserida:  "))
                     cursor.execute(

                        "UPDATE Produtos SET quantidade = %s WHERE quantidade = %s" (quantidade_nova, quantidade_anterior)    
                          
                     )
                     conexão.commit()
                     print("Nova quantidade alterada com sucesso! ")
                     print(f"Quantidade aduterada no estoque: {quantidade_anterior}: {quantidade_nova}")

                elif opcao == "4":
                     preço_anterior = float(input("Digite o valor errado inserido: "))
                     preço_novo = float(input("Digite o novo valor: "))
                     cursor.execute( 

                      "UPDATE Produtos SET preco = %s WHERE preco = %s" (preço_novo, preço_anterior)
                          
                     )
                     conexão.commit()
                     print("Novo preço adicionado com sucesso!")
                     print("Preço aduterado no estoque: { preço_anterior}: {preço_novo}")

                else:
                     print("Não foi possível realizar nenhuma alteração!") 

    elif opcao == "5":
        print("Saindo do programa...")
        break

conexão.close()
cursor.close()

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

