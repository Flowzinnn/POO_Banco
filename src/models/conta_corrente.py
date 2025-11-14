"""Model de Conta Corrente com validações Pydantic."""

from pydantic import field_validator
from src.models.conta import Conta
from src.interfaces.tributavel import Tributavel
from src.exceptions.banco_exceptions import ValorInvalidoError, LimiteExcedidoError


class ContaCorrente(Conta, Tributavel):
    """
    Representa uma conta corrente com limite de crédito.
    
    Permite saques até o limite (saldo + limite adicional) e está
    sujeita a tributação e taxa de manutenção.
    """
    
    limite: float
    taxa_manutencao: float = 10.0
    
    @field_validator('limite')
    @classmethod
    def validar_limite_nao_negativo(cls, v: float) -> float:
        """Valida que o limite não é negativo."""
        if v < 0:
            raise ValueError(f"Limite não pode ser negativo. Recebido: R$ {v:.2f}")
        return v
    
    def sacar(self, valor: float) -> None:
        """
        Realiza saque respeitando saldo + limite.
        
        Raises:
            ValorInvalidoError: Se o valor for inválido
            LimiteExcedidoError: Se exceder saldo + limite
        """
        if valor <= 0:
            raise ValorInvalidoError(valor)
        
        limite_total = self.saldo + self.limite
        if valor > limite_total:
            raise LimiteExcedidoError(limite_total, valor)
        
        self.saldo -= valor
    
    def aplicar_taxas(self) -> None:
        """Aplica a taxa de manutenção mensal."""
        self.saldo -= self.taxa_manutencao
    
    def get_valor_imposto(self) -> float:
        """Calcula imposto de 7% sobre o saldo."""
        return self.saldo * 0.07
    
    def __str__(self) -> str:
        return f"Conta Corrente Nº {self.numero} | Saldo: R$ {self.saldo:,.2f} | Limite: R$ {self.limite:,.2f}"
