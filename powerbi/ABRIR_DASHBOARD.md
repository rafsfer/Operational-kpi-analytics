# Abrir o dashboard

Abra **[operational_kpis.pbix](operational_kpis.pbix)** no Power BI Desktop. O arquivo já contém os dados, o modelo, as medidas DAX, o tema Nexa e duas páginas:

- **Visão Geral da Operação:** seis cartões, nove gráficos e filtros de mês, equipe, canal, categoria e prioridade.
- **Diagnóstico:** backlog histórico, resolvidos por equipe na coorte de abertura, pendentes vencidos e cobertura CSAT.

Para atualizar os CSVs, clique em **Atualizar**. A consulta **PastaDados** aponta para a pasta local `data/processed/`; se mover o repositório, ajuste esse parâmetro em **Transformar dados → Gerenciar parâmetros** antes de atualizar.

O [projeto PBIP](operational_kpis.pbip) oferece uma versão editável em arquivos de texto. Em outro computador, abra-o e clique em Atualizar para carregar os CSVs, pois o cache local é ignorado pelo Git.

Os KPIs gerais, os seis meses do estoque histórico e um cenário de filtros combinados foram conferidos no motor DAX do Desktop. Consulte [validacao_powerbi.md](../reports/validacao_powerbi.md). A [captura da página principal](dashboard.png) foi obtida diretamente do aplicativo.
