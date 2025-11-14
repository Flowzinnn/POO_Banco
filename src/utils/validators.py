"""
Validadores de documentos e dados brasileiros.

Implementa validação de CPF, CNPJ, CEP e telefone seguindo
as regras oficiais brasileiras.
"""

import re


def validar_cpf(cpf: str) -> bool:
    """
    Valida um CPF brasileiro.
    
    Verifica se o CPF tem 11 dígitos e se os dígitos verificadores
    estão corretos segundo o algoritmo oficial.
    
    Args:
        cpf: String contendo o CPF (pode conter pontos e hífen)
        
    Returns:
        True se o CPF for válido, False caso contrário
    """
    # Remove caracteres não numéricos
    cpf_limpo = re.sub(r'\D', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf_limpo) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if cpf_limpo == cpf_limpo[0] * 11:
        return False
    
    # Calcula o primeiro dígito verificador
    soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Verifica o primeiro dígito
    if int(cpf_limpo[9]) != digito1:
        return False
    
    # Calcula o segundo dígito verificador
    soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    # Verifica o segundo dígito
    return int(cpf_limpo[10]) == digito2


def validar_cnpj(cnpj: str) -> bool:
    """
    Valida um CNPJ brasileiro.
    
    Verifica se o CNPJ tem 14 dígitos e se os dígitos verificadores
    estão corretos segundo o algoritmo oficial.
    
    Args:
        cnpj: String contendo o CNPJ (pode conter pontos, barra e hífen)
        
    Returns:
        True se o CNPJ for válido, False caso contrário
    """
    # Remove caracteres não numéricos
    cnpj_limpo = re.sub(r'\D', '', cnpj)
    
    # Verifica se tem 14 dígitos
    if len(cnpj_limpo) != 14:
        return False
    
    # Verifica se todos os dígitos são iguais (CNPJ inválido)
    if cnpj_limpo == cnpj_limpo[0] * 14:
        return False
    
    # Calcula o primeiro dígito verificador
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_limpo[i]) * pesos1[i] for i in range(12))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Verifica o primeiro dígito
    if int(cnpj_limpo[12]) != digito1:
        return False
    
    # Calcula o segundo dígito verificador
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj_limpo[i]) * pesos2[i] for i in range(13))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    # Verifica o segundo dígito
    return int(cnpj_limpo[13]) == digito2


def validar_cep(cep: str) -> bool:
    """
    Valida um CEP brasileiro.
    
    Verifica se o CEP segue o formato brasileiro (8 dígitos).
    
    Args:
        cep: String contendo o CEP (pode conter hífen)
        
    Returns:
        True se o CEP for válido, False caso contrário
    """
    # Remove caracteres não numéricos
    cep_limpo = re.sub(r'\D', '', cep)
    
    # Verifica se tem 8 dígitos
    return len(cep_limpo) == 8


def validar_telefone(telefone: str) -> bool:
    """
    Valida um telefone brasileiro.
    
    Aceita formatos com DDD e 8 ou 9 dígitos.
    Exemplos: (11) 98765-4321, (11) 3456-7890, 11987654321
    
    Args:
        telefone: String contendo o telefone
        
    Returns:
        True se o telefone for válido, False caso contrário
    """
    # Remove caracteres não numéricos
    tel_limpo = re.sub(r'\D', '', telefone)
    
    # Verifica se tem 10 (fixo) ou 11 (celular) dígitos
    return len(tel_limpo) in [10, 11]
