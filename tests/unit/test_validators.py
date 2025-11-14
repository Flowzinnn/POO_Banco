"""Testes unitários para validadores."""

import pytest
from src.utils.validators import validar_cpf, validar_cnpj, validar_cep, validar_telefone


class TestValidadorCPF:
    """Testes para validação de CPF."""
    
    def test_cpf_valido(self) -> None:
        """Testa CPF válido."""
        assert validar_cpf("123.456.789-09") is True
        assert validar_cpf("12345678909") is True
    
    def test_cpf_invalido_digitos_verificadores(self) -> None:
        """Testa CPF com dígitos verificadores incorretos."""
        assert validar_cpf("123.456.789-00") is False
    
    def test_cpf_invalido_todos_digitos_iguais(self) -> None:
        """Testa CPF com todos os dígitos iguais."""
        assert validar_cpf("111.111.111-11") is False
        assert validar_cpf("000.000.000-00") is False
    
    def test_cpf_invalido_tamanho(self) -> None:
        """Testa CPF com tamanho incorreto."""
        assert validar_cpf("123.456.789") is False
        assert validar_cpf("123") is False


class TestValidadorCNPJ:
    """Testes para validação de CNPJ."""
    
    def test_cnpj_valido(self) -> None:
        """Testa CNPJ válido."""
        assert validar_cnpj("11.222.333/0001-81") is True
        assert validar_cnpj("11222333000181") is True
    
    def test_cnpj_invalido_digitos_verificadores(self) -> None:
        """Testa CNPJ com dígitos verificadores incorretos."""
        assert validar_cnpj("11.222.333/0001-00") is False
    
    def test_cnpj_invalido_todos_digitos_iguais(self) -> None:
        """Testa CNPJ com todos os dígitos iguais."""
        assert validar_cnpj("11.111.111/1111-11") is False
    
    def test_cnpj_invalido_tamanho(self) -> None:
        """Testa CNPJ com tamanho incorreto."""
        assert validar_cnpj("11.222.333/0001") is False


class TestValidadorCEP:
    """Testes para validação de CEP."""
    
    def test_cep_valido(self) -> None:
        """Testa CEP válido."""
        assert validar_cep("79002-000") is True
        assert validar_cep("79002000") is True
    
    def test_cep_invalido_tamanho(self) -> None:
        """Testa CEP com tamanho incorreto."""
        assert validar_cep("790020") is False
        assert validar_cep("790020000") is False


class TestValidadorTelefone:
    """Testes para validação de telefone."""
    
    def test_telefone_valido_celular(self) -> None:
        """Testa telefone celular válido."""
        assert validar_telefone("(67) 99876-5432") is True
        assert validar_telefone("67998765432") is True
    
    def test_telefone_valido_fixo(self) -> None:
        """Testa telefone fixo válido."""
        assert validar_telefone("(67) 3321-4567") is True
        assert validar_telefone("6733214567") is True
    
    def test_telefone_invalido_tamanho(self) -> None:
        """Testa telefone com tamanho incorreto."""
        assert validar_telefone("67999") is False
        assert validar_telefone("679987654321234") is False
