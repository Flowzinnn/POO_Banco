from datetime import datetime, date
from typing import List
from abc import ABC, abstractmethod

# INTERFACE -> CLASSE ABSTRATA QUE POSSUI APENAS MÉTODOS ABSTRATOS;
# INTERFACE É UM CONTRATO QUE DIZ QUE A CLASSE FILHA TEM QUE IMPLEMENTAR OS MÉTODOS DA INTERFACE;
# A INTERFACE NÃO TEM ATRIBUTOS, APENAS MÉTODOS;
# A INTERFACE NÃO PODE SER INSTANCIADA, APENAS HERDADA;
# A INTERFACE NÃO TEM CONSTRUTOR, APENAS MÉTODOS ABSTRATOS;
# A INTERFACE NÃO TEM IMPLEMENTAÇÃO, APENAS ASSINATURAS DE MÉTODOS;
# A INTERFACE NÃO TEM NENHUM CÓDIGO, APENAS DEFINIÇÕES DE MÉTODOS;
# A INTERFACE É UMA CLASSE ABSTRATA QUE NÃO TEM NENHUM CÓDIGO, APENAS DEFINIÇÕES DE MÉTODOS;

class Autenticavel(ABC):
    
    @abstractmethod
    def autenticar(self, senha: str) -> bool:
        pass

class Tributavel(ABC):
    
    @abstractmethod
    def get_valor_imposto(self) -> float:
        pass
    
class Rentavel(ABC):
    
    @abstractmethod
    def get_rendimento(self) -> float:
        pass

class Notificacao(ABC):
    
    @staticmethod
    def deposito(valor):
        print(f"✅ Depósito de R$ {valor:.2f} realizado com sucesso.")

    @staticmethod
    def saque(valor):
        print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso.")

    @staticmethod
    def erro_valor_invalido():
        print("⚠️ Valor inválido.")

    @staticmethod
    def erro_saldo_insuficiente():
        print("❌ Saldo insuficiente.")

    @staticmethod
    def erro_limite_excedido():
        print("❌ Valor excede o limite da conta.")

    @staticmethod
    def taxa_manutencao(valor):
        print(f"⚙️ Taxa de manutenção de R$ {valor:.2f} aplicada.")

    @staticmethod
    def nenhuma_transacao():
        print("⚠️  Nenhuma transação realizada.")

    @staticmethod
    def cabecalho_extrato():
        print("\n" + "="*40)
        print(f"{'🧾 EXTRATO BANCÁRIO':^40}")
        print("="*40)

    @staticmethod
    def cabecalho_conta(numero, nome_cliente):
        print(f"📄 Conta: {numero}")
        print(f"🙍 Cliente: {nome_cliente}")
        print("-"*40)

    @staticmethod
    def rodape_extrato(saldo):
        print("="*40)
        print(f"{'Saldo atual:':<27} R$ {saldo:,.2f}")
        print("="*40 + "\n")

    @staticmethod
    def listar_contas(cliente_nome):
        print(f"\n📘 Contas de {cliente_nome}:")

    @staticmethod
    def nenhuma_conta():
        print("⚠️ Nenhuma conta cadastrada.")

    @staticmethod
    def listar_agencias_do_banco(nome_banco):
        print(f"\n📝 Agências do {nome_banco}:")

    @staticmethod
    def nenhuma_agencia():
        print("⚠️ Não há agências cadastradas.")
        
    @staticmethod
    def agencia_detalhes(agencia):
        print(f"🏦 {agencia.nome} | Nº: {agencia.numero} | 📍 {agencia.endereco} | 📞 {agencia.fone}")
        
    @staticmethod
    def conta_enumerada(indice, conta):
        print(f"{indice}️⃣ {conta}")
        
    @staticmethod
    def mostrar_transacao(transacao: 'Transacao'):
        print(transacao)
        
    @staticmethod
    def sem_taxa_poupanca():
        print("ℹ️ Conta Poupança não possui taxa de manutenção.")

