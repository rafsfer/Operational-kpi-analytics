"""Persistência simples dos tickets tratados em SQLite."""
import sqlite3
import pandas as pd
from src.config import EQUIPES, INICIO, DATA_CORTE


def salvar_banco(df, caminho):
    """Cria tabelas e índices; o calendário inclui todo o horizonte observado."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    tickets = df.copy()
    for coluna in ["data_abertura", "data_fechamento"]:
        tickets[coluna] = tickets[coluna].dt.strftime("%Y-%m-%d %H:%M:%S")
    calendario = pd.DataFrame({"data": pd.date_range(INICIO, pd.Timestamp(DATA_CORTE)-pd.Timedelta(days=1)).strftime("%Y-%m-%d")})
    calendario["mes"] = calendario["data"].str[:7]
    equipes = pd.DataFrame({"equipe": list(EQUIPES), "atendentes_planejados": list(EQUIPES.values())})
    with sqlite3.connect(caminho) as conexao:
        tickets.to_sql("atendimentos", conexao, if_exists="replace", index=False)
        equipes.to_sql("equipes", conexao, if_exists="replace", index=False)
        calendario.to_sql("calendario", conexao, if_exists="replace", index=False)
        conexao.execute("CREATE UNIQUE INDEX idx_ticket ON atendimentos(id_atendimento)")
        conexao.execute("CREATE INDEX idx_abertura ON atendimentos(data_abertura)")
        conexao.execute("CREATE INDEX idx_equipe ON atendimentos(equipe)")
    return calendario
