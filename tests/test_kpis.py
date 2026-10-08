"""Pequenas populações conhecidas verificam as regras dos indicadores."""
import unittest
import pandas as pd
from src.kpis import calcular_kpis, kpis_por_dimensao


def exemplo():
    """Quatro tickets: três resolvidos, um pendente e duas notas válidas."""
    return pd.DataFrame({
        "resolvido": [1, 1, 1, 0], "dentro_sla": [1, 1, 0, None],
        "resolvido_primeiro_contato": [1, 0, 1, None],
        "tempo_resolucao_horas": [2., 4., 9., None],
        "nota_satisfacao": [5., 3., None, None], "equipe": ["A", "A", "B", "B"],
    })


class TesteKPIs(unittest.TestCase):
    """Os resultados esperados são calculados manualmente."""
    def setUp(self):
        self.df = exemplo()
        self.kpis = calcular_kpis(self.df)

    def test_sla_usa_total_inclusive_pendentes(self):
        self.assertEqual(self.kpis["sla_percentual"], 50.)
        self.assertAlmostEqual(self.kpis["sla_resolvidos_percentual"], 200/3)

    def test_fcr_usa_apenas_resolvidos(self):
        self.assertAlmostEqual(self.kpis["fcr_percentual"], 200/3)

    def test_csat_exclui_ausentes(self):
        self.assertEqual(self.kpis["csat_media"], 4.)
        self.assertEqual(self.kpis["respostas_csat"], 2)

    def test_backlog(self):
        self.assertEqual(self.kpis["backlog"], 1)

    def test_taxa_resolucao(self):
        self.assertEqual(self.kpis["taxa_resolucao_percentual"], 75.)

    def test_tempo_medio(self):
        self.assertEqual(self.kpis["tempo_medio_resolucao_horas"], 5.)

    def test_populacao_vazia(self):
        resultado = calcular_kpis(self.df.iloc[:0])
        self.assertEqual(resultado["backlog"], 0)
        for nome in ["sla_percentual", "fcr_percentual", "csat_media", "taxa_resolucao_percentual"]:
            self.assertIsNone(resultado[nome])

    def test_apenas_pendentes(self):
        resultado = calcular_kpis(self.df.iloc[3:])
        self.assertEqual(resultado["sla_percentual"], 0.)
        self.assertIsNone(resultado["fcr_percentual"])
        self.assertIsNone(resultado["csat_media"])

    def test_fcr_ausente_tem_cobertura_explicita(self):
        self.df.loc[0, "resolvido_primeiro_contato"] = None
        resultado = calcular_kpis(self.df)
        self.assertAlmostEqual(resultado["fcr_percentual"], 100/3)
        self.assertAlmostEqual(resultado["fcr_cobertura_percentual"], 200/3)

    def test_csat_ignora_nota_de_pendente(self):
        self.df.loc[3, "nota_satisfacao"] = 1.
        self.assertEqual(calcular_kpis(self.df)["csat_media"], 4.)

    def test_agrupamento_conserva_volume(self):
        grupos = kpis_por_dimensao(self.df, "equipe")
        self.assertEqual(grupos["total_atendimentos"].sum(), len(self.df))


if __name__ == "__main__":
    unittest.main()
