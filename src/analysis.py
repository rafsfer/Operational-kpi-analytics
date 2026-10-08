"""Exportações, consultas SQL e insights derivados dos resultados."""
import json
import sqlite3
import pandas as pd
from src.kpis import kpis_por_dimensao
from src.config import DATA_CORTE


def backlog_historico(df, calendario):
    """Reconstrói o estoque no fim de cada mês, incluindo resoluções futuras."""
    registros = []
    for mes in calendario["mes"].unique():
        inicio = pd.Timestamp(mes + "-01")
        fim = inicio + pd.offsets.MonthBegin(1)
        abertos = int(df["data_abertura"].between(inicio, fim, inclusive="left").sum())
        fechados = int(df["data_fechamento"].between(inicio, fim, inclusive="left").sum())
        anterior = int(((df["data_abertura"] < inicio) & (df["data_fechamento"].isna() | (df["data_fechamento"] >= inicio))).sum())
        estoque = int(((df["data_abertura"] < fim) & (df["data_fechamento"].isna() | (df["data_fechamento"] >= fim))).sum())
        assert estoque == anterior + abertos - fechados
        registros.append({"mes": mes, "backlog_inicial": anterior, "aberturas": abertos,
                          "resolucoes": fechados, "backlog_final": estoque})
    return pd.DataFrame(registros)


def executar_consultas(banco, pasta_sql, saida):
    """Executa cada consulta nomeada e exporta sua tabela para conferência."""
    resultados = {}
    saida.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(banco) as conexao:
        for arquivo in sorted(pasta_sql.glob("*.sql")):
            for bloco in arquivo.read_text(encoding="utf-8").split("-- consulta: ")[1:]:
                nome, consulta = bloco.split("\n", 1)
                tabela = pd.read_sql_query(consulta.strip(), conexao)
                tabela.to_csv(saida / f"{nome.strip()}.csv", index=False, encoding="utf-8-sig")
                resultados[nome.strip()] = tabela
    return resultados


def exportar_analises(df, calendario, pasta):
    """Exporta as seis dimensões e o estoque mensal de tickets."""
    tabelas = {}
    for coluna in ["mes_abertura", "equipe", "atendente", "canal", "categoria", "prioridade"]:
        tabelas[coluna] = kpis_por_dimensao(df, coluna)
        tabelas[coluna].to_csv(pasta / f"kpis_por_{coluna}.csv", index=False, encoding="utf-8-sig")
    historico = backlog_historico(df, calendario)
    historico.to_csv(pasta / "backlog_mensal.csv", index=False, encoding="utf-8-sig")
    return tabelas, historico


def gerar_insights(tabelas, historico):
    """Seleciona destaques observados; evita atribuir causalidade aos dados."""
    equipes, cats, canais, meses = [tabelas[c] for c in ["equipe", "categoria", "canal", "mes_abertura"]]
    melhor = equipes.loc[equipes["sla_percentual"].idxmax()]
    pior = equipes.loc[equipes["backlog"].idxmax()]
    lenta = cats.loc[cats["tempo_medio_resolucao_horas"].idxmax()]
    canal = canais.loc[canais["total_atendimentos"].idxmax()]
    categoria_volume = cats.loc[cats["total_atendimentos"].idxmax()]
    pico = meses.loc[meses["total_atendimentos"].idxmax()]
    fcr = equipes.loc[equipes["fcr_percentual"].idxmax()]
    primeiro, ultimo = meses.iloc[0], meses.iloc[-1]
    linhas = [
        f"{melhor['equipe']} apresenta o maior SLA geral: {melhor['sla_percentual']:.2f}%.",
        f"{pior['equipe']} concentra o maior backlog na data de corte: {int(pior['backlog'])} tickets.",
        f"{lenta['categoria']} tem o maior tempo médio de resolução: {lenta['tempo_medio_resolucao_horas']:.2f} horas.",
        f"{canal['canal']} é o canal com maior demanda: {int(canal['total_atendimentos'])} tickets.",
        f"{categoria_volume['categoria']} concentra o maior volume por categoria: {int(categoria_volume['total_atendimentos'])} tickets.",
        f"O pico de aberturas ocorre em {pico['mes_abertura']}: {int(pico['total_atendimentos'])} tickets.",
        f"{fcr['equipe']} apresenta o maior FCR: {fcr['fcr_percentual']:.2f}%.",
        f"O CSAT da coorte de aberturas passou de {primeiro['csat_media']:.2f} para {ultimo['csat_media']:.2f} (escala 1–5).",
        f"O backlog de fim de mês passou de {int(historico.iloc[0]['backlog_final'])} para {int(historico.iloc[-1]['backlog_final'])} tickets.",
    ]
    for metrica, rotulo in [("sla_percentual", "SLA geral"), ("fcr_percentual", "FCR"), ("taxa_resolucao_percentual", "taxa de resolução")]:
        delta = ultimo[metrica]-primeiro[metrica]
        linhas.append(f"{rotulo}: variação de {delta:+.2f} pontos percentuais entre a primeira e a última coorte mensal.")
    pri = tabelas["prioridade"].sort_values("tempo_medio_resolucao_horas")
    linhas.append("Tempo médio por prioridade: " + "; ".join(f"{r.prioridade}: {r.tempo_medio_resolucao_horas:.2f} h" for r in pri.itertuples()) + ". A associação não demonstra causalidade.")
    prod = equipes.loc[equipes["resolvidos"].idxmax()]
    linhas.append(f"{prod['equipe']} lidera a produção absoluta: {int(prod['resolvidos'])} resoluções. Equipes têm tamanhos e demandas diferentes.")
    return "\n".join("- " + linha for linha in linhas)


def salvar_json(caminho, dados):
    """Grava UTF-8 com nulos explícitos e sem valores NaN fora do padrão JSON."""
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
