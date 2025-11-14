"""
Interface para objetos tributáveis.

Define o contrato para cálculo de impostos sobre produtos financeiros.
"""

from abc import ABC, abstractmethod


class Tributavel(ABC):
    """
    Interface para entidades que estão sujeitas a tributação.
    
    Classes que implementam esta interface devem calcular o valor
    de imposto devido sobre o produto financeiro.
    """
    
    @abstractmethod
    def get_valor_imposto(self) -> float:
        """
        Calcula o valor do imposto devido.
        
        Returns:
            Valor do imposto em reais
        """
        pass
