# Validação no Power BI Desktop

Conferência realizada em 08/10/2026 no Power BI Desktop 2.158.1304.0. Todos os dados são sintéticos.

O modelo foi carregado no Desktop com 19.922 atendimentos e 181 datas de calendário. As medidas foram consultadas diretamente no motor Analysis Services local, usando DAX, e comparadas aos CSVs/JSONs preparados pelo projeto.

| Indicador | Resultado DAX sem filtros |
| --- | ---: |
| Total de atendimentos | 19.922 |
| SLA geral | 65,3950406585684% |
| FCR | 35,6948083195209% |
| Tempo médio de resolução | 38,9009838290945 h |
| Backlog no corte | 1.219 |
| CSAT médio | 4,1407018694654 |

Os seis resultados coincidem com `data/processed/kpis_gerais.json`, dentro da precisão numérica de ponto flutuante. O cartão de volume pode apresentar abreviação automática; o total exato do modelo é 19.922.

| Mês | Backlog histórico em DAX e CSV |
| --- | ---: |
| 2026-01 | 213 |
| 2026-02 | 361 |
| 2026-03 | 571 |
| 2026-04 | 703 |
| 2026-05 | 886 |
| 2026-06 | 1.219 |

O estoque histórico coincide com cada posição de `data/processed/backlog_mensal.csv`.

No cenário **junho/2026 + Relacionamento + Chat**, os seis indicadores também coincidem com agregações diretas dos tickets filtrados, com tolerância absoluta de 1e-8. O resultado detalhado está em [validacao_powerbi_filtros.json](validacao_powerbi_filtros.json).

As duas páginas foram renderizadas no Desktop. O arquivo `powerbi/operational_kpis.pbix` foi salvo com o modelo de dados e a captura da página principal está em `powerbi/dashboard.png`. A integridade dos componentes ZIP do PBIX foi conferida.

Esta conferência cobre os indicadores gerais, o estoque mensal e o cenário combinado descrito; não substitui uma revisão completa de todas as combinações de filtros e de acessibilidade.