class Exceptions:
    """
    Centraliza as exceções de domínio do sistema bancário
    e oferece métodos auxiliares de validação.
    """

    # ===================== CLASSES DE EXCEÇÃO ===================== #

    class BancoError(Exception):
        """Exceção base para o domínio bancário."""
        pass

    class ValorInvalidoError(BancoError):
        """Lançada quando o valor informado é menor ou igual a zero."""
        pass

    class SaldoInsuficienteError(BancoError):
        """Lançada quando o saldo não é suficiente para a operação."""
        pass

    class LimiteExcedidoError(BancoError):
        """Lançada quando o valor solicitado ultrapassa saldo + limite."""
        pass

    class AutenticacaoError(BancoError):
        """Lançada quando a autenticação de uma conta falha."""
        pass

    # ===================== MÉTODOS ESTÁTICOS DE VALIDAÇÃO ===================== #

    @staticmethod
    def validar_valor_positivo(valor: float) -> None:
        """
        Garante que o valor informado seja maior que zero.
        Levanta ValorInvalidoError se não for.
        """
        if valor <= 0:
            raise Exceptions.ValorInvalidoError(
                "Valor informado deve ser maior que zero."
            )

    @staticmethod
    def validar_saque_poupanca(saldo: float, valor: float) -> None:
        """
        Regras de saque para Conta Poupança:
        - valor deve ser positivo
        - valor não pode ser maior que o saldo
        """
        Exceptions.validar_valor_positivo(valor)

        if valor > saldo:
            raise Exceptions.SaldoInsuficienteError(
                "Saldo insuficiente para realizar o saque."
            )

    @staticmethod
    def validar_saque_corrente(saldo: float, limite: float, valor: float) -> None:
        """
        Regras de saque para Conta Corrente:
        - valor deve ser positivo
        - valor não pode ultrapassar (saldo + limite)
        """
        Exceptions.validar_valor_positivo(valor)

        if valor > (saldo + limite):
            raise Exceptions.LimiteExcedidoError(
                "Valor do saque excede o limite disponível da conta."
            )

    @staticmethod
    def validar_autenticacao(autenticado: bool) -> None:
        """
        Garante que a autenticação foi bem-sucedida.
        Lança AutenticacaoError se a senha for inválida.
        """
        if not autenticado:
            raise Exceptions.AutenticacaoError("Falha na autenticação: senha inválida.")

  
class Endereco:
    def __init__(self, cep: str, numero: str, rua: str, bairro: str, cidade: str, estado: str):
        self._cep = cep
        self._numero = numero
        self._rua = rua
        self._bairro = bairro
        self._cidade = cidade
        self._estado = estado

    def __str__(self):
        return f"{self._rua}, {self._numero}, {self._bairro}, {self._cidade} - {self._estado}, CEP: {self._cep}"
    
    @property
    def cep(self):
        return self._cep

    @cep.setter
    def cep(self, value):
        self._cep = value

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, value):
        self._numero = value

    @property
    def rua(self):
        return self._rua

    @rua.setter
    def rua(self, value):
        self._rua = value

    @property
    def bairro(self):
        return self._bairro

    @bairro.setter
    def bairro(self, value):
        self._bairro = value

    @property
    def cidade(self):
        return self._cidade

    @cidade.setter
    def cidade(self, value):
        self._cidade = value

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self._estado = value       

class Banco:
    def __init__(self, nome: str, cnpj: str, endereco: Endereco, fone: str) -> None:
        self._nome = nome
        self._cnpj = cnpj
        self._endereco = endereco
        self._fone = fone
        self._agencias: List['Agencia'] = []
        
    def __str__(self):
        return f"🏦 Banco: {self._nome}, CNPJ: {self._cnpj}, Endereço: {self._endereco}, Telefone: {self._fone}"

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def cnpj(self):
        return self._cnpj

    @cnpj.setter
    def cnpj(self, value):
        self._cnpj = value

    @property
    def endereco(self):
        return self._endereco

    @endereco.setter
    def endereco(self, value):
        self._endereco = value

    @property
    def fone(self):
        return self._fone

    @fone.setter
    def fone(self, value):
        self._fone = value

    def adicionar_agencia(self, *agencias: 'Agencia'):
        self._agencias.extend(agencias)
        
    def listar_agencias(self):
        Notificacao.listar_agencias_do_banco(self.nome)
        if not self._agencias:
            Notificacao.nenhuma_agencia()
        else:
            for agencia in self._agencias:
                Notificacao.agencia_detalhes(agencia)
                   
