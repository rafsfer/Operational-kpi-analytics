"""Leitura dos arquivos e inspeção inicial dos dados."""
import pandas as pd

COLUNAS = ["id_atendimento", "id_cliente", "data_abertura", "data_fechamento", "canal",
           "categoria", "subcategoria", "prioridade", "equipe", "atendente", "status",
           "tempo_primeira_resposta_min", "tempo_resolucao_horas", "dentro_sla",
           "resolvido_primeiro_contato", "nota_satisfacao", "quantidade_interacoes"]


def carregar_dados(caminho):
    """Confere o esquema antes de iniciar o tratamento."""
    df = pd.read_csv(caminho, encoding="utf-8-sig")
    ausentes = sorted(set(COLUNAS) - set(df.columns))
    if ausentes:
        raise ValueError(f"Colunas obrigatérias ausentes: {ausentes}")
    return df[COLUNAS].copy()


def inspecionar_dados(df):
    """Registra tipos, nulos e duplicidades antes da limpeza."""
    return {"linhas": len(df), "duplicados_exatos": int(df.duplicated().sum()),
            "tipos": df.dtypes.astype(str).to_dict(),
            "nulos": df.isna().sum().astype(int).to_dict()}
