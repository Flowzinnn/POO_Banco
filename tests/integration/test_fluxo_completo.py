"""Testes de integração - fluxo completo."""

import pytest
from datetime import date
from src.models.endereco import Endereco
from src.models.cliente import Cliente
from src.models.conta_corrente import ContaCorrente
from src.models.conta_poupanca import ContaPoupanca
from src.models.agencia import Agencia
from src.models.banco import Banco
from src.services import conta_service, agencia_service, banco_service
from src.utils.security import hash_senha


class TestFluxoCompleto:
    """Testes de cenários completos end-to-end."""
    
    def test_fluxo_completo_abertura_conta_e_operacoes(self) -> None:
        """
        Testa fluxo completo:
        1. Criar banco e agência
        2. Criar cliente e conta
        3. Adicionar conta à agência
        4. Realizar operações (depósito, saque)
        5. Verificar saldos e transações
        """
        # 1. Criar estrutura bancária
        endereco = Endereco(
            cep="79002-000",
            numero="100",
            rua="Rua Principal",
            bairro="Centro",
            cidade="Campo Grande",
            estado="MS"
        )
        
        agencia = Agencia(
            nome="Agência Central",
            numero="0001",
            endereco=endereco,
            fone="(67) 3321-0000"
        )
        
        banco = Banco(
            nome="Banco Integração",
            cnpj="11.222.333/0001-81",
            endereco=endereco,
            fone="(67) 3321-1111"
        )
        banco.adicionar_agencia(agencia)
        
        # 2. Criar cliente e conta
        cliente = Cliente(
            nome="Carlos Teste",
            cpf="123.456.789-09",
            data_nascimento=date(1988, 3, 10),
            cnh="987654321"
        )
        
        conta = ContaCorrente(
            numero="10001-0",
            cliente=cliente,
            saldo=0.0,
            senha_hash=hash_senha("senha123"),
            limite=1000.0
        )
        
        # 3. Adicionar conta à agência
        agencia_service.adicionar_conta_na_agencia(conta, agencia)
        
        # 4. Realizar operações
        conta_service.realizar_deposito(conta, 500.0)
        conta_service.realizar_deposito(conta, 300.0)
        conta_service.realizar_saque(conta, 200.0)
        
        # 5. Verificações
        assert conta.saldo == 600.0
        assert len(conta.transacoes) == 3
        assert conta in agencia.contas
        assert agencia in banco.agencias
        
        # Verifica saldo total do banco
        saldo_total = banco_service.calcular_saldo_total_banco(banco)
        assert saldo_total == 600.0
        
        # Verifica número de clientes
        num_clientes = banco_service.calcular_numero_clientes(banco)
        assert num_clientes == 1
    
    def test_fluxo_transferencia_entre_contas(
        self,
        conta_corrente_padrao: ContaCorrente,
        conta_poupanca_padrao: ContaPoupanca,
        agencia_padrao: Agencia
    ) -> None:
        """
        Testa fluxo de transferência entre contas na mesma agência.
        """
        # Adiciona ambas as contas à agência
        agencia_service.adicionar_conta_na_agencia(conta_corrente_padrao, agencia_padrao)
        agencia_service.adicionar_conta_na_agencia(conta_poupanca_padrao, agencia_padrao)
        
        # Saldos iniciais
        saldo_cc_inicial = conta_corrente_padrao.saldo
        saldo_cp_inicial = conta_poupanca_padrao.saldo
        
        # Realiza transferência
        valor_transferencia = 400.0
        conta_service.transferir(conta_corrente_padrao, conta_poupanca_padrao, valor_transferencia)
        
        # Verificações
        assert conta_corrente_padrao.saldo == saldo_cc_inicial - valor_transferencia
        assert conta_poupanca_padrao.saldo == saldo_cp_inicial + valor_transferencia
        
        # Verifica que ambas as contas têm registro da transferência
        assert len(conta_corrente_padrao.transacoes) >= 1
        assert len(conta_poupanca_padrao.transacoes) >= 1
