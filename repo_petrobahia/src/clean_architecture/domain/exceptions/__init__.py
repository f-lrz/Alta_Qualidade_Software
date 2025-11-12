"""Exceções customizadas do domínio."""


class DomainException(Exception):
    """Exceção base para erros de domínio."""

    pass


class ValidacaoError(DomainException):
    """Erro para falhas na validação de dados."""

    pass


class ProdutoNaoEncontradoError(DomainException):
    """Erro quando um tipo de produto desconhecido é solicitado."""

    pass


class ClienteInvalidoError(DomainException):
    """Erro quando os dados do cliente são inválidos."""

    pass
