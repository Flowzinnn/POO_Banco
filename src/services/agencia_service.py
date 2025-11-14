"""
Serviço de operações em agências bancárias.

Gerencia relacionamentos entre contas e agências.
"""

from typing import TYPE_CHECKING
from src.exceptions.banco_exceptions import ContaDuplicadaError, ContaNaoEncontradaError
from src.utils.logger import get_logger

if TYPE_CHECKING:
    from src.models.conta import Conta
    from src.models.agencia import Agencia

logger = get_logger("services.agencia")


def adicionar_conta_na_agencia(conta: 'Conta', agencia: 'Agencia') -> None:
    """
    Adiciona uma conta a uma agência (relacionamento bidirecional).
    
    Args:
        conta: Conta a ser adicionada
        agencia: Agência que receberá a conta
        
    Raises:
        ContaDuplicadaError: Se a conta já estiver na agência
    """
    # Verifica se a conta já está na agência
    if conta in agencia.contas:
        logger.warning(f"Tentativa de adicionar conta {conta.numero} já existente na agência {agencia.numero}")
        raise ContaDuplicadaError(conta.numero)
    
    # Adiciona a conta à agência
    agencia.contas.append(conta)
    
    logger.info(f"Conta {conta.numero} adicionada à agência {agencia.numero}")


def remover_conta_da_agencia(conta: 'Conta', agencia: 'Agencia') -> None:
    """
    Remove uma conta de uma agência.
    
    Args:
        conta: Conta a ser removida
        agencia: Agência de onde a conta será removida
        
    Raises:
        ContaNaoEncontradaError: Se a conta não estiver na agência
    """
    # Verifica se a conta está na agência
    if conta not in agencia.contas:
        logger.warning(f"Tentativa de remover conta {conta.numero} não encontrada na agência {agencia.numero}")
        raise ContaNaoEncontradaError(conta.numero)
    
    # Remove a conta da agência
    agencia.contas.remove(conta)
    
    logger.info(f"Conta {conta.numero} removida da agência {agencia.numero}")


def listar_contas_agencia(agencia: 'Agencia') -> list['Conta']:
    """
    Lista todas as contas de uma agência.
    
    Args:
        agencia: Agência para listar as contas
        
    Returns:
        Lista de contas da agência
    """
    logger.info(f"Listando {len(agencia.contas)} contas da agência {agencia.numero}")
    return agencia.contas


def buscar_conta_na_agencia(numero_conta: str, agencia: 'Agencia') -> 'Conta':
    """
    Busca uma conta específica em uma agência pelo número.
    
    Args:
        numero_conta: Número da conta a buscar
        agencia: Agência onde buscar
        
    Returns:
        Conta encontrada
        
    Raises:
        ContaNaoEncontradaError: Se a conta não for encontrada
    """
    for conta in agencia.contas:
        if conta.numero == numero_conta:
            logger.info(f"Conta {numero_conta} encontrada na agência {agencia.numero}")
            return conta
    
    logger.warning(f"Conta {numero_conta} não encontrada na agência {agencia.numero}")
    raise ContaNaoEncontradaError(numero_conta)
