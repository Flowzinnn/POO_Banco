"""Model de Agência com validações Pydantic."""

from typing import List, TYPE_CHECKING
from pydantic import BaseModel, field_validator
from src.models.endereco import Endereco
from src.utils.validators import validar_telefone

if TYPE_CHECKING:
    from src.models.conta import Conta


class Agencia(BaseModel):
    """Representa uma agência bancária."""
    
    model_config = {'arbitrary_types_allowed': True}
    
    nome: str
    numero: str
    endereco: Endereco
    fone: str
    contas: List['Conta'] = []
    
    @field_validator('fone')
    @classmethod
    def validar_telefone_formato(cls, v: str) -> str:
        """Valida o formato do telefone."""
        if not validar_telefone(v):
            raise ValueError(f"Telefone inválido: {v}")
        return v
    
    @field_validator('nome', 'numero')
    @classmethod
    def validar_campo_nao_vazio(cls, v: str) -> str:
        """Valida que o campo não é vazio."""
        if not v.strip():
            raise ValueError("Campo não pode ser vazio")
        return v.strip()
    
    def adicionar_conta(self, conta: 'Conta') -> None:
        """Adiciona uma conta à agência."""
        if conta not in self.contas:
            self.contas.append(conta)
    
    def remover_conta(self, conta: 'Conta') -> None:
        """Remove uma conta da agência."""
        if conta in self.contas:
            self.contas.remove(conta)
    
    def __str__(self) -> str:
        return f"Agência: {self.nome}, Número: {self.numero}, Endereço: {self.endereco}, Telefone: {self.fone}"
