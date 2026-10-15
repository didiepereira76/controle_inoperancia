# PRD — Controle de Inoperância de Radares

> Documento de Requisitos de Produto. Escrito de forma **descritiva** (engenharia reversa do sistema já construído), não prescritiva.

## 1. Visão geral

Dashboard interno para monitorar a **inoperância de radares (equipamentos de fiscalização de trânsito)** da cidade, medindo quanto tempo cada radar ficou fora de operação e qual o impacto acumulado por período, equipamento e local.

- **Área responsável:** GTSV — Gerência de Tecnologia em Sistema Viário (CET).
- **Tipo de produto:** aplicação web local (Streamlit), uso interno.
- **Público-alvo:** equipe de gestão e técnicos da GTSV.

## 2. Problema que resolve

As ocorrências de inoperância (CEs — Comunicados de Evento) são registradas em planilhas. Faltava uma visão consolidada que respondesse rapidamente:

- Quanto tempo total os radares ficaram inoperantes?
- Quais radares e quais CEs concentram o maior impacto?
- Como a inoperância evolui mês a mês, comparando anos?
- Qual o detalhe por equipamento, incluindo local e sentido?

## 3. Usuários e necessidades

| Usuário | Necessidade principal |
|---|---|
| Gestor da GTSV | Visão executiva (totais, rankings, tendência mensal) |
| Técnico | Detalhe analítico por equipamento e exportação dos dados filtrados |

## 4. Funcionalidades (entregues)

1. **Filtros interativos**
   - Por **ano** (multisseleção, 2024 / 2025 / 2026).
   - Por **equipamento** (com exibição do endereço junto ao código).
   - Exibição do **sentido** do equipamento selecionado (campo informativo).
2. **Métricas principais (cards)**
   - Número de CE's (contagem distinta, tratando CEs combinados e por ano).
   - Inoperância acumulada (em horas).
   - Equipamentos afetados (contagem distinta).
   - Média de horas por ocorrência.
3. **Gráficos de impacto**
   - Top 10 CEs com maior impacto (horas).
   - Ranking dos 10 equipamentos mais inoperantes.
4. **Histórico mensal** — inoperância por mês, agrupada e comparada por ano.
5. **Tabela analítica** — detalhe por equipamento (série, local, sentido, nº de CEs, horas), com destaque no hover.
6. **Exportação** — download da tabela filtrada em CSV.
7. **Atualização de dados** — botão para limpar cache e recarregar.

## 5. Fontes de dados

- **2024 e 2025:** arquivos CSV locais (dados estáticos/históricos).
- **2026 (ano ativo):** Google Planilhas (online, aba `BD_Looker`), com **fallback automático** para CSV local se a planilha estiver indisponível/privada.
- **Cadastro de locais:** CSV local (`Controle_de_CE_-_locais.csv`) com série, local e sentido de cada equipamento.

## 6. Requisitos não-funcionais

- **Execução local** via `streamlit run dashboard.py`; sem necessidade de servidor dedicado.
- **Resiliência:** o sistema nunca quebra por falta de internet — cai para dados locais.
- **Cache de 10 min** (`ttl=600`) para dados online.
- **Idioma/formatação:** português do Brasil (números com separador de milhar `.` e decimal `,`).
- **Visual:** tema escuro, identidade visual verde (padrão CET).

## 7. Fora de escopo (hoje)

- Autenticação/controle de acesso por usuário.
- Escrita de dados (o dashboard é somente leitura).
- Banco de dados relacional (persistência é em CSV / Google Sheets).
- Alertas automáticos / notificações.

## 8. Métricas de sucesso

- Consolidação de 3 anos de dados em uma única tela.
- Identificação imediata dos maiores ofensores (CE e equipamento).
- Exportação dos dados filtrados sem retrabalho manual.
