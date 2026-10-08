"""Verifica tratamento de falhas e reconstrução de estoque em datas conhecidas."""
import unittest
import pandas as pd
from src.cleaning import limpar_dados
from src.analysis import backlog_historico


def ticket(**mudancas):
    """Cria um ticket válido para alterar uma regra de cada vez."""
    base = {"id_atendimento": 1, "id_cliente": 1, "data_abertura": "2026-01-01 10:00:00",
            "data_fechamento": "2026-01-01 18:00:00", "canal": " chat ", "categoria": "Cadastro",
            "subcategoria": "Acesso", "prioridade": "Crítica", "equipe": "Relacionamento",
            "atendente": "REL-01", "status": "Resolvido", "tempo_primeira_resposta_min": 10,
            "tempo_resolucao_horas": 999, "dentro_sla": 0, "resolvido_primeiro_contato": 0,
            "nota_satisfacao": 5, "quantidade_interacoes": 1}
    return {**base, **mudancas}


class TesteTratamento(unittest.TestCase):
    def test_recalcula_sla_no_limite_e_remove_copia(self):
        df, rejeitados, audit = limpar_dados(pd.DataFrame([ticket(), ticket()]))
        self.assertEqual(len(df), 1)
        self.assertEqual(len(rejeitados), 0)
        self.assertEqual(audit["duplicados_removidos"], 1)
        self.assertEqual(df.iloc[0]["canal"], "Chat")
        self.assertEqual(df.iloc[0]["tempo_resolucao_horas"], 8.)
        self.assertEqual(df.iloc[0]["dentro_sla"], 1)
        self.assertEqual(df.iloc[0]["resolvido_primeiro_contato"], 1)

    def test_datas_invertidas_ficam_em_quarentena(self):
        df, rejeitados, _ = limpar_dados(pd.DataFrame([ticket(data_fechamento="2025-12-31 10:00:00")]))
        self.assertTrue(df.empty)
        self.assertIn("fechamento inválido", rejeitados.iloc[0]["motivo_rejeicao"])

    def test_id_conflitante_nao_escolhe_registro_arbitrario(self):
        df, rejeitados, _ = limpar_dados(pd.DataFrame([ticket(), ticket(nota_satisfacao=3)]))
        self.assertTrue(df.empty)
        self.assertEqual(len(rejeitados), 2)

    def test_metricas_invalidas_viram_nulos_sem_perder_ticket(self):
        df, _, _ = limpar_dados(pd.DataFrame([ticket(nota_satisfacao=9, quantidade_interacoes=-1, tempo_primeira_resposta_min=-2)]))
        self.assertEqual(len(df), 1)
        self.assertTrue(pd.isna(df.iloc[0]["nota_satisfacao"]))
        self.assertTrue(pd.isna(df.iloc[0]["resolvido_primeiro_contato"]))

    def test_extremo_e_canal_ausente_sao_preservados(self):
        df, _, _ = limpar_dados(pd.DataFrame([ticket(canal=None, tempo_primeira_resposta_min=15000)]))
        self.assertEqual(df.iloc[0]["canal"], "Não informado")
        self.assertEqual(df.iloc[0]["resposta_extrema"], 1)
        self.assertEqual(df.iloc[0]["tempo_primeira_resposta_min"], 15000)

    def test_backlog_inclui_ticket_fechado_no_mes_seguinte(self):
        df = pd.DataFrame({"data_abertura": pd.to_datetime(["2026-01-01", "2026-02-01", "2026-02-02"]),
                           "data_fechamento": pd.to_datetime(["2026-02-01", None, "2026-02-03"])})
        calendario = pd.DataFrame({"mes": ["2026-01", "2026-02"]})
        resultado = backlog_historico(df, calendario)
        self.assertEqual(resultado["backlog_final"].tolist(), [1, 1])
        self.assertEqual(resultado["resolucoes"].tolist(), [0, 2])


if __name__ == "__main__":
    unittest.main()
