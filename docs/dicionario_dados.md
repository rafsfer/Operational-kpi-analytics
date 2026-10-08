# Dicionário de dados e regras

Cada linha tratada representa um ticket único. O arquivo usa UTF-8 com BOM, vírgula como delimitador, ponto decimal e datas YYYY-MM-DD HH:MM:SS. Nulos aparecem como campo vazio. Campos derivados substituem indicadores brutos quando aplicável.

| Campo | Tipo / unidade | Regra |
| --- | --- | --- |
| id_atendimento | Inteiro | Positivo e único; conflitos vão para quarentena |
| id_cliente | Inteiro | Identificador sintético positivo; pode repetir |
| data_abertura | Data/hora | Entre 01/01/2026 inclusivo e 01/07/2026 exclusivo |
| data_fechamento | Data/hora ou nulo | Somente resolvidos; não anterior à abertura; anterior ao corte |
| canal | Texto | Chat, E-mail, Telefone, WhatsApp, Não informado |
| categoria | Texto | Cadastro, Dúvida, Problema técnico, Cobrança, Cancelamento |
| subcategoria | Texto | Cadastro: Atualização/Acesso; Dúvida: Produto/Plano; técnico: Conexão/Aplicativo; Cobrança: Fatura/Pagamento; Cancelamento: Contrato/Renovação |
| prioridade | Texto | Crítica, Alta, Média, Baixa |
| equipe | Texto | Relacionamento, Suporte técnico, Financeiro, Retenção; alocação fixa por categoria |
| atendente | Texto | Código fictício da equipe; não representa nome de pessoa |
| status | Texto | Aberto, Em andamento, Resolvido |
| tempo_primeira_resposta_min | Minutos ou nulo | Não negativo; acima de 1.440 marcado como extremo |
| tempo_resolucao_horas | Horas corridas ou nulo | Diferença entre fechamento e abertura dos resolvidos |
| dentro_sla | 0/1 ou nulo | 1 se resolvido com tempo menor ou igual ao prazo; pendentes nulos |
| resolvido_primeiro_contato | 0/1 ou nulo | Resolvido e uma interação; pendentes ou interações desconhecidas nulos |
| nota_satisfacao | Escala 1–5 ou nulo | Apenas avaliações válidas dos resolvidos |
| quantidade_interacoes | Inteiro ou nulo | Pelo menos 1; valores inválidos anulados |
| resolvido | 0/1 | 1 quando status é Resolvido |
| sla_horas | Horas corridas | Crítica 8; Alta 24; Média 48; Baixa 72 |
| mes_abertura | YYYY-MM | Coorte de entrada |
| mes_fechamento | YYYY-MM ou nulo | Período de produção |
| idade_horas | Horas | Tempo entre abertura e corte; usado no estoque atual |
| pendente_vencido | 0/1 | Pendente cuja idade excede o prazo |
| resposta_extrema | 0/1 | Primeira resposta acima de 24 horas; não remove ticket |

Relacionamento atende Cadastro e Dúvida; Suporte técnico atende Problema técnico; Financeiro atende Cobrança; Retenção atende Cancelamento. Não existem transferências neste cenário.

## Artefatos de qualidade

`qualidade.json` registra nulos, tipos iniciais, correções de domínios, valores anulados, linhas rejeitadas e duplicados. As contagens de categorias padronizadas incluem valores ausentes transformados. Motivos de rejeição podem se acumular no mesmo ticket, portanto não some motivos para contar linhas.

`rejeitados.csv` conserva os valores recebidos e adiciona `motivo_rejeicao`. Métricas opcionais inválidas não removem o ticket, mas ficam nulas. A decisão evita enviesar o volume de demanda pela disponibilidade de avaliações.

## Limitações analíticas

Não há estoque anterior a janeiro, horas trabalhadas, reaberturas, transferências, calendário de horas úteis ou histórico dos contatos. A satisfação depende de resposta voluntária simulada. Os tickets recentes têm menor janela para fechamento e a simulação cria parte das associações observadas.
