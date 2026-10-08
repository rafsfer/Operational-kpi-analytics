"""Regras de negócio e caminhos compartilhados pelas etapas."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DATA_CORTE = "2026-07-01 00:00:00"
INICIO = "2026-01-01 00:00:00"
SEMENTE = 42
SLA_HORAS = {"Crítica": 8, "Alta": 24, "Média": 48, "Baixa": 72}
EQUIPES = {"Relacionamento": 8, "Suporte técnico": 10, "Financeiro": 6, "Retenção": 5}
CATEGORIAS = {
    "Cadastro": ("Relacionamento", ["Atualização", "Acesso"]),
    "Dúvida": ("Relacionamento", ["Produto", "Plano"]),
    "Problema técnico": ("Suporte técnico", ["Conexão", "Aplicativo"]),
    "Cobrança": ("Financeiro", ["Fatura", "Pagamento"]),
    "Cancelamento": ("Retenção", ["Contrato", "Renovação"]),
}
