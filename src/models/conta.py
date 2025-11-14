"""Model base de Conta com validações Pydantic."""

from abc import abstractmethod
from typing import List, TYPE_CHECKING
from pydantic import BaseModel, field_validator, ConfigDict
from src.interfaces.autenticavel import Autenticavel
from src.utils.security import verificar_senha

if TYPE_CHECKING:
    from src.models.cliente import Cliente
    from src.models.transacao import Transacao


class Conta(BaseModel, Autenticavel):
    """
    Classe base abstrata para contas bancárias.
    
    Define comportamentos comuns a todos os tipos de conta.
    """
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    numero: str
    cliente: 'Cliente'
    saldo: float
    senha_hash: str  # Armazena hash da senha, não a senha em texto plano
    transacoes: List['Transacao'] = []
    
    @field_validator('saldo')
    @classmethod
    def validar_saldo_nao_negativo(cls, v: float) -> float:
        """Valida que o saldo inicial não é negativo."""
        if v < 0:
            raise ValueError(f"Saldo não pode ser negativo. Recebido: R$ {v:.2f}")
        return v
    
    @field_validator('numero')
    @classmethod
    def validar_numero_nao_vazio(cls, v: str) -> str:
        """Valida que o número da conta não é vazio."""
        if not v.strip():
            raise ValueError("Número da conta não pode ser vazio")
        return v.strip()
    
    def autenticar(self, senha: str) -> bool:
        """Autentica usando verificação segura de hash."""
        return verificar_senha(senha, self.senha_hash)
    
    @abstractmethod
    def sacar(self, valor: float) -> None:
        """Método abstrato para saque (implementado pelas subclasses)."""
        pass
    
    @abstractmethod
    def aplicar_taxas(self) -> None:
        """Método abstrato para aplicação de taxas (implementado pelas subclasses)."""
        pass
    
    def __str__(self) -> str:
        return f"Conta Nº {self.numero} | Saldo: R$ {self.saldo:,.2f}"
