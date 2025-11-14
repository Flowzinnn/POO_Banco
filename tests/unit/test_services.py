"""Testes unitários para services."""

import pytest
from src.services import conta_service, agencia_service
from src.models.conta_corrente import ContaCorrente
from src.models.conta_poupanca import ContaPoupanca
from src.models.agencia import Agencia
from src.exceptions.banco_exceptions import (
    SaldoInsuficienteError,
    ValorInvalidoError,
    LimiteExcedidoError,
    ContaDuplicadaError
)


class TestContaService:
    """Testes para o serviço de conta."""
    
    def test_realizar_deposito_valido(self, conta_corrente_padrao: ContaCorrente) -> None:
        """Testa depósito válido."""
        saldo_inicial = conta_corrente_padrao.saldo
        conta_service.realizar_deposito(conta_corrente_padrao, 500.0)
        
        assert conta_corrente_padrao.saldo == saldo_inicial + 500.0
        assert len(conta_corrente_padrao.transacoes) == 1
    
    def test_realizar_deposito_valor_invalido(self, conta_corrente_padrao: ContaCorrente) -> None:
        """Testa rejeição de depósito com valor inválido."""
        with pytest.raises(ValorInvalidoError):
            conta_service.realizar_deposito(conta_corrente_padrao, -100.0)
    
    def test_realizar_saque_conta_corrente_dentro_limite(
        self,
        conta_corrente_padrao: ContaCorrente
    ) -> None:
        """Testa saque dentro do limite da conta corrente."""
        # Saldo 1000 + limite 500 = 1500 disponível
        conta_service.realizar_saque(conta_corrente_padrao, 1200.0)
        
        assert conta_corrente_padrao.saldo == -200.0  # Usou parte do limite
        assert len(conta_corrente_padrao.transacoes) == 1
    
    def test_realizar_saque_conta_corrente_excede_limite(
        self,
        conta_corrente_padrao: ContaCorrente
    ) -> None:
        """Testa rejeição de saque que excede o limite."""
        with pytest.raises(LimiteExcedidoError):
            conta_service.realizar_saque(conta_corrente_padrao, 2000.0)  # Excede limite
    
    def test_realizar_saque_conta_poupanca_saldo_insuficiente(
        self,
        conta_poupanca_padrao: ContaPoupanca
    ) -> None:
        """Testa rejeição de saque com saldo insuficiente em poupança."""
        with pytest.raises(SaldoInsuficienteError):
            conta_service.realizar_saque(conta_poupanca_padrao, 10000.0)  # Excede saldo
    
    def test_transferir_entre_contas(
        self,
        conta_corrente_padrao: ContaCorrente,
        conta_poupanca_padrao: ContaPoupanca
    ) -> None:
        """Testa transferência entre contas."""
        saldo_origem = conta_corrente_padrao.saldo
        saldo_destino = conta_poupanca_padrao.saldo
        
        conta_service.transferir(conta_corrente_padrao, conta_poupanca_padrao, 300.0)
        
        assert conta_corrente_padrao.saldo == saldo_origem - 300.0
        assert conta_poupanca_padrao.saldo == saldo_destino + 300.0
    
    def test_calcular_imposto_conta_corrente(
        self,
        conta_corrente_padrao: ContaCorrente
    ) -> None:
        """Testa cálculo de imposto em conta corrente."""
        imposto = conta_service.calcular_imposto(conta_corrente_padrao)
        
        # 7% de 1000 = 70
        assert imposto == pytest.approx(70.0, rel=0.01)
    
    def test_calcular_rendimento_conta_poupanca(
        self,
        conta_poupanca_padrao: ContaPoupanca
    ) -> None:
        """Testa cálculo de rendimento em conta poupança."""
        rendimento = conta_service.calcular_rendimento(conta_poupanca_padrao)
        
        # 0.5% de 5000 = 25
        assert rendimento == pytest.approx(25.0, rel=0.01)


class TestAgenciaService:
    """Testes para o serviço de agência."""
    
    def test_adicionar_conta_na_agencia(
        self,
        conta_corrente_padrao: ContaCorrente,
        agencia_padrao: Agencia
    ) -> None:
        """Testa adição de conta à agência."""
        agencia_service.adicionar_conta_na_agencia(conta_corrente_padrao, agencia_padrao)
        
        assert conta_corrente_padrao in agencia_padrao.contas
    
    def test_adicionar_conta_duplicada_na_agencia(
        self,
        conta_corrente_padrao: ContaCorrente,
        agencia_padrao: Agencia
    ) -> None:
        """Testa rejeição de conta duplicada."""
        agencia_service.adicionar_conta_na_agencia(conta_corrente_padrao, agencia_padrao)
        
        with pytest.raises(ContaDuplicadaError):
            agencia_service.adicionar_conta_na_agencia(conta_corrente_padrao, agencia_padrao)
