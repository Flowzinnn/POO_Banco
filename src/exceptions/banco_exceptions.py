"""
Exceções customizadas do sistema bancário.

Este módulo define a hierarquia de exceções específicas do domínio bancário,
cada uma com um código único para facilitar o rastreamento e tratamento de erros.
"""


class BancoError(Exception):
    """
    Exceção base para todos os erros do sistema bancário.
    
    Atributos:
        codigo: Código único do erro (formato: E###)
        mensagem: Descrição detalhada do erro
    """
    
    def __init__(self, codigo: str, mensagem: str) -> None:
        self.codigo = codigo
        self.mensagem = mensagem
        super().__init__(f"[{codigo}] {mensagem}")


class SaldoInsuficienteError(BancoError):
    """Lançada quando há tentativa de saque com saldo insuficiente."""
    
    def __init__(self, saldo_atual: float, valor_solicitado: float) -> None:
        super().__init__(
            "E001",
            f"Saldo insuficiente. Disponível: R$ {saldo_atual:.2f}, Solicitado: R$ {valor_solicitado:.2f}"
        )


class ValorInvalidoError(BancoError):
    """Lançada quando um valor monetário é inválido (negativo ou zero)."""
    
    def __init__(self, valor: float) -> None:
        super().__init__(
            "E002",
            f"Valor inválido: R$ {valor:.2f}. O valor deve ser positivo."
        )


class LimiteExcedidoError(BancoError):
    """Lançada quando o limite de crédito da conta é excedido."""
    
    def __init__(self, limite_disponivel: float, valor_solicitado: float) -> None:
        super().__init__(
            "E003",
            f"Limite excedido. Disponível: R$ {limite_disponivel:.2f}, Solicitado: R$ {valor_solicitado:.2f}"
        )


class AutenticacaoError(BancoError):
    """Lançada quando há falha na autenticação de usuário ou conta."""
    
    def __init__(self, mensagem: str = "Falha na autenticação") -> None:
        super().__init__("E004", mensagem)


class ContaDuplicadaError(BancoError):
    """Lançada quando há tentativa de criar conta com número já existente."""
    
    def __init__(self, numero_conta: str) -> None:
        super().__init__(
            "E005",
            f"Já existe uma conta com o número: {numero_conta}"
        )


class ClienteNaoEncontradoError(BancoError):
    """Lançada quando um cliente não é encontrado no sistema."""
    
    def __init__(self, identificador: str) -> None:
        super().__init__(
            "E006",
            f"Cliente não encontrado: {identificador}"
        )


class AgenciaNaoEncontradaError(BancoError):
    """Lançada quando uma agência não é encontrada no sistema."""
    
    def __init__(self, numero_agencia: str) -> None:
        super().__init__(
            "E007",
            f"Agência não encontrada: {numero_agencia}"
        )


class CPFInvalidoError(BancoError):
    """Lançada quando um CPF fornecido é inválido."""
    
    def __init__(self, cpf: str) -> None:
        super().__init__(
            "E008",
            f"CPF inválido: {cpf}"
        )


class CNPJInvalidoError(BancoError):
    """Lançada quando um CNPJ fornecido é inválido."""
    
    def __init__(self, cnpj: str) -> None:
        super().__init__(
            "E009",
            f"CNPJ inválido: {cnpj}"
        )


class IdadeInvalidaError(BancoError):
    """Lançada quando a idade do cliente é inválida (menor que 18 anos)."""
    
    def __init__(self, idade: int) -> None:
        super().__init__(
            "E010",
            f"Idade inválida: {idade} anos. Cliente deve ter pelo menos 18 anos."
        )


class ContaNaoEncontradaError(BancoError):
    """Lançada quando uma conta não é encontrada no sistema."""
    
    def __init__(self, numero_conta: str) -> None:
        super().__init__(
            "E011",
            f"Conta não encontrada: {numero_conta}"
        )
