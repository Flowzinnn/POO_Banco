"""Model de Endereço com validações Pydantic."""

from pydantic import BaseModel, field_validator
from src.utils.validators import validar_cep


class Endereco(BaseModel):
    """Representa um endereço brasileiro."""
    
    cep: str
    numero: str
    rua: str
    bairro: str
    cidade: str
    estado: str
    
    @field_validator('cep')
    @classmethod
    def validar_formato_cep(cls, v: str) -> str:
        """Valida o formato do CEP."""
        if not validar_cep(v):
            raise ValueError(f"CEP inválido: {v}. Use o formato 00000-000 ou 00000000")
        return v
    
    @field_validator('estado')
    @classmethod
    def validar_sigla_estado(cls, v: str) -> str:
        """Valida a sigla do estado (2 letras maiúsculas)."""
        if len(v) != 2 or not v.isupper() or not v.isalpha():
            raise ValueError(f"Estado deve ser sigla de 2 letras maiúsculas. Recebido: {v}")
        return v
    
    def __str__(self) -> str:
        return f"{self.rua}, {self.numero}, {self.bairro}, {self.cidade} - {self.estado}, CEP: {self.cep}"
