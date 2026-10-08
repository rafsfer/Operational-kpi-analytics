"""Padronização, validação e cálculo dos campos derivados."""
import unicodedata
import pandas as pd
from src.config import DATA_CORTE, INICIO, SLA_HORAS, EQUIPES, CATEGORIAS


def normalizar(valor):
    """Remove espaços e acentos apenas para comparar categorias."""
    if pd.isna(valor):
        return ""
    texto = unicodedata.normalize("NFKD", str(valor).strip().lower())
    return "".join(c for c in texto if not unicodedata.combining(c))


def limpar_dados(dados):
    """Quarentena para falhas críticas; nulos para métricas opcionais inválidas."""
    df = dados.drop_duplicates().copy()
    duplicados = len(dados) - len(df)
    originais = df.copy()
    for coluna in ["data_abertura", "data_fechamento"]:
        df[coluna] = pd.to_datetime(df[coluna], errors="coerce")
    for coluna in ["id_atendimento", "id_cliente", "tempo_primeira_resposta_min", "quantidade_interacoes", "nota_satisfacao"]:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    dominios = {"canal": ["Chat", "E-mail", "Telefone", "WhatsApp"],
                "categoria": list(CATEGORIAS), "prioridade": list(SLA_HORAS),
                "equipe": list(EQUIPES), "status": ["Resolvido", "Aberto", "Em andamento"]}
    padronizacoes = {}
    for coluna, valores in dominios.items():
        mapa = {normalizar(v): v for v in valores}
        novo = df[coluna].map(normalizar).map(mapa)
        padronizacoes[coluna] = int((novo.fillna("") != df[coluna].fillna("")).sum())
        df[coluna] = novo
    df["canal"] = df["canal"].fillna("Não informado")
    motivo = pd.Series("", index=df.index)

    def marcar(mascara, texto):
        motivo.loc[mascara.fillna(True)] += texto + "; "

    for coluna in ["id_atendimento", "id_cliente"]:
        marcar(df[coluna].isna() | (df[coluna] <= 0) | (df[coluna] % 1 != 0), f"{coluna} inválido")
    marcar(df["id_atendimento"].duplicated(keep=False), "ID com registros conflitantes")
    marcar(df["data_abertura"].isna() | (df["data_abertura"] < pd.Timestamp(INICIO)) |
           (df["data_abertura"] >= pd.Timestamp(DATA_CORTE)), "abertura inválida")
    for coluna in ["categoria", "prioridade", "equipe", "status"]:
        marcar(df[coluna].isna(), f"{coluna} inválida")
    marcar(df["atendente"].isna(), "atendente ausente")
    equipe_esperada = df["categoria"].map({c: v[0] for c, v in CATEGORIAS.items()})
    marcar(df["equipe"] != equipe_esperada, "equipe incompatível com categoria")
    subcategoria_valida = pd.Series([c in CATEGORIAS and s in CATEGORIAS[c][1]
                                    for c, s in zip(df["categoria"], df["subcategoria"])], index=df.index)
    marcar(~subcategoria_valida, "subcategoria inválida")
    fechado = df["status"].eq("Resolvido")
    marcar(fechado & df["data_fechamento"].isna(), "resolvido sem fechamento")
    marcar(~fechado & df["data_fechamento"].notna(), "pendente com fechamento")
    marcar((df["data_fechamento"] < df["data_abertura"]) |
           (df["data_fechamento"] >= pd.Timestamp(DATA_CORTE)), "fechamento inválido")
    invalidos = motivo.ne("")
    rejeitados = originais.loc[invalidos].copy()
    rejeitados["motivo_rejeicao"] = motivo.loc[invalidos].str.rstrip("; ")
    df = df.loc[~invalidos].copy()
    correcoes = {}
    for coluna, mascara in {
        "tempo_primeira_resposta_min": df["tempo_primeira_resposta_min"] < 0,
        "nota_satisfacao": ~df["nota_satisfacao"].between(1, 5),
        "quantidade_interacoes": (df["quantidade_interacoes"] < 1) | (df["quantidade_interacoes"] % 1 != 0),
    }.items():
        correcoes[coluna] = int((mascara & df[coluna].notna()).sum())
        df.loc[mascara, coluna] = float("nan")
    df.loc[df["status"] != "Resolvido", "nota_satisfacao"] = float("nan")
    for coluna in ["id_atendimento", "id_cliente", "quantidade_interacoes"]:
        df[coluna] = df[coluna].astype("Int64")
    df["resolvido"] = df["status"].eq("Resolvido").astype(int)
    df["tempo_resolucao_horas"] = (df["data_fechamento"]-df["data_abertura"]).dt.total_seconds()/3600
    df["sla_horas"] = df["prioridade"].map(SLA_HORAS)
    # Tickets pendentes ficam sem resultado de SLA/FCR até a resolução.
    df["dentro_sla"] = (df["tempo_resolucao_horas"] <= df["sla_horas"]).astype("Int64").where(df["resolvido"].eq(1))
    df["resolvido_primeiro_contato"] = df["quantidade_interacoes"].eq(1).astype("Int64").where(df["resolvido"].eq(1))
    df["mes_abertura"] = df["data_abertura"].dt.strftime("%Y-%m")
    df["mes_fechamento"] = df["data_fechamento"].dt.strftime("%Y-%m")
    df["idade_horas"] = (pd.Timestamp(DATA_CORTE)-df["data_abertura"]).dt.total_seconds()/3600
    df["pendente_vencido"] = (df["resolvido"].eq(0) & (df["idade_horas"] > df["sla_horas"])).astype(int)
    # Extremos plausíveis permanecem disponíveis para análise, sem cortar a média.
    df["resposta_extrema"] = (df["tempo_primeira_resposta_min"] > 1440).astype(int)
    auditoria = {"linhas_recebidas": len(dados), "duplicados_removidos": duplicados,
                 "linhas_rejeitadas": len(rejeitados), "linhas_tratadas": len(df),
                 "categorias_padronizadas": padronizacoes, "valores_invalidos_anulados": correcoes,
                 "respostas_extremas_preservadas": int(df["resposta_extrema"].sum()),
                 "nulos_apos_tratamento": df.isna().sum().astype(int).to_dict()}
    assert len(dados) == duplicados + len(rejeitados) + len(df)
    return df.reset_index(drop=True), rejeitados, auditoria
