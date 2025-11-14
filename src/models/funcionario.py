"""Model de Funcionário com validações Pydantic."""

from pydantic import field_validator
from src.models.pessoa import Pessoa


class Funcionario(Pessoa):
    """Representa um funcionário do banco."""
    
    cargo: str
    matricula: str
    salario: float
    
    @field_validator('salario')
    @classmethod
    def validar_salario_positivo(cls, v: float) -> float:
        """Valida que o salário é positivo."""
        if v <= 0:
            raise ValueError(f"Salário deve ser positivo. Recebido: R$ {v:.2f}")
        return v
    
    @field_validator('cargo', 'matricula')
    @classmethod
    def validar_campo_nao_vazio(cls, v: str) -> str:
        """Valida que o campo não é vazio."""
        if not v.strip():
            raise ValueError("Campo não pode ser vazio")
        return v.strip()
    
    def __str__(self) -> str:
        return f"Funcionário: {self.nome} | Cargo: {self.cargo} | Matrícula: {self.matricula}"
