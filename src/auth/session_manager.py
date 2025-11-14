"""
Gerenciador de sessões do sistema bancário.

Mantém controle das sessões ativas dos usuários.
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
import secrets


class SessionManager:
    """
    Gerencia sessões de usuários autenticados.
    
    Mantém um dicionário de tokens de sessão com tempo de expiração.
    """
    
    def __init__(self, tempo_expiracao_minutos: int = 30) -> None:
        """
        Inicializa o gerenciador de sessões.
        
        Args:
            tempo_expiracao_minutos: Tempo em minutos até a sessão expirar
        """
        self._sessoes: Dict[str, Tuple[str, datetime]] = {}  # {username: (token, expira_em)}
        self._tempo_expiracao = timedelta(minutes=tempo_expiracao_minutos)
    
    def criar_sessao(self, username: str) -> str:
        """
        Cria uma nova sessão para o usuário.
        
        Args:
            username: Nome do usuário
            
        Returns:
            Token único da sessão
        """
        # Gera token seguro aleatório
        token = secrets.token_urlsafe(32)
        expira_em = datetime.now() + self._tempo_expiracao
        
        self._sessoes[username] = (token, expira_em)
        return token
    
    def validar_sessao(self, username: str, token: str) -> bool:
        """
        Valida se a sessão do usuário é válida e não expirou.
        
        Args:
            username: Nome do usuário
            token: Token da sessão
            
        Returns:
            True se a sessão for válida, False caso contrário
        """
        if username not in self._sessoes:
            return False
        
        token_armazenado, expira_em = self._sessoes[username]
        
        # Verifica se o token corresponde e não expirou
        if token != token_armazenado:
            return False
        
        if datetime.now() > expira_em:
            # Sessão expirada, remove
            del self._sessoes[username]
            return False
        
        return True
    
    def renovar_sessao(self, username: str) -> None:
        """
        Renova o tempo de expiração da sessão do usuário.
        
        Args:
            username: Nome do usuário
        """
        if username in self._sessoes:
            token, _ = self._sessoes[username]
            nova_expiracao = datetime.now() + self._tempo_expiracao
            self._sessoes[username] = (token, nova_expiracao)
    
    def encerrar_sessao(self, username: str) -> None:
        """
        Encerra a sessão do usuário (logout).
        
        Args:
            username: Nome do usuário
        """
        if username in self._sessoes:
            del self._sessoes[username]
    
    def limpar_sessoes_expiradas(self) -> int:
        """
        Remove todas as sessões expiradas.
        
        Returns:
            Número de sessões removidas
        """
        agora = datetime.now()
        expiradas = [
            username
            for username, (_, expira_em) in self._sessoes.items()
            if agora > expira_em
        ]
        
        for username in expiradas:
            del self._sessoes[username]
        
        return len(expiradas)
    
    def get_sessao_info(self, username: str) -> Optional[Tuple[str, datetime]]:
        """
        Retorna informações da sessão do usuário.
        
        Args:
            username: Nome do usuário
            
        Returns:
            Tupla (token, expira_em) ou None se não houver sessão
        """
        return self._sessoes.get(username)
