import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Conta(ABC):
    def __init__(self, agencia, numero_conta, cliente):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.cliente = cliente
        self.saldo = 0
        self.limite = 500
        self.extrato = ""
        self.numero_saques = 0

    @abstractclassmethod
    def sacar(self, valor):
        pass

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito:\tR$ {valor:.2f}\n"
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("==========================================")


class ContaCorrente(Conta):
    def __init__(self, agencia, numero_conta, cliente):
        super().__init__(agencia, numero_conta, cliente)
        self.limite_saques = 3

    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.limite_saques

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque:\t\tR$ {valor:.2f}\n"
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")


class Cliente:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class Banco:
    def __init__(self):
        self.agencia_padrao = "0001"
        self.clientes = []
        self.contas = []

    def criar_cliente(self):
        cpf = input("Digite o CPF (somente números): ")
        if self.buscar_cliente(cpf):
            print("\n@@@ Já existe cliente com esse CPF! @@@")
            return

        nome = input("Digite o nome completo: ")
        data_nascimento = input("Digite a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Digite o endereço (logradouro, número - bairro - cidade/sigla estado): ")

        cliente = Cliente(nome, data_nascimento, cpf, endereco)
        self.clientes.append(cliente)
        print("\n=== Cliente criado com sucesso! ===")

    def buscar_cliente(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                return cliente
        return None

    def criar_conta_corrente(self):
        cpf = input("Digite o CPF do cliente: ")
        cliente = self.buscar_cliente(cpf)
        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        numero_conta = len(self.contas) + 1
        conta_corrente = ContaCorrente(self.agencia_padrao, numero_conta, cliente)
        cliente.adicionar_conta(conta_corrente)
        self.contas.append(conta_corrente)
        print("\n=== Conta criada com sucesso! ===")

    def listar_contas(self):
        for conta in self.contas:
            print("=" * 100)
            print(f"Agência:\t{conta.agencia}")
            print(f"C/C:\t\t{conta.numero_conta}")
            print(f"Titular:\t{conta.cliente.nome}")

    def menu(self):
        menu_texto = textwrap.dedent("""
            ================ MENU ================
            [1]\tDepositar
            [2]\tSacar
            [3]\tExtrato
            [4]\tNova conta
            [5]\tListar contas
            [6]\tNovo usuário
            [7]\tSair
            => """)
        opcao = input(menu_texto)
        if opcao.isdigit() and 1 <= int(opcao) <= 7:
            return int(opcao)
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

    def realizar_operacao(self):
        while True:
            opcao = self.menu()

            if opcao == 1:
                cpf = input("Digite o CPF do cliente: ")
                cliente = self.buscar_cliente(cpf)
                if not cliente:
                    print("\n@@@ Cliente não encontrado! @@@")
                    continue

                valor = float(input("Digite o valor do depósito: "))
                conta = cliente.contas[0]
                conta.depositar(valor)

            elif opcao == 2:
                cpf = input("Digite o CPF do cliente: ")
                cliente = self.buscar_cliente(cpf)
                if not cliente:
                    print("\n@@@ Cliente não encontrado! @@@")
                    continue

                valor = float(input("Digite o valor do saque: "))
                conta = cliente.contas[0]
                conta.sacar(valor)

            elif opcao == 3:
                cpf = input("Digite o CPF do cliente: ")
                cliente = self.buscar_cliente(cpf)
                if not cliente:
                    print("\n@@@ Cliente não encontrado! @@@")
                    continue

                conta = cliente.contas[0]
                conta.exibir_extrato()

            elif opcao == 4:
                self.criar_conta_corrente()

            elif opcao == 5:
                self.listar_contas()

            elif opcao == 6:
                self.criar_cliente()

            elif opcao == 7:
                break

            else:
                print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


def main():
    banco = Banco()
    banco.realizar_operacao()


if __name__ == "__main__":
    main()
