"""Testes unitários para models Pydantic."""

import pytest
from datetime import date
from pydantic import ValidationError
from src.models.endereco import Endereco
from src.models.cliente import Cliente
from src.models.funcionario import Funcionario
from src.models.conta_corrente import ContaCorrente
from src.models.conta_poupanca import ContaPoupanca
from src.exceptions.banco_exceptions import CPFInvalidoError, IdadeInvalidaError
from src.utils.security import hash_senha


class TestModelEndereco:
    """Testes para o model Endereco."""
    
    def test_endereco_valido(self, endereco_padrao: Endereco) -> None:
        """Testa criação de endereço válido."""
        assert endereco_padrao.cep == "79002-000"
        assert endereco_padrao.estado == "MS"
    
    def test_endereco_cep_invalido(self) -> None:
        """Testa rejeição de CEP inválido."""
        with pytest.raises(ValidationError):
            Endereco(
                cep="790",  # CEP inválido
                numero="123",
                rua="Rua A",
                bairro="Centro",
                cidade="Campo Grande",
                estado="MS"
            )
    
    def test_endereco_estado_invalido(self) -> None:
        """Testa rejeição de sigla de estado inválida."""
        with pytest.raises(ValidationError):
            Endereco(
                cep="79002-000",
                numero="123",
                rua="Rua A",
                bairro="Centro",
                cidade="Campo Grande",
                estado="MSS"  # Deve ter 2 letras
            )


class TestModelCliente:
    """Testes para o model Cliente."""
    
    def test_cliente_valido(self, cliente_padrao: Cliente) -> None:
        """Testa criação de cliente válido."""
        assert cliente_padrao.nome == "João Silva"
        assert cliente_padrao.cpf == "123.456.789-09"
    
    def test_cliente_cpf_invalido(self) -> None:
        """Testa rejeição de CPF inválido."""
        with pytest.raises(CPFInvalidoError):
            Cliente(
                nome="João",
                cpf="111.111.111-11",  # CPF inválido
                data_nascimento=date(1990, 1, 1),
                cnh="123456789"
            )
    
    def test_cliente_idade_menor_18_anos(self) -> None:
        """Testa rejeição de cliente menor de 18 anos."""
        with pytest.raises(IdadeInvalidaError):
            Cliente(
                nome="João",
                cpf="123.456.789-09",
                data_nascimento=date(2020, 1, 1),  # Muito jovem
                cnh="123456789"
            )


class TestModelFuncionario:
    """Testes para o model Funcionario."""
    
    def test_funcionario_valido(self, funcionario_padrao: Funcionario) -> None:
        """Testa criação de funcionário válido."""
        assert funcionario_padrao.cargo == "Gerente"
        assert funcionario_padrao.salario == 5000.0
    
    def test_funcionario_salario_negativo(self) -> None:
        """Testa rejeição de salário negativo."""
        with pytest.raises(ValidationError):
            Funcionario(
                nome="Maria",
                cpf="987.654.321-00",
                data_nascimento=date(1985, 5, 15),
                cargo="Gerente",
                matricula="F001",
                salario=-100.0  # Salário negativo
            )


class TestModelContaCorrente:
    """Testes para o model ContaCorrente."""
    
    def test_conta_corrente_valida(self, conta_corrente_padrao: ContaCorrente) -> None:
        """Testa criação de conta corrente válida."""
        assert conta_corrente_padrao.numero == "12345-6"
        assert conta_corrente_padrao.saldo == 1000.0
        assert conta_corrente_padrao.limite == 500.0
    
    def test_conta_corrente_saldo_negativo(self, cliente_padrao: Cliente) -> None:
        """Testa rejeição de saldo negativo."""
        with pytest.raises(ValidationError):
            ContaCorrente(
                numero="12345-6",
                cliente=cliente_padrao,
                saldo=-100.0,  # Saldo negativo
                senha_hash=hash_senha("senha"),
                limite=500.0
            )


class TestModelContaPoupanca:
    """Testes para o model ContaPoupanca."""
    
    def test_conta_poupanca_valida(self, conta_poupanca_padrao: ContaPoupanca) -> None:
        """Testa criação de conta poupança válida."""
        assert conta_poupanca_padrao.numero == "98765-4"
        assert conta_poupanca_padrao.taxa_rendimento == 0.5
    
    def test_conta_poupanca_taxa_negativa(self, cliente_padrao: Cliente) -> None:
        """Testa rejeição de taxa de rendimento negativa."""
        with pytest.raises(ValidationError):
            ContaPoupanca(
                numero="98765-4",
                cliente=cliente_padrao,
                saldo=5000.0,
                senha_hash=hash_senha("senha"),
                taxa_rendimento=-0.5,  # Taxa negativa
                data_aniversario=15
            )
