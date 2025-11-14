"""Model de Banco com validações Pydantic."""

from typing import List
from pydantic import BaseModel, field_validator
from src.models.endereco import Endereco
from src.models.agencia import Agencia
from src.utils.validators import validar_cnpj, validar_telefone
from src.exceptions.banco_exceptions import CNPJInvalidoError


class Banco(BaseModel):
    """Representa um banco com suas agências."""
    
    model_config = {'arbitrary_types_allowed': True}
    
    nome: str
    cnpj: str
    endereco: Endereco
    fone: str
    agencias: List[Agencia] = []
    
    @field_validator('cnpj')
    @classmethod
    def validar_cnpj_format(cls, v: str) -> str:
        """Valida o CNPJ usando o algoritmo oficial."""
        if not validar_cnpj(v):
            raise CNPJInvalidoError(v)
        return v
    
    @field_validator('fone')
    @classmethod
    def validar_telefone_formato(cls, v: str) -> str:
        """Valida o formato do telefone."""
        if not validar_telefone(v):
            raise ValueError(f"Telefone inválido: {v}")
        return v
    
    @field_validator('nome')
    @classmethod
    def validar_nome_nao_vazio(cls, v: str) -> str:
        """Valida que o nome não é vazio."""
        if not v.strip():
            raise ValueError("Nome do banco não pode ser vazio")
        return v.strip()
    
    def adicionar_agencia(self, *agencias: Agencia) -> None:
        """Adiciona uma ou mais agências ao banco."""
        for agencia in agencias:
            if agencia not in self.agencias:
                self.agencias.append(agencia)
    
    def __str__(self) -> str:
        return f"Banco: {self.nome}, CNPJ: {self.cnpj}, Endereço: {self.endereco}, Telefone: {self.fone}"
