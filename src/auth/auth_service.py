"""
Serviço de autenticação do sistema bancário.

Gerencia registro, login, logout e verificação de usuários.
"""

from typing import Dict, Optional
from src.auth.usuario import Usuario
from src.auth.session_manager import SessionManager
from src.utils.security import hash_senha, verificar_senha
from src.exceptions.banco_exceptions import AutenticacaoError


class AuthService:
    """
    Serviço de autenticação centralizado.
    
    Gerencia o ciclo de vida completo da autenticação:
    - Registro de novos usuários
    - Login (autenticação)
    - Logout (encerramento de sessão)
    - Verificação de sessões ativas
    """
    
    def __init__(self) -> None:
        """Inicializa o serviço com gerenciador de sessões e base de usuários."""
        self._usuarios: Dict[str, Usuario] = {}  # {username: Usuario}
        self._session_manager = SessionManager()
    
    def registrar_usuario(
        self,
        username: str,
        senha: str,
        role: str,
        ativo: bool = True
    ) -> Usuario:
        """
        Registra um novo usuário no sistema.
        
        Args:
            username: Nome de usuário único
            senha: Senha em texto plano (será hasheada)
            role: Papel do usuário ("admin", "cliente", "funcionario")
            ativo: Se o usuário está ativo
            
        Returns:
            Objeto Usuario criado
            
        Raises:
            AutenticacaoError: Se o username já existir
        """
        if username in self._usuarios:
            raise AutenticacaoError(f"Usuário '{username}' já existe")
        
        # Cria hash seguro da senha
        senha_hash = hash_senha(senha)
        
        # Cria e armazena o usuário
        usuario = Usuario(
            username=username,
            senha_hash=senha_hash,
            role=role,
            ativo=ativo
        )
        
        self._usuarios[username] = usuario
        return usuario
    
    def fazer_login(self, username: str, senha: str) -> str:
        """
        Autentica um usuário e cria uma sessão.
        
        Args:
            username: Nome do usuário
            senha: Senha em texto plano
            
        Returns:
            Token da sessão criada
            
        Raises:
            AutenticacaoError: Se as credenciais forem inválidas
        """
        # Verifica se o usuário existe
        if username not in self._usuarios:
            raise AutenticacaoError("Usuário ou senha inválidos")
        
        usuario = self._usuarios[username]
        
        # Verifica se o usuário está ativo
        if not usuario.ativo:
            raise AutenticacaoError("Usuário inativo")
        
        # Verifica a senha
        if not verificar_senha(senha, usuario.senha_hash):
            raise AutenticacaoError("Usuário ou senha inválidos")
        
        # Cria a sessão
        token = self._session_manager.criar_sessao(username)
        return token
    
    def logout(self, username: str) -> None:
        """
        Encerra a sessão do usuário.
        
        Args:
            username: Nome do usuário
        """
        self._session_manager.encerrar_sessao(username)
    
    def verificar_sessao(self, username: str, token: str) -> bool:
        """
        Verifica se uma sessão é válida.
        
        Args:
            username: Nome do usuário
            token: Token da sessão
            
        Returns:
            True se a sessão for válida, False caso contrário
        """
        return self._session_manager.validar_sessao(username, token)
    
    def get_usuario(self, username: str) -> Optional[Usuario]:
        """
        Retorna um usuário pelo username.
        
        Args:
            username: Nome do usuário
            
        Returns:
            Objeto Usuario ou None se não existir
        """
        return self._usuarios.get(username)
    
    def renovar_sessao(self, username: str) -> None:
        """
        Renova o tempo de expiração da sessão.
        
        Args:
            username: Nome do usuário
        """
        self._session_manager.renovar_sessao(username)
