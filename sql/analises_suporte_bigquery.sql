-- ============================================================
-- Projeto: Data Lake de Chamados de Suporte Técnico
-- Plataforma: Google BigQuery
-- Dataset: suporte_tecnico
-- Objetivo: analisar chamados de Service Desk e logs técnicos
-- ============================================================

-- 1. Total de chamados
SELECT
  COUNT(*) AS total_chamados
FROM
  `data-lake-suporte-jessica.suporte_tecnico.chamados_suporte`;

-- 2. Chamados por categoria
SELECT
  categoria,
  COUNT(*) AS total_chamados
FROM
  `data-lake-suporte-jessica.suporte_tecnico.chamados_suporte`
GROUP BY categoria
ORDER BY total_chamados DESC;

-- 3. Chamados por prioridade
SELECT
  prioridade,
  COUNT(*) AS total_chamados
FROM
  `data-lake-suporte-jessica.suporte_tecnico.chamados_suporte`
GROUP BY prioridade
ORDER BY total_chamados DESC;

-- 4. Cumprimento de SLA por prioridade
SELECT
  prioridade,
  COUNTIF(sla_cumprido IN ('Sim', 'Não')) AS chamados_finalizados,
  COUNTIF(sla_cumprido = 'Sim') AS dentro_sla,
  COUNTIF(sla_cumprido = 'Não') AS fora_sla,
  ROUND(
    100 * SAFE_DIVIDE(
      COUNTIF(sla_cumprido = 'Sim'),
      COUNTIF(sla_cumprido IN ('Sim', 'Não'))
    ),
    1
  ) AS percentual_cumprimento_sla
FROM
  `data-lake-suporte-jessica.suporte_tecnico.chamados_suporte`
GROUP BY prioridade
ORDER BY
  CASE prioridade
    WHEN 'Crítica' THEN 1
    WHEN 'Alta' THEN 2
    WHEN 'Média' THEN 3
    WHEN 'Baixa' THEN 4
  END;

-- 5. Tempo médio de resolução por categoria
SELECT
  categoria,
  ROUND(AVG(tempo_resolucao_horas), 2) AS tempo_medio_resolucao_horas
FROM
  `data-lake-suporte-jessica.suporte_tecnico.chamados_suporte`
WHERE tempo_resolucao_horas IS NOT NULL
GROUP BY categoria
ORDER BY tempo_medio_resolucao_horas DESC;

-- 6. Reincidência por categoria
SELECT
  categoria,
  COUNT(*) AS total_chamados,
  COUNTIF(reincidente = 'Sim') AS chamados_reincidentes,
  ROUND(
    100 * SAFE_DIVIDE(
      COUNTIF(reincidente = 'Sim'),
      COUNT(*)
    ),
    1
  ) AS percentual_reincidencia
FROM
  `data-lake-suporte-jessica.suporte_tecnico.chamados_suporte`
GROUP BY categoria
ORDER BY percentual_reincidencia DESC;

-- 7. Relação entre SLA e satisfação (CSAT)
SELECT
  sla_cumprido,
  COUNT(*) AS total_avaliacoes,
  ROUND(AVG(csat), 2) AS media_csat
FROM
  `data-lake-suporte-jessica.suporte_tecnico.chamados_suporte`
WHERE
  csat IS NOT NULL
  AND sla_cumprido IN ('Sim', 'Não')
GROUP BY sla_cumprido
ORDER BY media_csat DESC;

-- 8. Relação entre reincidência, tempo de resolução e CSAT
SELECT
  reincidente,
  COUNT(*) AS total_chamados,
  ROUND(AVG(tempo_resolucao_horas), 2) AS tempo_medio_resolucao,
  ROUND(AVG(csat), 2) AS media_csat
FROM
  `data-lake-suporte-jessica.suporte_tecnico.chamados_suporte`
WHERE
  tempo_resolucao_horas IS NOT NULL
  AND csat IS NOT NULL
GROUP BY reincidente
ORDER BY reincidente DESC;

-- 9. Distribuição dos logs por severidade
SELECT
  severidade,
  COUNT(*) AS total_eventos
FROM
  `data-lake-suporte-jessica.suporte_tecnico.logs_sistema`
GROUP BY severidade
ORDER BY total_eventos DESC;

-- 10. Erros e eventos críticos por sistema
SELECT
  sistema,
  COUNTIF(severidade = 'CRITICAL') AS eventos_criticos,
  COUNTIF(severidade = 'ERROR') AS eventos_erro,
  COUNT(*) AS total_eventos
FROM
  `data-lake-suporte-jessica.suporte_tecnico.logs_sistema`
GROUP BY sistema
ORDER BY eventos_criticos DESC, eventos_erro DESC;

-- 11. Cruzamento entre logs e chamados
SELECT
  l.sistema,
  COUNT(*) AS logs_vinculados,
  ROUND(AVG(c.tempo_resolucao_horas), 2) AS tempo_medio_resolucao,
  ROUND(AVG(c.csat), 2) AS media_csat
FROM
  `data-lake-suporte-jessica.suporte_tecnico.logs_sistema` l
JOIN
  `data-lake-suporte-jessica.suporte_tecnico.chamados_suporte` c
ON l.id_chamado = c.id_chamado
WHERE
  l.id_chamado IS NOT NULL
  AND c.tempo_resolucao_horas IS NOT NULL
  AND c.csat IS NOT NULL
GROUP BY l.sistema
ORDER BY logs_vinculados DESC;

-- 12. Resumo executivo de KPIs
SELECT
  COUNT(*) AS total_chamados,
  COUNTIF(status IN ('Fechado', 'Resolvido')) AS chamados_finalizados,
  ROUND(
    100 * SAFE_DIVIDE(
      COUNTIF(sla_cumprido = 'Sim'),
      COUNTIF(sla_cumprido IN ('Sim', 'Não'))
    ),
    1
  ) AS percentual_sla,
  ROUND(AVG(tempo_resolucao_horas), 2) AS tempo_medio_resolucao,
  ROUND(AVG(csat), 2) AS csat_medio,
  ROUND(
    100 * SAFE_DIVIDE(
      COUNTIF(reincidente = 'Sim'),
      COUNT(*)
    ),
    1
  ) AS percentual_reincidencia
FROM
  `data-lake-suporte-jessica.suporte_tecnico.chamados_suporte`;

-- 13. Consulta usada na visualização de chamados por categoria
SELECT
  categoria,
  COUNT(*) AS total_chamados
FROM
  `data-lake-suporte-jessica.suporte_tecnico.chamados_suporte`
GROUP BY categoria
ORDER BY total_chamados DESC;
