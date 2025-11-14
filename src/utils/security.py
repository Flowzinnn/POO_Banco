"""
Utilitários de segurança para hash de senhas.

Utiliza bcrypt para criar e verificar hashes seguros de senhas.
"""

import bcrypt


def hash_senha(senha: str) -> str:
    """
    Gera um hash seguro da senha usando bcrypt.
    
    O bcrypt adiciona automaticamente um salt aleatório e utiliza
    um algoritmo de hashing lento para dificultar ataques de força bruta.
    
    Args:
        senha: Senha em texto plano
        
    Returns:
        Hash da senha em formato string
    """
    # Converte a senha para bytes e gera o hash
    senha_bytes = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(senha_bytes, salt)
    
    # Retorna como string
    return hash_bytes.decode('utf-8')


def verificar_senha(senha: str, hash_armazenado: str) -> bool:
    """
    Verifica se a senha corresponde ao hash armazenado.
    
    Args:
        senha: Senha em texto plano a ser verificada
        hash_armazenado: Hash previamente gerado com hash_senha()
        
    Returns:
        True se a senha corresponder ao hash, False caso contrário
    """
    senha_bytes = senha.encode('utf-8')
    hash_bytes = hash_armazenado.encode('utf-8')
    
    # bcrypt.checkpw compara de forma segura
    return bcrypt.checkpw(senha_bytes, hash_bytes)
