-- O estoque histórico considera tickets abertos antes do fim do mês e ainda não fechados nesse momento.
-- consulta: backlog_historico
WITH meses AS (
    SELECT mes, MIN(data) || ' 00:00:00' AS inicio,
           datetime(MIN(data), '+1 month') AS fim
    FROM calendario
    GROUP BY mes
)
SELECT m.mes,
       SUM(CASE WHEN a.data_abertura < m.inicio
                     AND (a.data_fechamento IS NULL OR a.data_fechamento >= m.inicio)
                THEN 1 ELSE 0 END) AS backlog_inicial,
       SUM(CASE WHEN a.data_abertura >= m.inicio AND a.data_abertura < m.fim
                THEN 1 ELSE 0 END) AS aberturas,
       SUM(CASE WHEN a.data_fechamento >= m.inicio AND a.data_fechamento < m.fim
                THEN 1 ELSE 0 END) AS resolucoes,
       SUM(CASE WHEN a.data_abertura < m.fim
                     AND (a.data_fechamento IS NULL OR a.data_fechamento >= m.fim)
                THEN 1 ELSE 0 END) AS backlog_final
FROM meses m
LEFT JOIN atendimentos a ON a.data_abertura < m.fim
GROUP BY m.mes
ORDER BY m.mes;

-- consulta: backlog_por_equipe
SELECT equipe, COUNT(*) AS backlog,
       SUM(pendente_vencido) AS pendentes_vencidos,
       ROUND(AVG(idade_horas), 2) AS idade_media_horas
FROM atendimentos
WHERE resolvido = 0
GROUP BY equipe
ORDER BY backlog DESC;