class Agencia:
    def __init__(self, nome: str, numero: str, endereco: Endereco, fone: str):
        self._nome = nome
        self._numero = numero
        self._endereco = endereco
        self._fone = fone
        self.contas: List['Conta'] = []
    
    def __str__(self):
        return f"🏢 Agência: {self._nome}, Número: {self._numero}, Endereço: {self._endereco}, Telefone: {self._fone}"
    
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, value):
        self._numero = value

    @property
    def endereco(self):
        return self._endereco

    @endereco.setter
    def endereco(self, value):
        self._endereco = value

    @property
    def fone(self):
        return self._fone

    @fone.setter
    def fone(self, value):
        self._fone = value

class Transacao:
    def __init__(self, tipo: str, valor: float, conta: 'Conta'):
        self._tipo = tipo
        self._valor = valor
        self._conta = conta
        self._data = datetime.now()

    def __str__(self):
        data = self._data.strftime('%d/%m/%Y %H:%M')
        valor = f"R$ {self._valor:,.2f}"
        return f"{data} | {self._tipo:<10} | {valor.rjust(12)}"

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, value):
        self._tipo = value

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, value):
        self._valor = value

    @property
    def conta(self):
        return self._conta

    @conta.setter
    def conta(self, value):
        self._conta = value

    @property
    def data(self):
        return self._data

#Classe Abstrata ou Classe Pai;
class Pessoa(ABC):
    def __init__(self, nome: str, cpf: str, data_nascimento: date) -> None:
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, value):
        self._cpf = value

    @property
    def data_nascimento(self):
        return self._data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, value):
        self._data_nascimento = value

class Cliente(Pessoa):
    def __init__(self, nome: str, cpf: str, data_nascimento: date, cnh: str):
        super().__init__(nome, cpf, data_nascimento)
        self._cnh = cnh
        self._contas: List['Conta'] = []
        
    def __str__(self):
        return f"🙍 Cliente: {self.nome} | CPF: {self.cpf}"


    @property
    def cnh(self):
        return self._cnh

    @cnh.setter
    def cnh(self, value):
        self._cnh = value

    @property
    def contas(self):
        return self._contas

    def adicionar_conta(self, conta: 'Conta'):
        self._contas.append(conta)
        
    def listar_contas(self):
        Notificacao.listar_contas(self.nome)
        if not self._contas:
            Notificacao.nenhuma_conta()
        else:
            for i, conta in enumerate(self._contas, 1):
                Notificacao.conta_enumerada(i, conta)

class Funcionario(Pessoa):
    def __init__(self, nome: str, cpf: str, data_nascimento: date, cargo: str, matricula: str, salario: float):
        super().__init__(nome, cpf, data_nascimento)
        self._cargo = cargo
        self._matricula = matricula
        self._salario = salario

    @property
    def cargo(self):
        return self._cargo

    @cargo.setter
    def cargo(self, value):
        self._cargo = value

    @property
    def matricula(self):
        return self._matricula

    @matricula.setter
    def matricula(self, value):
        self._matricula = value

    @property
    def salario(self):
        return self._salario

    @salario.setter
    def salario(self, value):
        self._salario = value
        
#Classe Abstrata/Abstract class : CLASSES ABSTRATAS NUNCA IRÃO GERAR UM OBJETO;
class Conta(Autenticavel):
    def __init__(self, numero: str, cliente: Cliente, saldo: float, senha: str):
        self._numero = numero
        self._cliente = cliente
        self._saldo =saldo 
        self._senha = senha
        self._transacoes: List['Transacao'] = []
        
        cliente.adicionar_conta(self)
    
    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, value):
        self._numero = value

    @property
    def cliente(self):
        return self._cliente

    @cliente.setter
    def cliente(self, value):
        self._cliente = value

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, value):
        self._saldo = value

    @property
    def senha(self):
        return self._senha

    @senha.setter
    def senha(self, value):
        self._senha = value
        
    @abstractmethod
    def sacar(self, valor: float):
        pass

    @abstractmethod
    def aplicar_taxas(self):
        pass

    def autenticar(self, senha):
        return self.senha == senha
        
    def depositar(self, valor: float):
        if valor <= 0:
            Notificacao.erro_valor_invalido()
            return

        self._saldo += valor
        transacao = Transacao("Depósito", valor, self)
        self._transacoes.append(transacao)
        Notificacao.deposito(valor)
    
    #========================================================= EXTRATO ===============================================================#
    
    def extrato(self):
        Notificacao.cabecalho_extrato()
        Notificacao.cabecalho_conta(self.numero, self.cliente.nome)

        if not self._transacoes:
            Notificacao.nenhuma_transacao()
            Notificacao.rodape_extrato(self.saldo)
            return

        for t in self._transacoes:
            Notificacao.mostrar_transacao(t)

        Notificacao.rodape_extrato(self.saldo)
        
