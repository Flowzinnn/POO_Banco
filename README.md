# 🏦 Sistema Bancário Modular - POO em Python

Sistema bancário completo desenvolvido em Python para estudo de **Programação Orientada a Objetos (POO)**, demonstrando conceitos avançados e boas práticas de desenvolvimento.

## 📚 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Conceitos de POO Aplicados](#conceitos-de-poo-aplicados)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação e Configuração](#instalação-e-configuração)
- [Como Usar](#como-usar)
- [Funcionalidades](#funcionalidades)
- [Modelos de Domínio](#modelos-de-domínio)
- [Serviços](#serviços)
- [Sistema de Exceções](#sistema-de-exceções)
- [Testes](#testes)
- [Comparação v1 vs v2](#comparação-v1-vs-v2)

---

## 🎯 Sobre o Projeto

Este projeto implementa um **sistema bancário completo** com duas versões:

- **v1 (Legado)**: Código monolítico em arquivo único ([banco2.py](banco2.py)) - demonstra código sem arquitetura
- **v2 (Refatorado)**: Arquitetura modular com separação de responsabilidades - demonstra boas práticas

### Objetivos Didáticos

✅ Demonstrar evolução de código monolítico para arquitetura limpa  
✅ Aplicar todos os pilares da POO (Abstração, Encapsulamento, Herança, Polimorfismo)  
✅ Implementar padrões de projeto (Service Layer, Repository Pattern)  
✅ Usar validações robustas com Pydantic  
✅ Implementar segurança (hash de senhas com bcrypt)  
✅ Criar sistema de logging profissional  
✅ Desenvolver testes unitários e de integração  

---

## 🧩 Conceitos de POO Aplicados

### 1️⃣ **Abstração**

Classes abstratas definem contratos que as subclasses devem implementar:

```python
# src/models/conta.py
class Conta(BaseModel, Autenticavel):
    """Classe base abstrata para contas bancárias"""
    
    @abstractmethod
    def sacar(self, valor: float) -> None:
        """Cada tipo de conta implementa sua regra de saque"""
        pass
```

### 2️⃣ **Encapsulamento**

Dados protegidos com validações automáticas via Pydantic:

```python
# src/models/conta_corrente.py
class ContaCorrente(Conta):
    limite: float
    
    @field_validator('limite')
    def validar_limite_positivo(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Limite não pode ser negativo")
        return v
```

### 3️⃣ **Herança**

Reutilização de código através de hierarquia de classes:

```
Pessoa (ABC)
├── Cliente
│   └── Pode ter múltiplas contas
└── Funcionario
    └── Tem matrícula e salário

Conta (ABC)
├── ContaCorrente (implementa Tributavel)
│   └── Tem limite de crédito
└── ContaPoupanca (implementa Rentavel)
    └── Gera rendimento
```

### 4️⃣ **Polimorfismo**

Objetos diferentes respondem à mesma interface de forma específica:

```python
# Ambas são contas, mas comportamento de saque é diferente
conta_corrente.sacar(1500)  # Usa saldo + limite
conta_poupanca.sacar(1500)  # Apenas saldo disponível
```

### 5️⃣ **Interfaces (Protocolos)**

Contratos que garantem comportamento específico:

```python
# src/interfaces/autenticavel.py
class Autenticavel(ABC):
    @abstractmethod
    def autenticar(self, senha: str) -> bool:
        """Todo objeto autenticável deve poder verificar senha"""
        pass
```

---

## 🏗️ Arquitetura do Sistema

O sistema v2 segue a arquitetura em camadas:

```
┌─────────────────────────────────────────┐
│           MAIN.PY (Entry Point)         │
│  - Menu interativo                      │
│  - Seleção de versão (v1/v2)           │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│          VIEWS (Apresentação)           │
│  - console_view.py                      │
│  - Formatação de saída                  │
│  - Logging visual                       │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│        SERVICES (Lógica de Negócio)     │
│  - conta_service.py                     │
│  - agencia_service.py                   │
│  - banco_service.py                     │
│  - Orquestração de operações            │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         MODELS (Domínio)                │
│  - Conta, Cliente, Banco, Agencia       │
│  - Validações Pydantic                  │
│  - Regras de negócio básicas            │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│    UTILS / INTERFACES / EXCEPTIONS      │
│  - Validadores (CPF, CNPJ, CEP)         │
│  - Segurança (bcrypt)                   │
│  - Logger profissional                  │
│  - Exceções customizadas                │
└─────────────────────────────────────────┘
```

### Princípios SOLID Aplicados

- **S**ingle Responsibility: Cada classe tem uma única responsabilidade
- **O**pen/Closed: Aberto para extensão, fechado para modificação
- **L**iskov Substitution: Subtipos podem substituir tipos base
- **I**nterface Segregation: Interfaces específicas (Autenticavel, Tributavel, Rentavel)
- **D**ependency Inversion: Depende de abstrações, não de implementações

---

## 📁 Estrutura de Pastas

```
POO_Banco/
│
├── banco2.py                 # ❌ v1 - Código legado monolítico
├── main.py                   # ✅ Ponto de entrada com menu
│
├── src/                      # ✅ v2 - Código refatorado
│   ├── __init__.py
│   ├── py.typed              # Suporte para type checking
│   │
│   ├── models/               # 📦 Modelos de domínio (Pydantic)
│   │   ├── __init__.py
│   │   ├── pessoa.py         # Classe base abstrata
│   │   ├── cliente.py        # Cliente herda de Pessoa
│   │   ├── funcionario.py    # Funcionário herda de Pessoa
│   │   ├── conta.py          # Conta base abstrata
│   │   ├── conta_corrente.py # Implementação específica
│   │   ├── conta_poupanca.py # Implementação específica
│   │   ├── agencia.py        # Agência bancária
│   │   ├── banco.py          # Banco com agências
│   │   ├── endereco.py       # Endereço (reutilizável)
│   │   └── transacao.py      # Registro de operações
│   │
│   ├── services/             # 🔧 Lógica de negócio
│   │   ├── __init__.py
│   │   ├── conta_service.py      # Operações em contas
│   │   ├── agencia_service.py    # Gestão de agências
│   │   └── banco_service.py      # Operações bancárias
│   │
│   ├── views/                # 🖥️ Apresentação
│   │   ├── __init__.py
│   │   └── console_view.py   # Saída formatada com logging
│   │
│   ├── interfaces/           # 📋 Contratos (ABC)
│   │   ├── __init__.py
│   │   ├── autenticavel.py   # Interface para autenticação
│   │   ├── tributavel.py     # Interface para cálculo de impostos
│   │   └── rentavel.py       # Interface para rendimentos
│   │
│   ├── exceptions/           # ⚠️ Exceções customizadas
│   │   ├── __init__.py
│   │   └── banco_exceptions.py
│   │
│   ├── utils/                # 🛠️ Utilitários
│   │   ├── __init__.py
│   │   ├── validators.py     # Validadores (CPF, CNPJ, CEP)
│   │   ├── security.py       # Hash de senhas (bcrypt)
│   │   └── logger.py         # Sistema de logging
│   │
│   └── auth/                 # 🔐 Autenticação
│       ├── __init__.py
│       ├── usuario.py        # Model de usuário
│       ├── session_manager.py # Gerenciamento de sessões
│       └── auth_service.py   # Serviço de autenticação
│
├── tests/                    # 🧪 Testes automatizados
│   ├── __init__.py
│   ├── conftest.py          # Fixtures compartilhadas
│   ├── unit/                # Testes unitários
│   │   ├── test_models.py
│   │   └── test_services.py
│   └── integration/         # Testes de integração
│       └── test_fluxo_completo.py
│
├── logs/                    # 📝 Arquivos de log
│   └── banco.log
│
├── requirements.txt         # 📦 Dependências
├── pyproject.toml          # ⚙️ Configurações do projeto
└── .env                    # 🔒 Variáveis de ambiente
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Propósito |
|------------|-----------|
| **Python 3.11+** | Linguagem base |
| **Pydantic** | Validação de dados e modelos |
| **bcrypt** | Hash seguro de senhas |
| **pytest** | Framework de testes |
| **pytest-cov** | Cobertura de testes |
| **mypy** | Verificação de tipos estáticos |
| **colorama** | Cores no terminal |

---

## ⚙️ Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd POO_Banco
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Execute o sistema**
```bash
python main.py
```

---

## 🚀 Como Usar

### Menu Principal

Ao executar `python main.py`, você verá:

```
════════════════════════════════════════════════════════════
                  SISTEMA BANCÁRIO MODULAR
════════════════════════════════════════════════════════════

[1] Rodar Sistema v1 (Legado)
[2] Rodar Sistema v2 (Refatorado)
[3] Menu Desenvolvedor
[0] Sair
```

### Opção 1: Sistema v1 (Legado)

Executa o código original em [banco2.py](banco2.py) - útil para comparação.

### Opção 2: Sistema v2 (Refatorado)

Executa a versão moderna com arquitetura limpa. Demonstra:
- Criação de banco e agências
- Cadastro de clientes
- Abertura de contas
- Operações bancárias (depósito, saque, transferência)
- Extrato de movimentações

### Opção 3: Menu Desenvolvedor

Ferramentas para desenvolvimento:

```
[1] Rodar Testes Unitários
[2] Rodar Testes de Integração
[3] Rodar Todos os Testes
[4] Validar Tipos com mypy
[5] Ver Últimas 50 Linhas do Log
[6] Limpar Arquivos de Log
[7] Cobertura de Testes
```

---

## 💼 Funcionalidades

### Operações Bancárias

| Operação | Descrição |
|----------|-----------|
| **Depósito** | Adiciona valor ao saldo da conta |
| **Saque** | Remove valor (valida saldo/limite) |
| **Transferência** | Move valor entre contas |
| **Extrato** | Lista todas as transações |
| **Aplicar Taxas** | Cobra taxa de manutenção (só corrente) |
| **Aplicar Rendimento** | Adiciona rendimento (só poupança) |

### Validações Automáticas

✅ **CPF**: Validação com dígitos verificadores  
✅ **CNPJ**: Validação com dígitos verificadores  
✅ **CEP**: Formato brasileiro (99999-999)  
✅ **Idade**: Mínimo 18 anos para clientes  
✅ **Valores**: Sempre positivos  
✅ **Saldo**: Não pode ficar negativo  

---

## 📦 Modelos de Domínio

### Hierarquia de Pessoas

```python
# src/models/pessoa.py
class Pessoa(BaseModel, ABC):
    """Classe base com dados comuns"""
    nome: str
    cpf: str
    data_nascimento: date
```

```python
# src/models/cliente.py
class Cliente(Pessoa):
    """Cliente do banco"""
    cnh: str
    contas: List[Conta] = []
```

```python
# src/models/funcionario.py
class Funcionario(Pessoa):
    """Funcionário do banco"""
    cargo: str
    matricula: str
    salario: float
```

### Hierarquia de Contas

```python
# src/models/conta.py
class Conta(BaseModel, Autenticavel):
    """Classe base para contas"""
    numero: str
    cliente: Cliente
    saldo: float
    senha_hash: str
    transacoes: List[Transacao] = []
    
    @abstractmethod
    def sacar(self, valor: float) -> None:
        pass
```

```python
# src/models/conta_corrente.py
class ContaCorrente(Conta, Tributavel):
    """Conta corrente com limite"""
    limite: float
    taxa_manutencao: float
    
    def sacar(self, valor: float) -> None:
        # Pode usar saldo + limite
        if valor > self.saldo + self.limite:
            raise LimiteExcedidoError(...)
```

```python
# src/models/conta_poupanca.py
class ContaPoupanca(Conta, Rentavel):
    """Conta poupança com rendimento"""
    taxa_rendimento: float
    data_aniversario: int
    
    def sacar(self, valor: float) -> None:
        # Só pode usar saldo disponível
        if valor > self.saldo:
            raise SaldoInsuficienteError(...)
```

### Estrutura Bancária

```python
# src/models/banco.py
class Banco(BaseModel):
    nome: str
    cnpj: str
    endereco: Endereco
    fone: str
    agencias: List[Agencia] = []
```

```python
# src/models/agencia.py
class Agencia(BaseModel):
    nome: str
    numero: str
    endereco: Endereco
    fone: str
    contas: List[Conta] = []
```

---

## 🔧 Serviços

### ContaService ([src/services/conta_service.py](src/services/conta_service.py))

Gerencia operações em contas:

```python
def realizar_deposito(conta: Conta, valor: float) -> None:
    """Adiciona valor ao saldo"""

def realizar_saque(conta: Conta, valor: float) -> None:
    """Remove valor (delega para conta.sacar())"""

def transferir(origem: Conta, destino: Conta, valor: float) -> None:
    """Transfere entre contas"""

def aplicar_taxas(conta: Conta) -> None:
    """Cobra taxa de manutenção"""

def calcular_imposto(conta: Conta) -> float:
    """Calcula imposto (se tributável)"""

def calcular_rendimento(conta: Conta) -> float:
    """Calcula rendimento (se rentável)"""
```

### AgenciaService ([src/services/agencia_service.py](src/services/agencia_service.py))

Gerencia contas em agências:

```python
def adicionar_conta_na_agencia(conta: Conta, agencia: Agencia) -> None:
def remover_conta_da_agencia(conta: Conta, agencia: Agencia) -> None:
def listar_contas_agencia(agencia: Agencia) -> List[Conta]:
def buscar_conta_na_agencia(numero: str, agencia: Agencia) -> Conta:
```

### BancoService ([src/services/banco_service.py](src/services/banco_service.py))

Operações de alto nível:

```python
def buscar_agencia_por_numero(numero: str, banco: Banco) -> Agencia:
def listar_todas_contas_banco(banco: Banco) -> List[Conta]:
def calcular_saldo_total_banco(banco: Banco) -> float:
def calcular_numero_clientes(banco: Banco) -> int:
```

---

## ⚠️ Sistema de Exceções

Hierarquia organizada com códigos únicos:

```python
# src/exceptions/banco_exceptions.py

class BancoError(Exception):
    """Exceção base - código E###"""

├── SaldoInsuficienteError      # E001
├── ValorInvalidoError          # E002
├── LimiteExcedidoError         # E003
├── AutenticacaoError           # E004
├── ContaDuplicadaError         # E005
├── ClienteNaoEncontradoError   # E006
├── AgenciaNaoEncontradaError   # E007
├── CPFInvalidoError            # E008
├── CNPJInvalidoError           # E009
├── IdadeInvalidaError          # E010
└── ContaNaoEncontradaError     # E011
```

### Exemplo de Uso

```python
try:
    conta.sacar(5000)
except SaldoInsuficienteError as e:
    print(f"{e.codigo}: {e.mensagem}")
    # [E001] Saldo insuficiente. Disponível: R$ 100.00, Solicitado: R$ 5000.00
```

---

## 🧪 Testes

### Estrutura de Testes

```
tests/
├── conftest.py              # Fixtures compartilhadas
├── unit/                    # Testes isolados
│   ├── test_models.py       # Testa validações Pydantic
│   └── test_services.py     # Testa lógica de negócio
└── integration/             # Testes de fluxo
    └── test_fluxo_completo.py
```

### Fixtures Disponíveis ([tests/conftest.py](tests/conftest.py))

```python
@pytest.fixture
def endereco_padrao() -> Endereco:
    """Endereço válido padrão"""

@pytest.fixture
def cliente_padrao() -> Cliente:
    """Cliente válido padrão"""

@pytest.fixture
def conta_corrente_padrao() -> ContaCorrente:
    """Conta corrente com R$ 1000"""

@pytest.fixture
def agencia_padrao() -> Agencia:
    """Agência válida"""

@pytest.fixture
def banco_padrao() -> Banco:
    """Banco com uma agência"""
```

### Executar Testes

```bash
# Todos os testes
pytest

# Testes unitários
pytest tests/unit

# Testes de integração
pytest tests/integration

# Com cobertura
pytest --cov=src --cov-report=term-missing

# Verboso
pytest -v
```

### Exemplo de Teste Unitário

```python
def test_saque_conta_corrente_com_sucesso(conta_corrente_padrao):
    """Testa saque válido em conta corrente"""
    conta_service.realizar_saque(conta_corrente_padrao, 500.0)
    
    assert conta_corrente_padrao.saldo == 500.0
    assert len(conta_corrente_padrao.transacoes) == 1
```

### Exemplo de Teste de Integração

```python
def test_fluxo_completo_abertura_conta_e_operacoes():
    """Testa fluxo completo do sistema"""
    # 1. Criar estrutura bancária
    banco = Banco(...)
    agencia = Agencia(...)
    
    # 2. Criar cliente e conta
    cliente = Cliente(...)
    conta = ContaCorrente(...)
    
    # 3. Realizar operações
    conta_service.realizar_deposito(conta, 500.0)
    conta_service.realizar_saque(conta, 200.0)
    
    # 4. Verificar resultados
    assert conta.saldo == 300.0
    assert len(conta.transacoes) == 2
```

---

## 🔄 Comparação v1 vs v2

### Versão 1 (Legado) - [banco2.py](banco2.py)

❌ **Problemas:**
- Código monolítico (600+ linhas em um arquivo)
- Senhas em texto plano
- Prints espalhados (dificulta testes)
- Sem separação de responsabilidades
- Difícil de testar
- Difícil de manter

```python
# Exemplo v1
class Conta:
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"✅ Depósito de R$ {valor:.2f} realizado")
        else:
            print("⚠️ Valor inválido")
```

### Versão 2 (Refatorada) - [src/](src/)

✅ **Melhorias:**
- Arquitetura em camadas
- Senhas com hash bcrypt
- Logging profissional
- Validações Pydantic
- Facilmente testável
- Manutenível e extensível

```python
# Exemplo v2
# src/services/conta_service.py
def realizar_deposito(conta: Conta, valor: float) -> None:
    if valor <= 0:
        raise ValorInvalidoError(valor)
    
    conta.saldo += valor
    transacao = Transacao(tipo="Depósito", valor=valor, conta=conta)
    conta.transacoes.append(transacao)
    
    logger.info(f"Depósito de R$ {valor:.2f} na conta {conta.numero}")
    exibir_deposito(valor)
```

---

## 🔐 Segurança

### Hash de Senhas

```python
# src/utils/security.py
import bcrypt

def hash_senha(senha: str) -> str:
    """Cria hash seguro da senha"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode(), salt).decode()

def verificar_senha(senha: str, hash_armazenado: str) -> bool:
    """Verifica senha contra hash"""
    return bcrypt.checkpw(senha.encode(), hash_armazenado.encode())
```

### Sistema de Autenticação

```python
# src/auth/auth_service.py
class AuthService:
    def fazer_login(self, username: str, senha: str) -> str:
        """Retorna token de sessão se credenciais válidas"""
        
    def verificar_sessao(self, username: str, token: str) -> bool:
        """Valida se sessão está ativa"""
```

---

## 📊 Logging

Sistema de logging profissional com múltiplos níveis:

```python
# src/utils/logger.py
logger.debug("Informação detalhada para debug")
logger.info("Operação normal")
logger.warning("Alerta de atenção")
logger.error("Erro recuperável")
logger.critical("Erro crítico do sistema")
```

### Saída Colorida no Console

```
2024/01/15 10:30:45 | services.conta | INFO | Depósito de R$ 500.00 na conta 001
2024/01/15 10:31:12 | services.conta | WARNING | Tentativa de saque acima do limite
2024/01/15 10:31:45 | services.conta | ERROR | Saldo insuficiente para operação
```

### Arquivo de Log Rotativo

Logs salvos em `logs/banco.log` com rotação automática (10MB, 3 backups).

---

## 🎓 Conceitos Avançados Demonstrados

### Type Hints Completos

```python
from typing import List, Optional, TYPE_CHECKING

def transferir(origem: 'Conta', destino: 'Conta', valor: float) -> None:
    """Type hints evitam erros e melhoram IDE"""
```

### Validações Pydantic

```python
class ContaCorrente(Conta):
    limite: float
    
    @field_validator('limite')
    @classmethod
    def validar_limite_positivo(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Limite não pode ser negativo")
        return v
```

### Duck Typing Controlado

```python
# Verifica capacidade sem herança forçada
if hasattr(conta, 'get_rendimento'):
    rendimento = conta.get_rendimento()
```

### Context Managers (Futuro)

```python
# Potencial uso futuro
with SessionManager() as session:
    session.executar_transacao(...)
```

---

## 📖 Para Estudar

### Ordem Recomendada

1. **Comece pelo básico**: Leia [banco2.py](banco2.py) para entender o problema
2. **Entenda os modelos**: Estude [src/models/](src/models/)
3. **Veja as interfaces**: Analise [src/interfaces/](src/interfaces/)
4. **Aprenda os serviços**: Leia [src/services/](src/services/)
5. **Execute os testes**: Rode e leia [tests/](tests/)
6. **Compare versões**: Veja as diferenças entre v1 e v2

### Exercícios Sugeridos

1. ✏️ Adicione um novo tipo de conta (Conta Investimento)
2. ✏️ Crie um sistema de notificações por email
3. ✏️ Implemente um histórico de login
4. ✏️ Adicione um sistema de limites diários
5. ✏️ Crie relatórios em PDF

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é de código aberto para fins educacionais.

---

## 👨‍💻 Autor

Desenvolvido para estudo de **Programação Orientada a Objetos** no IFMS.

---

## 📞 Suporte

Dúvidas? Entre em contato ou abra uma issue no repositório.

---

## 🔗 Links Úteis

- [Documentação Python](https://docs.python.org/3/)
- [Documentação Pydantic](https://docs.pydantic.dev/)
- [Documentação pytest](https://docs.pytest.org/)
- [PEP 8 - Style Guide](https://pep8.org/)
- [Type Hints PEP 484](https://www.python.org/dev/peps/pep-0484/)

---

**⭐ Se este projeto te ajudou, considere dar uma estrela no repositório!**