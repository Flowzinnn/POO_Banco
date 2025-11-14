"""
Sistema de logging profissional para o sistema bancário.

Configura logging com múltiplos handlers: console colorido e arquivo rotativo.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

# Tenta importar colorama para console colorido (opcional)
try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    COLORAMA_DISPONIVEL = True
except ImportError:
    COLORAMA_DISPONIVEL = False


class ColoredFormatter(logging.Formatter):
    """Formatter que adiciona cores aos níveis de log no console."""
    
    # Mapeamento de níveis para cores (se colorama estiver disponível)
    CORES = {
        'DEBUG': Fore.CYAN if COLORAMA_DISPONIVEL else '',
        'INFO': Fore.GREEN if COLORAMA_DISPONIVEL else '',
        'WARNING': Fore.YELLOW if COLORAMA_DISPONIVEL else '',
        'ERROR': Fore.RED if COLORAMA_DISPONIVEL else '',
        'CRITICAL': Fore.RED + Style.BRIGHT if COLORAMA_DISPONIVEL else '',
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Formata a mensagem com cores baseadas no nível."""
        cor = self.CORES.get(record.levelname, '')
        reset = Style.RESET_ALL if COLORAMA_DISPONIVEL else ''
        
        # Aplica cor apenas ao nível de log
        record.levelname = f"{cor}{record.levelname}{reset}"
        return super().format(record)


def setup_logger(
    nome: str = "banco",
    nivel_console: str = "INFO",
    nivel_arquivo: str = "DEBUG",
    arquivo_log: Optional[str] = None
) -> logging.Logger:
    """
    Configura e retorna um logger com handlers de console e arquivo.
    
    Args:
        nome: Nome do logger
        nivel_console: Nível de log para o console (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        nivel_arquivo: Nível de log para o arquivo
        arquivo_log: Caminho do arquivo de log (padrão: logs/banco.log)
        
    Returns:
        Logger configurado
    """
    # Cria o logger
    logger = logging.getLogger(nome)
    logger.setLevel(logging.DEBUG)  # Captura tudo, handlers filtram
    
    # Evita duplicação de handlers se já configurado
    if logger.handlers:
        return logger
    
    # Formato das mensagens
    formato = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    formato_data = "%d/%m/%Y %H:%M:%S"
    
    # Handler para console (com cores)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, nivel_console.upper()))
    console_formatter = ColoredFormatter(formato, datefmt=formato_data)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Handler para arquivo rotativo (10MB máximo, 3 backups)
    if arquivo_log is None:
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        arquivo_log = str(logs_dir / "banco.log")
    
    file_handler = RotatingFileHandler(
        arquivo_log,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(getattr(logging, nivel_arquivo.upper()))
    file_formatter = logging.Formatter(formato, datefmt=formato_data)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_logger(nome: str = "banco") -> logging.Logger:
    """
    Retorna um logger configurado (ou cria se não existir).
    
    Args:
        nome: Nome do logger
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(nome)
    
    # Se ainda não tem handlers, configura
    if not logger.handlers:
        return setup_logger(nome)
    
    return logger
