"""Model base de Pessoa com validações Pydantic."""

from abc import ABC
from datetime import date, datetime
from pydantic import BaseModel, field_validator, ConfigDict
from src.utils.validators import validar_cpf
from src.exceptions.banco_exceptions import CPFInvalidoError, IdadeInvalidaError


class Pessoa(BaseModel, ABC):
    """
    Classe base abstrata para pessoas no sistema bancário.
    
    Representa dados comuns a clientes e funcionários.
    """
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    nome: str
    cpf: str
    data_nascimento: date
    
    @field_validator('cpf')
    @classmethod
    def validar_cpf_format(cls, v: str) -> str:
        """Valida o CPF usando o algoritmo oficial."""
        if not validar_cpf(v):
            raise CPFInvalidoError(v)
        return v
    
    @field_validator('data_nascimento')
    @classmethod
    def validar_idade_minima(cls, v: date) -> date:
        """Valida que a pessoa tem pelo menos 18 anos."""
        hoje = datetime.now().date()
        idade = hoje.year - v.year - ((hoje.month, hoje.day) < (v.month, v.day))
        
        if idade < 18:
            raise IdadeInvalidaError(idade)
        
        return v
    
    @field_validator('nome')
    @classmethod
    def validar_nome_nao_vazio(cls, v: str) -> str:
        """Valida que o nome não é vazio."""
        if not v.strip():
            raise ValueError("Nome não pode ser vazio")
        return v.strip()
