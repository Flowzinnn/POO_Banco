"""
Interface para objetos autenticáveis.

Define o contrato que classes devem implementar para suportar autenticação.
"""

from abc import ABC, abstractmethod


class Autenticavel(ABC):
    """
    Interface para entidades que requerem autenticação por senha.
    
    Classes que implementam esta interface devem fornecer um mecanismo
    de autenticação baseado em senha.
    """
    
    @abstractmethod
    def autenticar(self, senha: str) -> bool:
        """
        Autentica o objeto com a senha fornecida.
        
        Args:
            senha: Senha a ser verificada
            
        Returns:
            True se a autenticação for bem-sucedida, False caso contrário
        """
        pass
