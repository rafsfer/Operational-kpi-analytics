-- Reutilizamos as mesmas fórmulas para permitir comparação entre dimensões.

-- consulta: kpis_por_equipe
SELECT equipe,
       COUNT(*) AS total_atendimentos,
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
FROM atendimentos
GROUP BY equipe
ORDER BY equipe;

-- consulta: kpis_por_mes_abertura
SELECT mes_abertura,
       COUNT(*) AS total_atendimentos,
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
FROM atendimentos
GROUP BY mes_abertura
ORDER BY mes_abertura;

-- consulta: kpis_por_categoria
SELECT categoria,
       COUNT(*) AS total_atendimentos,
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
FROM atendimentos
GROUP BY categoria
ORDER BY categoria;

-- consulta: kpis_por_canal
SELECT canal,
       COUNT(*) AS total_atendimentos,
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
FROM atendimentos
GROUP BY canal
ORDER BY canal;

-- consulta: kpis_por_atendente
SELECT atendente,
       COUNT(*) AS total_atendimentos,
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
FROM atendimentos
GROUP BY atendente
ORDER BY atendente;

-- consulta: kpis_por_prioridade
SELECT prioridade,
       COUNT(*) AS total_atendimentos,
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
FROM atendimentos
GROUP BY prioridade
ORDER BY prioridade;
