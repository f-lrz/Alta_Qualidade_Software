"""Testes para value objects e exceções do domínio."""

import pytest
from clean_architecture.domain.value_objects import ProdutoTipo, CupomTipo, BASES_PRECO
from clean_architecture.domain.exceptions import (
    DomainException,
    ValidacaoError,
    ProdutoNaoEncontradoError,
    ClienteInvalidoError,
)


class TestValueObjects:
    """Testes para Value Objects."""

    def test_produto_tipo_valores(self):
        """Testa valores dos tipos de produto."""
        assert ProdutoTipo.DIESEL.value == "diesel"
        assert ProdutoTipo.GASOLINA.value == "gasolina"
        assert ProdutoTipo.ETANOL.value == "etanol"
        assert ProdutoTipo.LUBRIFICANTE.value == "lubrificante"

    def test_produto_tipo_criacao_por_valor(self):
        """Testa criação de ProdutoTipo a partir de string."""
        assert ProdutoTipo("diesel") == ProdutoTipo.DIESEL
        assert ProdutoTipo("gasolina") == ProdutoTipo.GASOLINA
        assert ProdutoTipo("etanol") == ProdutoTipo.ETANOL
        assert ProdutoTipo("lubrificante") == ProdutoTipo.LUBRIFICANTE

    def test_produto_tipo_invalido(self):
        """Testa que valor inválido lança exceção."""
        with pytest.raises(ValueError):
            ProdutoTipo("combustivel_invalido")

    def test_cupom_tipo_valores(self):
        """Testa valores dos tipos de cupom."""
        assert CupomTipo.MEGA10.value == "MEGA10"
        assert CupomTipo.NOVO5.value == "NOVO5"
        assert CupomTipo.LUB2.value == "LUB2"

    def test_cupom_tipo_criacao_por_valor(self):
        """Testa criação de CupomTipo a partir de string."""
        assert CupomTipo("MEGA10") == CupomTipo.MEGA10
        assert CupomTipo("NOVO5") == CupomTipo.NOVO5
        assert CupomTipo("LUB2") == CupomTipo.LUB2

    def test_cupom_tipo_invalido(self):
        """Testa que cupom inválido lança exceção."""
        with pytest.raises(ValueError):
            CupomTipo("CUPOM_INVALIDO")

    def test_bases_preco_existem(self):
        """Testa que os preços base estão definidos."""
        assert "diesel" in BASES_PRECO
        assert "gasolina" in BASES_PRECO
        assert "etanol" in BASES_PRECO
        assert "lubrificante" in BASES_PRECO

    def test_bases_preco_valores_positivos(self):
        """Testa que os preços base são positivos."""
        for produto, preco in BASES_PRECO.items():
            assert preco > 0, f"Preço de {produto} deve ser positivo"

    def test_bases_preco_sao_float(self):
        """Testa que os preços base são números."""
        for produto, preco in BASES_PRECO.items():
            assert isinstance(preco, (int, float)), f"Preço de {produto} deve ser numérico"


class TestExceptions:
    """Testes para exceções do domínio."""

    def test_domain_exception_heranca(self):
        """Testa que DomainException é uma Exception."""
        assert issubclass(DomainException, Exception)

    def test_validacao_error_heranca(self):
        """Testa que ValidacaoError herda de DomainException."""
        assert issubclass(ValidacaoError, DomainException)

    def test_produto_nao_encontrado_error_heranca(self):
        """Testa que ProdutoNaoEncontradoError herda de DomainException."""
        assert issubclass(ProdutoNaoEncontradoError, DomainException)

    def test_cliente_invalido_error_heranca(self):
        """Testa que ClienteInvalidoError herda de DomainException."""
        assert issubclass(ClienteInvalidoError, DomainException)

    def test_lancar_validacao_error(self):
        """Testa lançamento de ValidacaoError."""
        with pytest.raises(ValidacaoError) as exc_info:
            raise ValidacaoError("Erro de validação")
        
        assert str(exc_info.value) == "Erro de validação"

    def test_lancar_produto_nao_encontrado_error(self):
        """Testa lançamento de ProdutoNaoEncontradoError."""
        with pytest.raises(ProdutoNaoEncontradoError) as exc_info:
            raise ProdutoNaoEncontradoError("Produto não encontrado")
        
        assert str(exc_info.value) == "Produto não encontrado"

    def test_lancar_cliente_invalido_error(self):
        """Testa lançamento de ClienteInvalidoError."""
        with pytest.raises(ClienteInvalidoError) as exc_info:
            raise ClienteInvalidoError("Cliente inválido")
        
        assert str(exc_info.value) == "Cliente inválido"

    def test_capturar_como_domain_exception(self):
        """Testa que todas as exceções podem ser capturadas como DomainException."""
        exceptions = [
            ValidacaoError("teste"),
            ProdutoNaoEncontradoError("teste"),
            ClienteInvalidoError("teste"),
        ]
        
        for exc in exceptions:
            try:
                raise exc
            except DomainException:
                pass  # Deve capturar todas
            else:
                pytest.fail(f"{type(exc).__name__} não foi capturada como DomainException")
