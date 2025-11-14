"""
Views para apresentação no console usando logging.

Substitui os prints diretos por logging estruturado mantendo
a formatação visual.
"""

from typing import TYPE_CHECKING
from src.utils.logger import get_logger

if TYPE_CHECKING:
    from src.models.conta import Conta
    from src.models.transacao import Transacao
    from src.models.agencia import Agencia


logger = get_logger("views")


def exibir_deposito(valor: float) -> None:
    """Exibe mensagem de depósito realizado com sucesso."""
    logger.info(f"Depósito de R$ {valor:.2f} realizado com sucesso")


def exibir_saque(valor: float) -> None:
    """Exibe mensagem de saque realizado com sucesso."""
    logger.info(f"Saque de R$ {valor:.2f} realizado com sucesso")


def exibir_erro_valor_invalido() -> None:
    """Exibe mensagem de erro para valor inválido."""
    logger.warning("Valor inválido")


def exibir_erro_saldo_insuficiente() -> None:
    """Exibe mensagem de erro para saldo insuficiente."""
    logger.error("Saldo insuficiente")


def exibir_erro_limite_excedido() -> None:
    """Exibe mensagem de erro para limite excedido."""
    logger.error("Valor excede o limite da conta")


def exibir_taxa_manutencao(valor: float) -> None:
    """Exibe mensagem de aplicação de taxa de manutenção."""
    logger.info(f"Taxa de manutenção de R$ {valor:.2f} aplicada")


def exibir_sem_taxa_poupanca() -> None:
    """Exibe mensagem informando que poupança não tem taxa."""
    logger.info("Conta Poupança não possui taxa de manutenção")


def exibir_extrato(conta: 'Conta') -> None:
    """
    Exibe o extrato completo de uma conta.
    
    Args:
        conta: Conta para exibir o extrato
    """
    # Cabeçalho
    print("\n" + "="*40)
    print(f"{'EXTRATO BANCÁRIO':^40}")
    print("="*40)
    print(f"Conta: {conta.numero}")
    print(f"Cliente: {conta.cliente.nome}")
    print("-"*40)
    
    # Transações
    if not conta.transacoes:
        print("Nenhuma transação realizada")
        logger.info(f"Extrato consultado - Conta {conta.numero} sem transações")
    else:
        for transacao in conta.transacoes:
            print(transacao)
        logger.info(f"Extrato consultado - Conta {conta.numero} com {len(conta.transacoes)} transações")
    
    # Rodapé
    print("="*40)
    print(f"{'Saldo atual:':<27} R$ {conta.saldo:,.2f}")
    print("="*40 + "\n")


def exibir_lista_contas(cliente_nome: str, contas: list) -> None:
    """
    Exibe lista de contas de um cliente.
    
    Args:
        cliente_nome: Nome do cliente
        contas: Lista de contas do cliente
    """
    print(f"\nContas de {cliente_nome}:")
    
    if not contas:
        print("Nenhuma conta cadastrada")
        logger.info(f"Cliente {cliente_nome} não possui contas")
    else:
        for i, conta in enumerate(contas, 1):
            print(f"{i}. {conta}")
        logger.info(f"Listadas {len(contas)} contas do cliente {cliente_nome}")


def exibir_lista_agencias(nome_banco: str, agencias: list['Agencia']) -> None:
    """
    Exibe lista de agências de um banco.
    
    Args:
        nome_banco: Nome do banco
        agencias: Lista de agências
    """
    print(f"\nAgências do {nome_banco}:")
    
    if not agencias:
        print("Não há agências cadastradas")
        logger.warning(f"Banco {nome_banco} sem agências cadastradas")
    else:
        for agencia in agencias:
            print(f"- {agencia.nome} | Nº: {agencia.numero} | {agencia.endereco} | {agencia.fone}")
        logger.info(f"Listadas {len(agencias)} agências do banco {nome_banco}")


def exibir_erro(erro: Exception) -> None:
    """
    Exibe uma mensagem de erro formatada.
    
    Args:
        erro: Exceção capturada
    """
    logger.error(f"Erro: {str(erro)}")


def exibir_sucesso(mensagem: str) -> None:
    """
    Exibe uma mensagem de sucesso.
    
    Args:
        mensagem: Mensagem a exibir
    """
    logger.info(mensagem)


def exibir_aviso(mensagem: str) -> None:
    """
    Exibe uma mensagem de aviso.
    
    Args:
        mensagem: Mensagem a exibir
    """
    logger.warning(mensagem)
