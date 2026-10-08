"""Indicadores com denominadores explícitos e percentuais de 0 a 100."""
import pandas as pd


def percentual(numerador, denominador):
    """Retorna nulo quando não existe população elegível."""
    return float(numerador / denominador * 100) if denominador else None


def media(serie):
    """Converte média sem observações para nulo serializável."""
    valor = serie.mean()
    return None if pd.isna(valor) else float(valor)


def calcular_kpis(df):
    """Resume a coorte de aberturas observada até a data de corte."""
    total = len(df)
    fechados = df.loc[df["resolvido"].eq(1)]
    resolvidos = len(fechados)
    return {
        "total_atendimentos": total, "resolvidos": resolvidos,
        "tempo_medio_resolucao_horas": media(fechados["tempo_resolucao_horas"]),
        "sla_percentual": percentual(fechados["dentro_sla"].sum(), total),
        "sla_resolvidos_percentual": percentual(fechados["dentro_sla"].sum(), resolvidos),
        "fcr_percentual": percentual(fechados["resolvido_primeiro_contato"].sum(), resolvidos),
        "fcr_cobertura_percentual": percentual(fechados["resolvido_primeiro_contato"].notna().sum(), resolvidos),
        "backlog": total-resolvidos,
        "csat_media": media(fechados["nota_satisfacao"]),
        "respostas_csat": int(fechados["nota_satisfacao"].notna().sum()),
        "csat_cobertura_percentual": percentual(fechados["nota_satisfacao"].notna().sum(), resolvidos),
        "produtividade_resolvidos": resolvidos,
        "taxa_resolucao_percentual": percentual(resolvidos, total),
    }


def kpis_por_dimensao(df, coluna):
    """Aplica as mesmas regras a cada grupo, sem tirar média de percentuais."""
    return pd.DataFrame([{coluna: grupo, **calcular_kpis(linhas)}
                         for grupo, linhas in df.groupby(coluna, dropna=False)])
