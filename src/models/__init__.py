"""Models de domínio do sistema bancário."""

# Importação ordenada para resolver referências circulares do Pydantic
from src.models.endereco import Endereco
from src.models.pessoa import Pessoa
from src.models.funcionario import Funcionario
from src.models.transacao import Transacao
from src.models.conta import Conta
from src.models.conta_corrente import ContaCorrente
from src.models.conta_poupanca import ContaPoupanca
from src.models.cliente import Cliente
from src.models.agencia import Agencia
from src.models.banco import Banco

# Resolve referências circulares do Pydantic
# Ordem importante: primeiro Cliente, depois as contas que dependem dele, depois Transacao
Cliente.model_rebuild()
ContaCorrente.model_rebuild()
ContaPoupanca.model_rebuild()
Transacao.model_rebuild()
Agencia.model_rebuild()
Banco.model_rebuild()

__all__ = [
    'Endereco',
    'Pessoa',
    'Funcionario',
    'Transacao',
    'Conta',
    'ContaCorrente',
    'ContaPoupanca',
    'Cliente',
    'Agencia',
    'Banco',
]