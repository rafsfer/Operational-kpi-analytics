"""Executa o projeto completo de forma reproduzível."""
import argparse
import logging
import math
import sys
import pandas as pd
from src.config import RAIZ, DATA_CORTE, SEMENTE
from src.generation import gerar_dados
from src.ingestion import carregar_dados, inspecionar_dados
from src.cleaning import limpar_dados
from src.kpis import calcular_kpis
from src.database import salvar_banco
from src.analysis import exportar_analises, executar_consultas, gerar_insights, salvar_json


def executar(quantidade=20000, semente=SEMENTE):
    """Gera dados, audita a limpeza, calcula indicadores e valida SQL."""
    raw, saida = RAIZ / "data/raw", RAIZ / "data/processed"
    for pasta in [raw, saida, RAIZ / "reports", RAIZ / "database"]:
        pasta.mkdir(parents=True, exist_ok=True)
    logging.info("Gerando %s tickets sintéticos com semente %s", quantidade, semente)
    gerar_dados(raw / "atendimentos.csv", quantidade, semente)
    bruto = carregar_dados(raw / "atendimentos.csv")
    df, rejeitados, auditoria = limpar_dados(bruto)
    auditoria["inspecao_inicial"] = inspecionar_dados(bruto)
    auditoria["semente"] = semente
    auditoria["data_corte_exclusiva"] = DATA_CORTE
    salvar_json(saida / "qualidade.json", auditoria)
    df.to_csv(saida / "atendimentos.csv", index=False, encoding="utf-8-sig", date_format="%Y-%m-%d %H:%M:%S")
    rejeitados.to_csv(saida / "rejeitados.csv", index=False, encoding="utf-8-sig")
    kpis = calcular_kpis(df)
    salvar_json(saida / "kpis_gerais.json", kpis)
    banco = RAIZ / "database/operational_kpis.db"
    calendario = salvar_banco(df, banco)
    calendario.to_csv(saida / "calendario.csv", index=False, encoding="utf-8-sig")
    tabelas, historico = exportar_analises(df, calendario, saida)
    resultados = executar_consultas(banco, RAIZ / "sql", saida / "sql")
    # Confere cada indicador comum às implementações Python e SQL.
    geral_sql = resultados["kpis_gerais"].iloc[0]
    for nome in geral_sql.index:
        esperado, obtido = kpis[nome], geral_sql[nome]
        if esperado is None:
            assert pd.isna(obtido), nome
        else:
            assert math.isclose(float(esperado), float(obtido), abs_tol=.00001), nome
    for dimensao, tabela in tabelas.items():
        python_ordenado = tabela.sort_values(dimensao).reset_index(drop=True)
        sql_ordenado = resultados[f"kpis_por_{dimensao}"].sort_values(dimensao).reset_index(drop=True)
        pd.testing.assert_frame_equal(python_ordenado, sql_ordenado, check_dtype=False, atol=.00001)
    pd.testing.assert_frame_equal(historico, resultados["backlog_historico"], check_dtype=False)
    insights = gerar_insights(tabelas, historico)
    (RAIZ / "reports/insights.md").write_text("# Insights observados\n\n" + insights + "\n", encoding="utf-8")
    readme = RAIZ / "README.md"
    texto = readme.read_text(encoding="utf-8")
    inicio, fim = "<!-- INICIO_INSIGHTS -->", "<!-- FIM_INSIGHTS -->"
    antes, resto = texto.split(inicio, 1)
    _, depois = resto.split(fim, 1)
    readme.write_text(antes + inicio + "\n\n" + insights + "\n\n" + fim + depois, encoding="utf-8")
    logging.info("Tratamento: %s tickets válidos; %s rejeitados; %s duplicados removidos", len(df), len(rejeitados), auditoria["duplicados_removidos"])
    logging.info("KPIs gerais, seis dimensões e backlog histórico conferem entre Python e SQL")
    print(pd.Series(kpis).to_string())
    return kpis


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Análise de performance operacional com dados sintéticos")
    parser.add_argument("--quantidade", type=int, default=20000)
    parser.add_argument("--semente", type=int, default=SEMENTE)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        executar(args.quantidade, args.semente)
    except (OSError, ValueError, AssertionError) as erro:
        logging.exception("Não foi possível concluir a análise: %s", erro)
        sys.exit(1)
