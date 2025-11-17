"""Testes para serviços da camada de infraestrutura."""

import pytest
from clean_architecture.infrastructure.services import (
    CalculoPrecoService,
    DescontoService,
    ArredondamentoService,
)
from clean_architecture.domain.value_objects import ProdutoTipo, CupomTipo
from clean_architecture.domain.exceptions import ProdutoNaoEncontradoError


class TestCalculoPrecoService:
    """Testes para o serviço de cálculo de preço."""

    def setup_method(self):
        """Setup executado antes de cada teste."""
        self.service = CalculoPrecoService()

    def test_calcular_diesel_sem_desconto(self):
        """Testa cálculo de diesel sem atingir desconto por volume."""
        preco = self.service.calcular(ProdutoTipo.DIESEL, 100)
        assert preco == pytest.approx(399.0, rel=0.01)

    def test_calcular_diesel_desconto_5_porcento(self):
        """Testa cálculo de diesel com desconto de 5% (>500 unidades)."""
        preco = self.service.calcular(ProdutoTipo.DIESEL, 600)
        # 3.99 * 600 = 2394.0
        # 2394.0 * 0.95 = 2274.3
        assert preco == pytest.approx(2274.3, rel=0.01)

    def test_calcular_diesel_desconto_10_porcento(self):
        """Testa cálculo de diesel com desconto de 10% (>1000 unidades)."""
        preco = self.service.calcular(ProdutoTipo.DIESEL, 1200)
        # 3.99 * 1200 = 4788.0
        # 4788.0 * 0.90 = 4309.2
        assert preco == pytest.approx(4309.2, rel=0.01)

    def test_calcular_gasolina_sem_desconto(self):
        """Testa cálculo de gasolina sem desconto."""
        preco = self.service.calcular(ProdutoTipo.GASOLINA, 100)
        # 5.19 * 100 = 519.0
        assert preco == pytest.approx(519.0, rel=0.01)

    def test_calcular_gasolina_com_desconto(self):
        """Testa cálculo de gasolina com desconto (>200 unidades)."""
        preco = self.service.calcular(ProdutoTipo.GASOLINA, 300)
        # 5.19 * 300 = 1557.0
        # 1557.0 - 100 = 1457.0
        assert preco == pytest.approx(1457.0, rel=0.01)

    def test_calcular_etanol_sem_desconto(self):
        """Testa cálculo de etanol sem desconto."""
        preco = self.service.calcular(ProdutoTipo.ETANOL, 50)
        # 3.59 * 50 = 179.5
        assert preco == pytest.approx(179.5, rel=0.01)

    def test_calcular_etanol_com_desconto(self):
        """Testa cálculo de etanol com desconto de 3% (>80 unidades)."""
        preco = self.service.calcular(ProdutoTipo.ETANOL, 100)
        # 3.59 * 100 = 359.0
        # 359.0 * 0.97 = 348.23
        assert preco == pytest.approx(348.23, rel=0.01)

    def test_calcular_lubrificante(self):
        """Testa cálculo de lubrificante."""
        preco = self.service.calcular(ProdutoTipo.LUBRIFICANTE, 12)
        # 25.0 * 12 = 300.0
        assert preco == pytest.approx(300.0, rel=0.01)


