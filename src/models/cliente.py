"""Model de Cliente com validações Pydantic."""

from typing import List, TYPE_CHECKING
from pydantic import field_validator
from src.models.pessoa import Pessoa

if TYPE_CHECKING:
    from src.models.conta import Conta


class Cliente(Pessoa):
    """
    Representa um cliente do banco.
    
    Clientes podem ter múltiplas contas associadas.
    """
    
    cnh: str
    contas: List['Conta'] = []
    
    @field_validator('cnh')
    @classmethod
    def validar_cnh_formato(cls, v: str) -> str:
        """Valida que a CNH tem formato básico."""
        cnh_limpo = v.replace(' ', '').replace('-', '')
        if not cnh_limpo.isdigit() or len(cnh_limpo) < 9:
            raise ValueError(f"CNH inválida: {v}. Deve conter pelo menos 9 dígitos")
        return v
    
    def adicionar_conta(self, conta: 'Conta') -> None:
        """Adiciona uma conta à lista de contas do cliente."""
        if conta not in self.contas:
            self.contas.append(conta)
    
    def __str__(self) -> str:
        return f"Cliente: {self.nome} | CPF: {self.cpf}"
