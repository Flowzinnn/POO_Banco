"""
Model de Usuário do sistema bancário.

Representa um usuário com credenciais de acesso ao sistema.
"""

from typing import Literal
from pydantic import BaseModel, field_validator


class Usuario(BaseModel):
    """
    Representa um usuário do sistema bancário.
    
    Usuários têm credenciais (username e senha_hash) e uma role
    que determina suas permissões no sistema.
    """
    
    username: str
    senha_hash: str
    role: Literal["admin", "cliente", "funcionario"]
    ativo: bool = True
    
    @field_validator('username')
    @classmethod
    def validar_username(cls, v: str) -> str:
        """Valida que o username tem formato adequado."""
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username deve ter pelo menos 3 caracteres")
        if not v.replace('_', '').isalnum():
            raise ValueError("Username deve conter apenas letras, números e underscore")
        return v
    
    def __str__(self) -> str:
        status = "Ativo" if self.ativo else "Inativo"
        return f"Usuário: {self.username} | Role: {self.role} | Status: {status}"
