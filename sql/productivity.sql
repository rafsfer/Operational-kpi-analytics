-- A contagem de resoluções não mede eficiência por hora nem corrige a complexidade dos tickets.
-- consulta: produtividade_equipes
SELECT e.equipe, e.atendentes_planejados,
       SUM(a.resolvido) AS resolvidos,
       ROUND(1.0 * SUM(a.resolvido) / e.atendentes_planejados, 2) AS resolvidos_por_atendente_planejado
FROM equipes e
LEFT JOIN atendimentos a ON a.equipe = e.equipe
GROUP BY e.equipe, e.atendentes_planejados
ORDER BY resolvidos DESC;

-- consulta: produtividade_mensal
SELECT mes_fechamento AS mes, equipe, atendente, COUNT(*) AS resolvidos
FROM atendimentos
WHERE resolvido = 1
GROUP BY mes_fechamento, equipe, atendente
ORDER BY mes, equipe, resolvidos DESC;
