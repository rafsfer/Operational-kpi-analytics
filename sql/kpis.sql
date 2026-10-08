-- Indicadores da coorte de aberturas; pendentes não entram nas médias de resolução.
-- consulta: kpis_gerais
SELECT COUNT(*) AS total_atendimentos,
       SUM(resolvido) AS resolvidos,
       AVG(CASE WHEN resolvido = 1 THEN tempo_resolucao_horas END) AS tempo_medio_resolucao_horas,
       100.0 * SUM(COALESCE(dentro_sla, 0)) / NULLIF(COUNT(*), 0) AS sla_percentual,
       100.0 * SUM(COALESCE(dentro_sla, 0)) / NULLIF(SUM(resolvido), 0) AS sla_resolvidos_percentual,
       100.0 * SUM(COALESCE(resolvido_primeiro_contato, 0)) / NULLIF(SUM(resolvido), 0) AS fcr_percentual,
       100.0 * COUNT(resolvido_primeiro_contato) / NULLIF(SUM(resolvido), 0) AS fcr_cobertura_percentual,
       COUNT(*) - SUM(resolvido) AS backlog,
       AVG(CASE WHEN resolvido = 1 THEN nota_satisfacao END) AS csat_media,
       COUNT(CASE WHEN resolvido = 1 THEN nota_satisfacao END) AS respostas_csat,
       100.0 * COUNT(CASE WHEN resolvido = 1 THEN nota_satisfacao END) / NULLIF(SUM(resolvido), 0) AS csat_cobertura_percentual,
       SUM(resolvido) AS produtividade_resolvidos,
       100.0 * SUM(resolvido) / NULLIF(COUNT(*), 0) AS taxa_resolucao_percentual
FROM atendimentos;
