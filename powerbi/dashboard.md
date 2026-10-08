# Construção do dashboard no Power BI

## Objetivo e escopo

Construa uma página principal **Visão Geral da Operação**, destinada à gestão da Nexa Serviços. Todos os dados são sintéticos. O relatório observa janeiro a junho de 2026 até o corte exclusivo de 01/07/2026. Este guia acompanha dados, DAX e tema; o projeto nativo já está disponível em [operational_kpis.pbip](operational_kpis.pbip). Consulte [ABRIR_DASHBOARD.md](ABRIR_DASHBOARD.md) para carregar os dados e conferir o relatório no Desktop. As etapas manuais abaixo também servem como referência para revisar o modelo.

## Importar os dados

1. Execute o projeto e confira o log de validação.
2. No Power BI Desktop, use **Obter dados → Texto/CSV** para `data/processed/atendimentos.csv`. Escolha UTF-8 e vírgula como delimitador. Renomeie a consulta para **Atendimentos**.
3. Importe `data/processed/calendario.csv` como **Calendario**.
4. Selecione **Transformar dados**. Não importe os CSVs de resultados agregados no mesmo modelo: as medidas devem partir dos tickets para evitar soma de percentuais.
5. Corrija explicitamente os tipos da tabela abaixo. Use **Alterar tipo → Usar localidade → Inglês (Estados Unidos)** para decimais com ponto, se a configuração PT-BR não os reconhecer corretamente. Não substitua os nulos por zero.
6. Duplique a coluna `data_abertura` no Power Query, transforme a cópia em **Data** e renomeie para `Data abertura`. Preserve a coluna original com hora para o backlog e os tempos.
7. Em Calendario, defina `data` como Data e `mes` como Texto. Marque Calendario como tabela de datas, usando `data`.
8. Crie um relacionamento ativo **Calendario[data] (1) → Atendimentos[Data abertura] (*)**, direção de filtro única. O calendário contém todos os dias, sem duplicidades. Não relacione datas com horário diretamente a datas sem horário.
9. Feche e aplique. Utilize exclusivamente campos de Calendario nos filtros e eixos temporais.

| Tipo | Colunas |
| --- | --- |
| Número inteiro | id_atendimento, id_cliente, quantidade_interacoes, resolvido, dentro_sla, resolvido_primeiro_contato, sla_horas, pendente_vencido, resposta_extrema |
| Data/hora | data_abertura, data_fechamento |
| Número decimal | tempo_primeira_resposta_min, tempo_resolucao_horas, nota_satisfacao, idade_horas |
| Texto | canal, categoria, subcategoria, prioridade, equipe, atendente, status, mes_abertura, mes_fechamento |

Os IDs são identificadores: defina **Não resumir**. A satisfação aceita nulos e números de 1–5. Pendentes têm fechamento, duração e resultados SLA/FCR em branco.

A importação CSV evita depender de um driver SQLite externo. O banco é usado pelas análises SQL; o Power BI consome a mesma base tratada exportada. Não carregue os dados brutos ou a quarentena na página gerencial.

## Medidas

Abra [medidas.dax](medidas.dax). Crie uma medida por vez com **Nova medida**, copiando sua fórmula. O arquivo é uma referência e não um script executável como SQL. Dependendo da configuração regional, poderá ser necessário trocar vírgulas por ponto e vírgula nos argumentos.

Formate SLA, FCR, coberturas e taxa de resolução como **percentual (duas casas)**. Formate tempos como decimal com duas casas e sufixo visual `h`. CSAT tem duas casas, com subtítulo `escala 1–5`. Contagens são inteiros com separador de milhar. Não multiplique as medidas de razão por 100 antes de formatá-las como percentual.

O cartão Backlog mostra **pendências da coorte selecionada na data de corte**. `Backlog histórico` reconstrói o estoque na última data visível, removendo o filtro de abertura do calendário. Não coloque status ou `mes_abertura` da fato em filtros dessa medida. Ela mantém os filtros de equipe, canal, categoria e prioridade.

Para um gráfico de backlog mensal, use Calendario[mes] e `Backlog histórico`. Confira com `backlog_mensal.csv`. O estoque inclui tickets de meses anteriores ainda pendentes naquele momento, mesmo se hoje constam como resolvidos. Não some os estoques mensais.

## Layout da página

Use uma página **1920 × 1200**, com fundo claro e margens de 24 px. Importe [tema.json](tema.json) em **Exibir → Temas → Procurar temas**. O tema define a paleta; ajuste a legibilidade no Desktop.

- Cabeçalho: título, `Dados sintéticos | Jan–Jun/2026 | Corte: 01/07/2026` e botão Limpar filtros.
- Faixa de filtros: período de abertura, equipe, canal, categoria e prioridade.
- Faixa de seis cartões: Total de atendimentos; SLA; FCR; Tempo médio de resolução; Backlog; CSAT.
- Três linhas de três gráficos, conforme a tabela abaixo.
- Rodapé: legenda do SLA geral e explicação da coorte/corte. Inclua coberturas FCR/CSAT e SLA dos resolvidos em dicas de ferramenta.

