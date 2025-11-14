"""
Fixtures compartilhadas para testes.

Fixtures simples, legíveis e combináveis entre si.
"""

import pytest
from datetime import date
from src.models.endereco import Endereco
from src.models.cliente import Cliente
from src.models.funcionario import Funcionario
from src.models.agencia import Agencia
from src.models.banco import Banco
from src.models.conta_corrente import ContaCorrente
from src.models.conta_poupanca import ContaPoupanca
from src.utils.security import hash_senha


@pytest.fixture
def endereco_padrao() -> Endereco:
    """Fixture de endereço válido padrão."""
    return Endereco(
        cep="79002-000",
        numero="123",
        rua="Rua das Flores",
        bairro="Centro",
        cidade="Campo Grande",
        estado="MS"
    )


@pytest.fixture
def cliente_padrao(endereco_padrao: Endereco) -> Cliente:
    """Fixture de cliente válido padrão."""
    return Cliente(
        nome="João Silva",
        cpf="123.456.789-09",  # CPF válido para testes
        data_nascimento=date(1990, 1, 1),
        cnh="123456789"
    )


@pytest.fixture
def funcionario_padrao() -> Funcionario:
    """Fixture de funcionário válido padrão."""
    return Funcionario(
        nome="Maria Santos",
        cpf="987.654.321-00",  # CPF válido para testes
        data_nascimento=date(1985, 5, 15),
        cargo="Gerente",
        matricula="F001",
        salario=5000.0
    )


@pytest.fixture
def agencia_padrao(endereco_padrao: Endereco) -> Agencia:
    """Fixture de agência válida padrão."""
    return Agencia(
        nome="Agência Central",
        numero="0001",
        endereco=endereco_padrao,
        fone="(67) 3321-4567"
    )


@pytest.fixture
def banco_padrao(endereco_padrao: Endereco, agencia_padrao: Agencia) -> Banco:
    """Fixture de banco válido padrão com uma agência."""
    banco = Banco(
        nome="Banco Teste",
        cnpj="11.222.333/0001-81",  # CNPJ válido para testes
        endereco=endereco_padrao,
        fone="(67) 3321-0000"
    )
    banco.adicionar_agencia(agencia_padrao)
    return banco


@pytest.fixture
def conta_corrente_padrao(cliente_padrao: Cliente) -> ContaCorrente:
    """Fixture de conta corrente válida padrão."""
    senha_hash = hash_senha("senha123")
    return ContaCorrente(
        numero="12345-6",
        cliente=cliente_padrao,
        saldo=1000.0,
        senha_hash=senha_hash,
        limite=500.0
    )


@pytest.fixture
def conta_poupanca_padrao(cliente_padrao: Cliente) -> ContaPoupanca:
    """Fixture de conta poupança válida padrão."""
    senha_hash = hash_senha("senha456")
    return ContaPoupanca(
        numero="98765-4",
        cliente=cliente_padrao,
        saldo=5000.0,
        senha_hash=senha_hash,
        taxa_rendimento=0.5,
        data_aniversario=15
    )
