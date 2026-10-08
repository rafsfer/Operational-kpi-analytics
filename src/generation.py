"""Gera um cenário fictício reproduzível, com falhas de qualidade conhecidas."""
import numpy as np
import pandas as pd
from src.config import CATEGORIAS, EQUIPES, INICIO, DATA_CORTE, SEMENTE, SLA_HORAS


def gerar_dados(caminho, quantidade=20000, semente=SEMENTE):
    """Cria tickets de seis meses; acrescenta 120 cópias exatas para a limpeza."""
    if not 10000 <= quantidade <= 30000:
        raise ValueError("A quantidade deve ficar entre 10.000 e 30.000 tickets.")
    rng = np.random.default_rng(semente)
    inicio, corte = pd.Timestamp(INICIO), pd.Timestamp(DATA_CORTE)
    dias = pd.date_range(inicio, corte - pd.Timedelta(days=1), freq="D")
    pesos = np.array([1.0, 1.05, 1.15, 1.18, 1.4, 1.6])[dias.month - 1]
    pesos *= np.where(dias.dayofweek < 5, 1.0, 0.45)
    abertura = dias[rng.choice(len(dias), quantidade, p=pesos / pesos.sum())]
    abertura = abertura + pd.to_timedelta(rng.integers(8*60, 20*60, quantidade), unit="m")
    categoria = rng.choice(list(CATEGORIAS), quantidade, p=[.18, .22, .30, .20, .10])
    equipe = np.array([CATEGORIAS[c][0] for c in categoria])
    prioridade = rng.choice(list(SLA_HORAS), quantidade, p=[.08, .22, .45, .25])
    fator_cat = np.array([{"Cadastro": .6, "Dúvida": .5, "Problema técnico": 1.6,
                           "Cobrança": 1.1, "Cancelamento": 1.3}[c] for c in categoria])
    fator_pri = np.array([{"Crítica": .4, "Alta": .7, "Média": 1., "Baixa": 1.3}[v] for v in prioridade])
    # O aumento da demanda pressiona os tempos nos últimos meses.
    horas = rng.lognormal(3.1, .85, quantidade) * fator_cat * fator_pri
    horas *= 1 + .09 * (abertura.month.to_numpy() - 1)
    fechamento = abertura + pd.to_timedelta(horas, unit="h")
    pendente = (rng.random(quantidade) < .045) | (fechamento >= corte)
    fechamento = pd.Series(fechamento).mask(pendente)
    interacoes = np.maximum(1, rng.poisson(1.2 + fator_cat, quantidade))
    fcr = (~pendente) & (interacoes == 1)
    limites = np.array([SLA_HORAS[v] for v in prioridade])
    sla = (~pendente) & (horas <= limites)
    nota = np.clip(np.rint(4.7 - .85*(~sla) - .18*(interacoes-1)
                          + rng.normal(0, .7, quantidade)), 1, 5).astype(float)
    nota[pendente | (rng.random(quantidade) < .35)] = np.nan
    df = pd.DataFrame({
        "id_atendimento": np.arange(1, quantidade+1),
        "id_cliente": rng.integers(1, 8501, quantidade),
        "data_abertura": abertura, "data_fechamento": fechamento,
        "canal": rng.choice(["Chat", "E-mail", "Telefone", "WhatsApp"], quantidade, p=[.33,.24,.18,.25]),
        "categoria": categoria,
        "subcategoria": [rng.choice(CATEGORIAS[c][1]) for c in categoria],
        "prioridade": prioridade, "equipe": equipe,
        "atendente": [f"{e[:3].upper()}-{rng.integers(1, EQUIPES[e]+1):02d}" for e in equipe],
        "status": np.where(pendente, rng.choice(["Aberto", "Em andamento"], quantidade), "Resolvido"),
        "tempo_primeira_resposta_min": np.round(rng.lognormal(2.8, .8, quantidade), 2),
        "tempo_resolucao_horas": np.where(pendente, np.nan, np.round(horas, 4)),
        "dentro_sla": np.where(pendente, np.nan, sla.astype(float)),
        "resolvido_primeiro_contato": np.where(pendente, np.nan, fcr.astype(float)),
        "nota_satisfacao": nota, "quantidade_interacoes": interacoes,
    })
    # Cada falha ocupa um conjunto separado para facilitar a auditoria.
    ids = rng.permutation(quantidade)
    df.loc[ids[:80], "canal"] = " chat "
    df.loc[ids[80:130], "categoria"] = "problema tecnico"
    df.loc[ids[130:170], "canal"] = None
    df.loc[ids[170:195], "tempo_primeira_resposta_min"] = -10
    df.loc[ids[195:215], "nota_satisfacao"] = 9
    df.loc[ids[215:235], "data_abertura"] = pd.NaT
    df.loc[ids[235:255], "data_fechamento"] = df.loc[ids[235:255], "data_abertura"] - pd.Timedelta(hours=2)
    df.loc[ids[255:270], "quantidade_interacoes"] = -1
    df.loc[ids[270:280], "tempo_primeira_resposta_min"] = 15000
    df = pd.concat([df, df.iloc[ids[280:400]]], ignore_index=True)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, index=False, encoding="utf-8-sig", date_format="%Y-%m-%d %H:%M:%S")
    return df
