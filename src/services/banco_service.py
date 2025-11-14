"""
Serviço de operações em bancos.

Gerencia operações de alto nível no banco e suas agências.
"""

from typing import TYPE_CHECKING, List
from src.exceptions.banco_exceptions import AgenciaNaoEncontradaError
from src.utils.logger import get_logger

if TYPE_CHECKING:
    from src.models.banco import Banco
    from src.models.agencia import Agencia
    from src.models.conta import Conta

logger = get_logger("services.banco")


def buscar_agencia_por_numero(numero: str, banco: 'Banco') -> 'Agencia':
    """
    Busca uma agência pelo número dentro de um banco.
    
    Args:
        numero: Número da agência
        banco: Banco onde buscar
        
    Returns:
        Agência encontrada
        
    Raises:
        AgenciaNaoEncontradaError: Se a agência não for encontrada
    """
    for agencia in banco.agencias:
        if agencia.numero == numero:
            logger.info(f"Agência {numero} encontrada no banco {banco.nome}")
            return agencia
    
    logger.warning(f"Agência {numero} não encontrada no banco {banco.nome}")
    raise AgenciaNaoEncontradaError(numero)


def listar_todas_contas_banco(banco: 'Banco') -> List['Conta']:
    """
    Lista todas as contas de todas as agências do banco.
    
    Args:
        banco: Banco para listar as contas
        
    Returns:
        Lista de todas as contas do banco
    """
    todas_contas = []
    
    for agencia in banco.agencias:
        todas_contas.extend(agencia.contas)
    
    logger.info(f"Listadas {len(todas_contas)} contas no banco {banco.nome}")
    return todas_contas


def calcular_saldo_total_banco(banco: 'Banco') -> float:
    """
    Calcula o saldo total de todas as contas do banco.
    
    Args:
        banco: Banco para calcular o saldo total
        
    Returns:
        Saldo total em reais
    """
    saldo_total = 0.0
    
    for agencia in banco.agencias:
        for conta in agencia.contas:
            saldo_total += conta.saldo
    
    logger.info(f"Saldo total do banco {banco.nome}: R$ {saldo_total:,.2f}")
    return saldo_total


def calcular_numero_clientes(banco: 'Banco') -> int:
    """
    Calcula o número total de clientes únicos do banco.
    
    Args:
        banco: Banco para contar os clientes
        
    Returns:
        Número de clientes únicos
    """
    clientes_cpfs = set()
    
    for agencia in banco.agencias:
        for conta in agencia.contas:
            clientes_cpfs.add(conta.cliente.cpf)
    
    num_clientes = len(clientes_cpfs)
    logger.info(f"Número de clientes únicos no banco {banco.nome}: {num_clientes}")
    return num_clientes