Os seis cartões e nove gráficos são os visuais obrigatórios. O estoque histórico e a produtividade podem ficar em uma página adicional **Diagnóstico**, para complementar a investigação sem reduzir a leitura da página principal.

| Visual | Eixo / categoria | Valor | Pergunta e apresentação |
| --- | --- | --- | --- |
| Linha de volume mensal | Calendario[mes] | Total de atendimentos | Quando a demanda aumenta? Ordenar meses em ordem crescente. |
| Linha de SLA | Calendario[mes] | SLA | Qual parcela da demanda foi resolvida no prazo? Eixo 0–100%. |
| Barras de SLA por equipe | equipe | SLA | Qual equipe tem maior cumprimento? Exibir volume e SLA dos resolvidos no tooltip. |
| Barras de backlog por equipe | equipe | Backlog | Onde estão as pendências atuais da coorte? Ordem decrescente e tooltip de vencidos. |
| Barras de tempo por categoria | categoria | Tempo médio de resolução | Quais demandas levam mais tempo? Unidade em horas. |
| Barras de FCR por equipe | equipe | FCR | Onde há mais resoluções em uma interação? Tooltip com cobertura. |
| Linha de CSAT mensal | Calendario[mes] | CSAT | Como variam as avaliações das coortes? Eixo fixo 1–5; tooltip com respostas e cobertura. |
| Barras de volume por canal | canal | Total de atendimentos | Qual canal concentra demanda? Inclua Não informado. |
| Colunas de volume por prioridade | prioridade | Total de atendimentos | Como a demanda se distribui por urgência? Ordem Crítica, Alta, Média, Baixa. |

Para ordenar prioridades, crie uma coluna auxiliar via Power Query: Crítica = 1, Alta = 2, Média = 3, Baixa = 4. Use **Classificar por coluna**. `mes` no formato YYYY-MM já ordena cronologicamente. Não trate texto como data ambígua.

## Interações, acessibilidade e leitura

Todos os filtros devem atingir cartões e visuais da página principal. A medida de estoque histórico usa o fim do período como data de posição, mantendo as dimensões. Evite filtros diretos em `mes_abertura` da fato e rankings que excluam silenciosamente equipes.

Use rótulos e títulos claros; não comunique prazo somente com cor. Verde pode indicar cumprimento e laranja pode chamar atenção para pendências, mas inclua valores. Não crie semáforos de metas inventadas: os prazos de tickets foram definidos; uma meta gerencial de SLA exigiria outra decisão de negócio. Adicione texto alternativo com a pergunta de cada gráfico e ajuste a ordem de navegação por teclado.

## Conferência dos dados e das medidas

1. Sem filtros, compare os seis cartões com `data/processed/kpis_gerais.json`.
2. Compare volume, SLA, FCR e CSAT por equipe com `kpis_por_equipe.csv` e por mês com `kpis_por_mes_abertura.csv`.
3. Verifique que Total = Resolvidos + Backlog e Taxa de resolução = Resolvidos / Total.
4. SLA dos resolvidos deve ser maior ou igual ao SLA geral, e ambos devem permanecer em 0–100%.
5. CSAT deve ficar entre 1 e 5; vazios não são avaliações zero. FCR exige observar a cobertura.
6. Teste cada filtro e dois filtros combinados. Confira a população correspondente em Python/SQL, sem tirar média das porcentagens exportadas.
7. Para estoque histórico sem filtros dimensionais, compare cada mês com `backlog_mensal.csv`. O total do visual representa a posição final, não a soma dos meses.
8. Verifique que junho tem tempo de observação menor. Escreva isso na dica de ferramenta para evitar interpretar toda queda de resolução como piora operacional.
9. Teste um grupo sem resolvidos: medidas de média e razão sem população elegível devem ficar em branco. Contagens podem aparecer em branco em células sem linhas; para mostrar zero, use COALESCE apenas nas medidas de contagem.
10. Salve como `powerbi/operational_kpis.pbix`, revise o layout e exporte uma captura real do Desktop para o portfólio.

**Estado desta entrega:** dashboard salvo em [operational_kpis.pbix](operational_kpis.pbix), com dados carregados e tema Nexa. Os seis KPIs gerais, o backlog histórico de janeiro a junho e um cenário combinado de mês/equipe/canal foram conferidos em DAX contra os dados do projeto. As duas páginas foram renderizadas no Desktop; a captura real da página principal está em [dashboard.png](dashboard.png). Consulte [o registro de validação](../reports/validacao_powerbi.md).

## Referências oficiais

O modelo e as instruções de filtro se apoiam na documentação da Microsoft: [relacionamentos no Power BI](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand), [CALCULATE](https://learn.microsoft.com/en-us/dax/calculate-function-dax) e [fundamentos de DAX](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-quickstart-learn-dax-basics). As medidas deste projeto foram escritas para o modelo descrito acima.
