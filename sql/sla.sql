-- O SLA geral segue o denominador pedido: todos os tickets da coorte.
-- O SLA dos resolvidos e os pendentes vencidos ajudam a interpretar esse resultado.
-- consulta: sla_por_prioridade
SELECT prioridade, MAX(sla_horas) AS prazo_horas,
       COUNT(*) AS total_atendimentos,
       SUM(resolvido) AS resolvidos,
       ROUND(100.0 * SUM(COALESCE(dentro_sla, 0)) / COUNT(*), 2) AS sla_percentual,
       ROUND(100.0 * SUM(COALESCE(dentro_sla, 0)) / NULLIF(SUM(resolvido), 0), 2) AS sla_resolvidos_percentual,
       SUM(pendente_vencido) AS pendentes_vencidos
FROM atendimentos
GROUP BY prioridade
ORDER BY prazo_horas;
