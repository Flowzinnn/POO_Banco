"""
Interface para objetos que geram rendimento.

Define o contrato para cálculo de rendimentos sobre investimentos.
"""

from abc import ABC, abstractmethod


class Rentavel(ABC):
    """
    Interface para produtos financeiros que geram rendimento.
    
    Classes que implementam esta interface devem calcular o rendimento
    gerado pelo produto financeiro (ex: poupança, investimentos).
    """
    
    @abstractmethod
    def get_rendimento(self) -> float:
        """
        Calcula o valor do rendimento gerado.
        
        Returns:
            Valor do rendimento em reais
        """
        pass
