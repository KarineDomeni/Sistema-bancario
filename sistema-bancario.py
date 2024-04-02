saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
  operacao = """
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Sair
    """
  print(operacao)
  opcao = input("Escolha uma opção: ")

  if opcao == "1":
    valor_deposito = float(input("Digite o valor a depositar: "))
    if valor_deposito > 0:
      saldo += valor_deposito
      extrato += f"Depósito de R$ {valor_deposito:.2f}\n"
      print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso!")
    else:
      print("O valor do depósito deve ser positivo.")
  elif opcao == "2":
    if numero_saques < LIMITE_SAQUES:
      valor_saque = float(input("Digite o valor a sacar: "))
      if saldo >= valor_saque and valor_saque <= limite:
        saldo -= valor_saque
        numero_saques += 1
        extrato += f"Saque de R$ {valor_saque:.2f}\n"
        print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso!")
      elif saldo < valor_saque:
        print("Saldo insuficiente.")
      elif valor_saque > limite:
        print(f"Limite de saque por operação é de R$ {limite:.2f}")
    else:
      print("Limite de saques diários atingido.")
  elif opcao == "3":
    print(f"Saldo disponível: R$ {saldo:.2f}")
    print("Extrato:")
    print(extrato)
    print(f"Número de saques realizados hoje: {numero_saques}")
  elif opcao == "4":
    print("Obrigado por usar o nosso sistema bancário. Volte sempre!")
    break
  else:
    print("Opção inválida, tente novamente.")