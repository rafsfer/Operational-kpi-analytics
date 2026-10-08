# Validação da entrega

Execução verificada em 08/10/2026, com Python 3.11.9, Pandas 2.3.3 e NumPy 2.4.6. Cenário padrão: semente 42 e 20.000 tickets originais.

## Evidências

- 17 testes aprovados; saída completa em `testes.txt`.
- Execução de `main.py` concluída, inclusive as 14 consultas SQL nomeadas.
- KPIs gerais e todos os KPIs das seis dimensões conferidos entre Python e SQL.
- Estoque de cada mês conferido entre Python e SQL e reconciliado com entradas e saídas.
- Banco SQLite: `PRAGMA integrity_check` retorna `ok`.
- CSV tratado reimportado: unicidade de IDs, domínios, notas e nulos esperados validados.
- Todos os KPIs recalculados a partir do CSV coincidem com o JSON exportado.
- Calendário com 181 dias únicos, de 01/01/2026 a 30/06/2026.
- `.venv`, arquivos `.db`, caches e `.env` conferidos como ignorados pelo Git.
- README, docstrings, comentários Python/SQL e mensagens de commit em português.

## Qualidade dos dados

- 20,120 linhas recebidas; 120 duplicados removidos; 78 rejeitados; 19,922 tickets tratados.
- Algumas grafias inconsistentes também geram incompatibilidade entre categoria, equipe e subcategoria. Esses registros são rejeitados, sem adivinhar a categoria correta.

## Resultado dos indicadores

| Indicador | Resultado |
| --- | --- |
| Total de atendimentos | 19.922 |
| Resolvidos | 18.703 |
| Tempo médio de resolução (h) | 38,90 |
| SLA geral (%) | 65,40 |
| SLA dos resolvidos (%) | 69,66 |
| FCR (%) | 35,69 |
| Cobertura FCR (%) | 99,93 |
| Backlog | 1.219 |
| CSAT (1–5) | 4,14 |
| Respostas CSAT | 12.196 |
| Cobertura CSAT (%) | 65,21 |
| Produção absoluta | 18.703 |
| Taxa de resolução (%) | 93,88 |

## Limites da validação

Os dados preparados para o Power BI foram verificados. O Power BI Desktop não foi executado: importação visual, medidas DAX e layout devem ser conferidos com o checklist de `powerbi/dashboard.md`. Não existe PBIX nesta entrega.