class TestDescontoService:
    """Testes para o serviço de desconto."""

    def setup_method(self):
        """Setup executado antes de cada teste."""
        self.service = DescontoService()

    def test_sem_cupom(self):
        """Testa que sem cupom não há desconto adicional."""
        preco_original = 1000.0
        preco_com_desconto = self.service.aplicar_desconto(
            preco=preco_original,
            produto=ProdutoTipo.DIESEL,
            quantidade=100,
            cupom=None,
        )
        assert preco_com_desconto == preco_original

    def test_cupom_mega10(self):
        """Testa cupom MEGA10 (10% de desconto)."""
        preco_original = 1000.0
        preco_com_desconto = self.service.aplicar_desconto(
            preco=preco_original,
            produto=ProdutoTipo.DIESEL,
            quantidade=100,
            cupom=CupomTipo.MEGA10,
        )
        # 1000.0 * 0.90 = 900.0
        assert preco_com_desconto == pytest.approx(900.0, rel=0.01)

    def test_cupom_novo5(self):
        """Testa cupom NOVO5 (5% de desconto)."""
        preco_original = 1000.0
        preco_com_desconto = self.service.aplicar_desconto(
            preco=preco_original,
            produto=ProdutoTipo.DIESEL,
            quantidade=100,
            cupom=CupomTipo.NOVO5,
        )
        # 1000.0 * 0.95 = 950.0
        assert preco_com_desconto == pytest.approx(950.0, rel=0.01)

    def test_cupom_lub2_com_lubrificante(self):
        """Testa cupom LUB2 com produto lubrificante."""
        preco_original = 300.0
        preco_com_desconto = self.service.aplicar_desconto(
            preco=preco_original,
            produto=ProdutoTipo.LUBRIFICANTE,
            quantidade=12,
            cupom=CupomTipo.LUB2,
        )
        # 300.0 - 2.0 = 298.0
        assert preco_com_desconto == pytest.approx(298.0, rel=0.01)

    def test_cupom_lub2_com_outro_produto(self):
        """Testa que cupom LUB2 não funciona com outros produtos."""
        preco_original = 1000.0
        preco_com_desconto = self.service.aplicar_desconto(
            preco=preco_original,
            produto=ProdutoTipo.DIESEL,
            quantidade=100,
            cupom=CupomTipo.LUB2,
        )
        # Não deve aplicar desconto
        assert preco_com_desconto == preco_original

    def test_descontos_diferentes_produtos(self):
        """Testa descontos em diferentes produtos."""
        produtos = [
            ProdutoTipo.DIESEL,
            ProdutoTipo.GASOLINA,
            ProdutoTipo.ETANOL,
            ProdutoTipo.LUBRIFICANTE,
        ]
        
        for produto in produtos:
            preco = self.service.aplicar_desconto(
                preco=1000.0,
                produto=produto,
                quantidade=100,
                cupom=CupomTipo.MEGA10,
            )
            # Todos devem ter desconto de 10%
            assert preco == pytest.approx(900.0, rel=0.01)


class TestArredondamentoService:
    """Testes para o serviço de arredondamento."""

    def setup_method(self):
        """Setup executado antes de cada teste."""
        self.service = ArredondamentoService()

    def test_arredondar_diesel_sem_decimais(self):
        """Testa que diesel não tem casas decimais."""
        preco = self.service.arredondar(1234.56, ProdutoTipo.DIESEL)
        assert preco == 1235.0
        assert preco == int(preco)

    def test_arredondar_diesel_arredonda_para_cima(self):
        """Testa arredondamento para cima no diesel."""
        # Python usa banker's rounding (arredonda para o número par mais próximo)
        # 1234.5 arredonda para 1234.0 (par)
        # 1235.5 arredonda para 1236.0 (par)
        preco = self.service.arredondar(1235.6, ProdutoTipo.DIESEL)
        assert preco == 1236.0

    def test_arredondar_diesel_arredonda_para_baixo(self):
        """Testa arredondamento para baixo no diesel."""
        preco = self.service.arredondar(1234.4, ProdutoTipo.DIESEL)
        assert preco == 1234.0

    def test_arredondar_gasolina_duas_casas(self):
        """Testa que gasolina tem 2 casas decimais."""
        preco = self.service.arredondar(1234.56789, ProdutoTipo.GASOLINA)
        assert preco == pytest.approx(1234.57, rel=0.001)

    def test_arredondar_gasolina_exato(self):
        """Testa gasolina com valor exato em 2 casas."""
        preco = self.service.arredondar(1234.56, ProdutoTipo.GASOLINA)
        assert preco == pytest.approx(1234.56, rel=0.001)

    def test_arredondar_etanol_trunca(self):
        """Testa que etanol trunca em 2 casas."""
        preco = self.service.arredondar(1234.5678, ProdutoTipo.ETANOL)
        # Trunca: 1234.56
        assert preco == pytest.approx(1234.56, rel=0.001)

    def test_arredondar_lubrificante_trunca(self):
        """Testa que lubrificante trunca em 2 casas."""
        preco = self.service.arredondar(298.999, ProdutoTipo.LUBRIFICANTE)
        # Trunca: 298.99
        assert preco == pytest.approx(298.99, rel=0.001)

    def test_arredondamento_diferentes_produtos(self):
        """Testa arredondamento de todos os produtos."""
        valor = 1234.5678
        
        # Diesel: sem decimais
        diesel = self.service.arredondar(valor, ProdutoTipo.DIESEL)
        assert diesel == 1235.0
        
        # Gasolina: 2 casas
        gasolina = self.service.arredondar(valor, ProdutoTipo.GASOLINA)
        assert gasolina == pytest.approx(1234.57, rel=0.001)
        
        # Etanol: trunca em 2 casas
        etanol = self.service.arredondar(valor, ProdutoTipo.ETANOL)
        assert etanol == pytest.approx(1234.56, rel=0.001)
        
        # Lubrificante: trunca em 2 casas
        lubrificante = self.service.arredondar(valor, ProdutoTipo.LUBRIFICANTE)
        assert lubrificante == pytest.approx(1234.56, rel=0.001)
