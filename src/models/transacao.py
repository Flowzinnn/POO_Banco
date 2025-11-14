"""Model de Transação com validações Pydantic."""

from datetime import datetime
from typing import TYPE_CHECKING
from pydantic import BaseModel, field_validator

if TYPE_CHECKING:
    from src.models.conta import Conta


class Transacao(BaseModel):
    """Representa uma transação financeira em uma conta."""
    
    tipo: str
    valor: float
    conta: 'Conta'
    data: datetime = datetime.now()
    
    model_config = {'arbitrary_types_allowed': True}
    
    @field_validator('valor')
    @classmethod
    def validar_valor_positivo(cls, v: float) -> float:
        """Valida que o valor da transação é positivo."""
        if v <= 0:
            raise ValueError(f"Valor da transação deve ser positivo. Recebido: R$ {v:.2f}")
        return v
    
    @field_validator('tipo')
    @classmethod
    def validar_tipo_nao_vazio(cls, v: str) -> str:
        """Valida que o tipo não é vazio."""
        if not v.strip():
            raise ValueError("Tipo de transação não pode ser vazio")
        return v.strip()
    
    def __str__(self) -> str:
        data_formatada = self.data.strftime('%d/%m/%Y %H:%M')
        valor_formatado = f"R$ {self.valor:,.2f}"
        return f"{data_formatada} | {self.tipo:<10} | {valor_formatado.rjust(12)}"
