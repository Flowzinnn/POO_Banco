"""
Serviço de operações em contas bancárias.

Centraliza a lógica de negócio para operações como depósito,
saque, transferência e aplicação de taxas.
"""

from typing import TYPE_CHECKING
from src.exceptions.banco_exceptions import ValorInvalidoError
from src.models.transacao import Transacao
from src.views.console_view import (
    exibir_deposito,
    exibir_saque,
    exibir_taxa_manutencao,
    exibir_sem_taxa_poupanca
)
from src.utils.logger import get_logger

if TYPE_CHECKING:
    from src.models.conta import Conta

logger = get_logger("services.conta")


def realizar_deposito(conta: 'Conta', valor: float) -> None:
    """
    Realiza um depósito em uma conta.
    
    Args:
        conta: Conta destino do depósito
        valor: Valor a ser depositado
        
    Raises:
        ValorInvalidoError: Se o valor for inválido (negativo ou zero)
    """
    if valor <= 0:
        logger.warning(f"Tentativa de depósito com valor inválido: R$ {valor:.2f}")
        raise ValorInvalidoError(valor)
    
    # Realiza o depósito
    conta.saldo += valor
    
    # Registra a transação
    transacao = Transacao(tipo="Depósito", valor=valor, conta=conta)
    conta.transacoes.append(transacao)
    
    logger.info(f"Depósito de R$ {valor:.2f} realizado na conta {conta.numero}")
    exibir_deposito(valor)


def realizar_saque(conta: 'Conta', valor: float) -> None:
    """
    Realiza um saque de uma conta.
    
    Delega para o método sacar() da conta, que implementa
    as regras específicas de cada tipo de conta.
    
    Args:
        conta: Conta origem do saque
        valor: Valor a ser sacado
        
    Raises:
        ValorInvalidoError: Se o valor for inválido
        SaldoInsuficienteError: Se não houver saldo suficiente
        LimiteExcedidoError: Se exceder o limite da conta
    """
    # O método sacar() da conta já valida e lança exceções
    conta.sacar(valor)
    
    # Registra a transação
    transacao = Transacao(tipo="Saque", valor=valor, conta=conta)
    conta.transacoes.append(transacao)
    
    logger.info(f"Saque de R$ {valor:.2f} realizado na conta {conta.numero}")
    exibir_saque(valor)


def transferir(conta_origem: 'Conta', conta_destino: 'Conta', valor: float) -> None:
    """
    Transfere valor entre duas contas.
    
    Args:
        conta_origem: Conta que envia o valor
        conta_destino: Conta que recebe o valor
        valor: Valor a ser transferido
        
    Raises:
        ValorInvalidoError: Se o valor for inválido
        SaldoInsuficienteError: Se não houver saldo suficiente na origem
        LimiteExcedidoError: Se exceder o limite da conta origem
    """
    # Saca da conta origem (valida saldo/limite)
    conta_origem.sacar(valor)
    
    # Registra transação de saída
    transacao_saida = Transacao(
        tipo=f"Transf. para {conta_destino.numero}",
        valor=valor,
        conta=conta_origem
    )
    conta_origem.transacoes.append(transacao_saida)
    
    # Deposita na conta destino
    conta_destino.saldo += valor
    
    # Registra transação de entrada
    transacao_entrada = Transacao(
        tipo=f"Transf. de {conta_origem.numero}",
        valor=valor,
        conta=conta_destino
    )
    conta_destino.transacoes.append(transacao_entrada)
    
    logger.info(
        f"Transferência de R$ {valor:.2f} da conta {conta_origem.numero} "
        f"para conta {conta_destino.numero}"
    )


def aplicar_taxas(conta: 'Conta') -> None:
    """
    Aplica as taxas da conta (se houver).
    
    Delega para o método aplicar_taxas() da conta, que implementa
    as regras específicas de cada tipo de conta.
    
    Args:
        conta: Conta para aplicar as taxas
    """
    saldo_anterior = conta.saldo
    conta.aplicar_taxas()
    
    # Se houve mudança no saldo, foi cobrada taxa
    if conta.saldo < saldo_anterior:
        taxa_cobrada = saldo_anterior - conta.saldo
        
        # Registra transação
        transacao = Transacao(
            tipo="Taxa manutenção",
            valor=taxa_cobrada,
            conta=conta
        )
        conta.transacoes.append(transacao)
        
        logger.info(f"Taxa de R$ {taxa_cobrada:.2f} aplicada na conta {conta.numero}")
        exibir_taxa_manutencao(taxa_cobrada)
    else:
        # Poupança não tem taxa
        logger.info(f"Conta {conta.numero} não possui taxa de manutenção")
        exibir_sem_taxa_poupanca()


def calcular_imposto(conta: 'Conta') -> float:
    """
    Calcula o imposto devido sobre a conta (se aplicável).
    
    Args:
        conta: Conta para calcular o imposto
        
    Returns:
        Valor do imposto em reais (0 se não for tributável)
    """
    # Verifica se a conta é tributável (usando duck typing)
    if hasattr(conta, 'get_valor_imposto'):
        imposto = conta.get_valor_imposto()
        logger.info(f"Imposto calculado para conta {conta.numero}: R$ {imposto:.2f}")
        return imposto
    
    return 0.0


def calcular_rendimento(conta: 'Conta') -> float:
    """
    Calcula o rendimento da conta (se aplicável).
    
    Args:
        conta: Conta para calcular o rendimento
        
    Returns:
        Valor do rendimento em reais (0 se não for rentável)
    """
    # Verifica se a conta é rentável (usando duck typing)
    if hasattr(conta, 'get_rendimento'):
        rendimento = conta.get_rendimento()
        logger.info(f"Rendimento calculado para conta {conta.numero}: R$ {rendimento:.2f}")
        return rendimento
    
    return 0.0


def aplicar_rendimento(conta: 'Conta') -> None:
    """
    Aplica o rendimento ao saldo da conta (se aplicável).
    
    Args:
        conta: Conta para aplicar o rendimento
    """
    if hasattr(conta, 'get_rendimento'):
        rendimento = conta.get_rendimento()
        conta.saldo += rendimento
        
        # Registra transação
        transacao = Transacao(
            tipo="Rendimento",
            valor=rendimento,
            conta=conta
        )
        conta.transacoes.append(transacao)
        
        logger.info(f"Rendimento de R$ {rendimento:.2f} aplicado na conta {conta.numero}")
