"""
Sistema Bancário Modular - Ponto de entrada principal.

Oferece menu interativo para executar diferentes versões do sistema
e ferramentas de desenvolvimento.
"""

import sys
import subprocess
from pathlib import Path

# Tenta importar colorama para menu colorido
try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    COLORAMA_DISPONIVEL = True
except ImportError:
    COLORAMA_DISPONIVEL = False
    # Define fallbacks vazios se colorama não estiver disponível
    class Fore:
        CYAN = BLUE = GREEN = YELLOW = RED = ""
    class Style:
        BRIGHT = RESET_ALL = ""


def limpar_tela() -> None:
    """Limpa a tela do console."""
    subprocess.run("cls" if sys.platform == "win32" else "clear", shell=True)


def exibir_titulo(titulo: str) -> None:
    """Exibe um título formatado."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 60}")
    print(f"{titulo:^60}")
    print(f"{'=' * 60}{Style.RESET_ALL}\n")


def main_v1() -> None:
    """
    Executa a versão 1 (legado) do sistema bancário.
    
    Importa e executa o código original de banco2.py sem modificações.
    Esta versão usa:
    - Código monolítico
    - Prints diretos
    - Senhas em texto plano
    - Sem validações Pydantic
    """
    print(f"{Fore.YELLOW}Carregando Sistema Bancário v1 (Legado)...{Style.RESET_ALL}\n")
    
    try:
        # Importa e executa o main original
        from banco2 import main as main_original
        main_original()
    except Exception as e:
        print(f"{Fore.RED}Erro ao executar v1: {e}{Style.RESET_ALL}")


def main_v2() -> None:
    """
    Executa a versão 2 (refatorada) do sistema bancário.
    
    Usa a nova arquitetura modular com:
    - Separação em camadas (models, services, views)
    - Logging profissional
    - Autenticação com bcrypt
    - Validações Pydantic
    - Type hints completos
    """
    print(f"{Fore.GREEN}Carregando Sistema Bancário v2 (Refatorado)...{Style.RESET_ALL}\n")
    
    try:
        from datetime import date
        from src.models.endereco import Endereco
        from src.models.cliente import Cliente
        from src.models.conta_corrente import ContaCorrente
        from src.models.conta_poupanca import ContaPoupanca
        from src.models.agencia import Agencia
        from src.models.banco import Banco
        from src.services import conta_service, agencia_service
        from src.views.console_view import exibir_extrato, exibir_lista_contas, exibir_lista_agencias
        from src.utils.security import hash_senha
        from src.utils.logger import setup_logger
        
        # Configura logger
        logger = setup_logger("main_v2")
        logger.info("Sistema Bancário v2 iniciado")
        
        # Cria estrutura bancária
        endereco_banco = Endereco(
            cep="79002-000",
            numero="123",
            rua="Av. Afonso Pena",
            bairro="Centro",
            cidade="Campo Grande",
            estado="MS"
        )
        
        endereco_agencia = Endereco(
            cep="79002-100",
            numero="456",
            rua="Rua 14 de Julho",
            bairro="Centro",
            cidade="Campo Grande",
            estado="MS"
        )
        
        # Cria cliente
        cliente_nicolas = Cliente(
            nome="Nicolas",
            cpf="123.456.789-09",
            data_nascimento=date(2003, 5, 10),
            cnh="123456789"
        )
        
        # Cria contas com senhas hasheadas
        conta_corrente = ContaCorrente(
            numero="001",
            cliente=cliente_nicolas,
            saldo=1000.0,
            senha_hash=hash_senha("1234"),
            limite=1000.0
        )
        
        conta_poupanca = ContaPoupanca(
            numero="002",
            cliente=cliente_nicolas,
            saldo=15000.0,
            senha_hash=hash_senha("2508"),
            taxa_rendimento=0.5,
            data_aniversario=15
        )
        
        # Realiza operações usando services
        conta_service.realizar_deposito(conta_corrente, 500.0)
        conta_service.realizar_saque(conta_corrente, 150.0)
        
        # Exibe extrato
        exibir_extrato(conta_corrente)
        
        # Exibe lista de contas do cliente
        exibir_lista_contas(cliente_nicolas.nome, cliente_nicolas.contas)
        
        # Cria agência e banco
        agencia_sul = Agencia(
            nome="Agência Sul",
            numero="001",
            endereco=endereco_agencia,
            fone="(67) 3321-4567"
        )
        
        banco_wolf = Banco(
            nome="Banco Wolf",
            cnpj="11.222.333/0001-81",
            endereco=endereco_banco,
            fone="(67) 3321-0000"
        )
        
        banco_wolf.adicionar_agencia(agencia_sul)
        
        # Adiciona contas à agência
        agencia_service.adicionar_conta_na_agencia(conta_corrente, agencia_sul)
        agencia_service.adicionar_conta_na_agencia(conta_poupanca, agencia_sul)
        
        print(f"\n{banco_wolf}\n")
        exibir_lista_agencias(banco_wolf.nome, banco_wolf.agencias)
        
        logger.info("Sistema Bancário v2 finalizado com sucesso")
        
    except Exception as e:
        print(f"{Fore.RED}Erro ao executar v2: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()


def menu_desenvolvedor() -> None:
    """Menu com ferramentas de desenvolvimento."""
    while True:
        limpar_tela()
        exibir_titulo("MENU DESENVOLVEDOR")
        
        print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Rodar Testes Unitários")
        print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Rodar Testes de Integração")
        print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Rodar Todos os Testes")
        print(f"{Fore.CYAN}[4]{Style.RESET_ALL} Validar Tipos com mypy")
        print(f"{Fore.CYAN}[5]{Style.RESET_ALL} Ver Últimas 50 Linhas do Log")
        print(f"{Fore.CYAN}[6]{Style.RESET_ALL} Limpar Arquivos de Log")
        print(f"{Fore.CYAN}[7]{Style.RESET_ALL} Cobertura de Testes")
        print(f"{Fore.CYAN}[0]{Style.RESET_ALL} Voltar ao Menu Principal")
        
        opcao = input(f"\n{Fore.YELLOW}Escolha uma opção: {Style.RESET_ALL}")
        
        if opcao == "1":
            print(f"\n{Fore.GREEN}Executando testes unitários...{Style.RESET_ALL}\n")
            subprocess.run(["pytest", "tests/unit", "-v"])
            input(f"\n{Fore.YELLOW}Pressione Enter para continuar...{Style.RESET_ALL}")
        
        elif opcao == "2":
            print(f"\n{Fore.GREEN}Executando testes de integração...{Style.RESET_ALL}\n")
            subprocess.run(["pytest", "tests/integration", "-v"])
            input(f"\n{Fore.YELLOW}Pressione Enter para continuar...{Style.RESET_ALL}")
        
        elif opcao == "3":
            print(f"\n{Fore.GREEN}Executando todos os testes...{Style.RESET_ALL}\n")
            subprocess.run(["pytest", "-v"])
            input(f"\n{Fore.YELLOW}Pressione Enter para continuar...{Style.RESET_ALL}")
        
        elif opcao == "4":
            print(f"\n{Fore.GREEN}Validando tipos com mypy...{Style.RESET_ALL}\n")
            subprocess.run(["mypy", "src/"])
            input(f"\n{Fore.YELLOW}Pressione Enter para continuar...{Style.RESET_ALL}")
        
        elif opcao == "5":
            log_file = Path("logs/banco.log")
            if log_file.exists():
                print(f"\n{Fore.GREEN}Últimas 50 linhas do log:{Style.RESET_ALL}\n")
                with open(log_file, "r", encoding="utf-8") as f:
                    linhas = f.readlines()
                    for linha in linhas[-50:]:
                        print(linha.rstrip())
            else:
                print(f"{Fore.YELLOW}Arquivo de log não encontrado.{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Pressione Enter para continuar...{Style.RESET_ALL}")
        
        elif opcao == "6":
            log_dir = Path("logs")
            if log_dir.exists():
                for log_file in log_dir.glob("*.log*"):
                    log_file.unlink()
                print(f"{Fore.GREEN}Arquivos de log limpos com sucesso!{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Diretório de logs não encontrado.{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Pressione Enter para continuar...{Style.RESET_ALL}")
        
        elif opcao == "7":
            print(f"\n{Fore.GREEN}Executando testes com cobertura...{Style.RESET_ALL}\n")
            subprocess.run(["pytest", "--cov=src", "--cov-report=term-missing"])
            input(f"\n{Fore.YELLOW}Pressione Enter para continuar...{Style.RESET_ALL}")
        
        elif opcao == "0":
            break
        
        else:
            print(f"{Fore.RED}Opção inválida!{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Pressione Enter para continuar...{Style.RESET_ALL}")


def menu_principal() -> None:
    """Menu principal do sistema."""
    while True:
        limpar_tela()
        exibir_titulo("SISTEMA BANCÁRIO MODULAR")
        
        print(f"{Fore.BLUE}{Style.BRIGHT}Selecione uma opção:{Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}[1]{Style.RESET_ALL} Rodar Sistema v1 (Legado)")
        print(f"{Fore.GREEN}[2]{Style.RESET_ALL} Rodar Sistema v2 (Refatorado)")
        print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Menu Desenvolvedor")
        print(f"{Fore.RED}[0]{Style.RESET_ALL} Sair")
        
        opcao = input(f"\n{Fore.YELLOW}Escolha uma opção: {Style.RESET_ALL}")
        
        if opcao == "1":
            limpar_tela()
            exibir_titulo("SISTEMA BANCÁRIO V1 - LEGADO")
            main_v1()
            input(f"\n{Fore.YELLOW}Pressione Enter para continuar...{Style.RESET_ALL}")
        
        elif opcao == "2":
            limpar_tela()
            exibir_titulo("SISTEMA BANCÁRIO V2 - REFATORADO")
            main_v2()
            input(f"\n{Fore.YELLOW}Pressione Enter para continuar...{Style.RESET_ALL}")
        
        elif opcao == "3":
            menu_desenvolvedor()
        
        elif opcao == "0":
            print(f"\n{Fore.GREEN}Encerrando sistema. Até logo!{Style.RESET_ALL}\n")
            sys.exit(0)
        
        else:
            print(f"{Fore.RED}Opção inválida!{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Pressione Enter para continuar...{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Sistema interrompido pelo usuário.{Style.RESET_ALL}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Erro fatal: {e}{Style.RESET_ALL}\n")
        sys.exit(1)