class Conta_Corrente(Conta, Tributavel):
    def __init__(self, numero: str, cliente: Cliente, saldo: float, senha: str, limite: float):
        super().__init__(numero, cliente, saldo, senha)
        self._limite = limite
        self._taxa_manutencao = 10.0
        
    def __str__(self):
        return f"💳 Conta Corrente Nº {self.numero} | Saldo: R$ {self.saldo:,.2f} | Limite: R$ {self.limite:,.2f}"


    @property
    def limite(self):
        return self._limite

    @limite.setter
    def limite(self, value):
        self._limite = value
     
    def sacar(self, valor: float):
        if valor <= 0:
            Notificacao.erro_valor_invalido()
            return

        if valor > self._saldo + self._limite:
            Notificacao.erro_limite_excedido()
            return

        self._saldo -= valor
        transacao = Transacao("Saque", valor, self)
        self._transacoes.append(transacao)
        Notificacao.saque(valor)

    def aplicar_taxas(self):
        self._saldo -= self._taxa_manutencao
        transacao = Transacao("Taxa manutenção", self._taxa_manutencao, self)
        self._transacoes.append(transacao)
        Notificacao.taxa_manutencao(self._taxa_manutencao)
    
    def get_valor_imposto(self) -> float:
        return self.saldo * 0.07    
    
class Conta_Poupanca(Conta, Rentavel):
    def __init__(self, numero: str, cliente: Cliente, saldo: float, senha: str, taxa_rendimento: float):
        super().__init__(numero, cliente, saldo, senha)
        self._taxa_rendimento = taxa_rendimento
        self._data_aniversario = datetime.now().day
        
    def __str__(self):
        return f"🏦 Conta Poupança Nº {self.numero} | Saldo: R$ {self.saldo:,.2f} | Rendimento: {self.taxa_rendimento:.2f}%"

    def sacar(self, valor: float):
        if valor <= 0:
            Notificacao.erro_valor_invalido()
            return

        if valor > self._saldo:
            Notificacao.erro_saldo_insuficiente()
            return

        self._saldo -= valor
        transacao = Transacao("Saque", valor, self)
        self._transacoes.append(transacao)
        Notificacao.saque(valor)

    def aplicar_taxas(self):
        # Poupança geralmente não tem taxa, mas só pra cumprir o método
        Notificacao.sem_taxa_poupanca()
        
    def get_rendimento(self) -> float:
        rendimento = self.saldo * (self.taxa_rendimento / 100)
        return rendimento

    @property
    def taxa_rendimento(self):
        return self._taxa_rendimento

    @taxa_rendimento.setter
    def taxa_rendimento(self, value):
        self._taxa_rendimento = value

    @property
    def data_aniversario(self):
        return self._data_aniversario

    @data_aniversario.setter
    def data_aniversario(self, value):
        self._data_aniversario = value   

def main():
    
    # Endereço Banco
    enderecoBancoWolf = Endereco("122312", "123", "rua a", "bairro b", "tree lake city", "MS")
    enderecoAgenciaSul = Endereco("123121", "1323", "rua b", "bairro a", "tree lake city", "MS")
    
    # Criando as contas
    clienteNicolas = Cliente("Nicolas", "123.456.789-00", date(2003, 5, 10), "000000000")
    contaCorrenteNicolas001 = Conta_Corrente("001", clienteNicolas, 1000.0, "1234", 1000)
    contaPoupancaNicolas001 = Conta_Poupanca("001", clienteNicolas, 15000, "2508", 0.5)

    # Realizando operações
    contaCorrenteNicolas001.depositar(500)
    contaCorrenteNicolas001.sacar(150)

    # Imprimindo extrato
    contaCorrenteNicolas001.extrato()

    # Mostrando as contas do cliente
    clienteNicolas.listar_contas()


    agenciaSul = Agencia("Agência Sul", "001", enderecoAgenciaSul, "(11) 12345-6789")

    bancoWolf = Banco("Banco Wolf", "12.345.678/0001-90", enderecoBancoWolf, "(11) 98765-4321")

    bancoWolf.adicionar_agencia(agenciaSul)

    print(bancoWolf)

    bancoWolf.listar_agencias()

if __name__ == '__main__':
    main()