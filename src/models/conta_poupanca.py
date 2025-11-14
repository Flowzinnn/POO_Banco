"""Model de Conta Poupança com validações Pydantic."""

from pydantic import field_validator
from src.models.conta import Conta
from src.interfaces.rentavel import Rentavel
from src.exceptions.banco_exceptions import ValorInvalidoError, SaldoInsuficienteError


class ContaPoupanca(Conta, Rentavel):
    """
    Representa uma conta poupança com rendimento.
    
    Não permite saque além do saldo disponível e não possui taxas.
    Gera rendimento baseado em uma taxa percentual.
    """
    
    taxa_rendimento: float
    data_aniversario: int
    
    @field_validator('taxa_rendimento')
    @classmethod
    def validar_taxa_positiva(cls, v: float) -> float:
        """Valida que a taxa de rendimento é positiva."""
        if v <= 0:
            raise ValueError(f"Taxa de rendimento deve ser positiva. Recebido: {v}%")
        return v
    
    @field_validator('data_aniversario')
    @classmethod
    def validar_dia_mes(cls, v: int) -> int:
        """Valida que o dia do aniversário está entre 1 e 31."""
        if not 1 <= v <= 31:
            raise ValueError(f"Dia de aniversário deve estar entre 1 e 31. Recebido: {v}")
        return v
    
    def sacar(self, valor: float) -> None:
        """
        Realiza saque apenas se houver saldo suficiente.
        
        Raises:
            ValorInvalidoError: Se o valor for inválido
            SaldoInsuficienteError: Se não houver saldo suficiente
        """
        if valor <= 0:
            raise ValorInvalidoError(valor)
        
        if valor > self.saldo:
            raise SaldoInsuficienteError(self.saldo, valor)
        
        self.saldo -= valor
    
    def aplicar_taxas(self) -> None:
        """Poupança não possui taxa de manutenção."""
        pass  # Sem taxa
    
    def get_rendimento(self) -> float:
        """Calcula o rendimento baseado na taxa percentual."""
        return self.saldo * (self.taxa_rendimento / 100)
    
    def __str__(self) -> str:
        return f"Conta Poupança Nº {self.numero} | Saldo: R$ {self.saldo:,.2f} | Rendimento: {self.taxa_rendimento:.2f}%"
