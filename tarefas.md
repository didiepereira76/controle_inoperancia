# Tarefas

> Registro do que já foi entregue e de possíveis próximos passos identificados no código.

## ✅ Concluído

- [x] Carga híbrida de dados: CSV local (2024/2025) + Google Sheets (2026) com fallback.
- [x] Validação de planilha privada (checagem de 4 colunas).
- [x] Cache com `ttl=600` + botão de atualização manual.
- [x] Normalização de dados (datas BR, horas, limpeza de IDs, merge com locais).
- [x] Contagem de CEs tratando valores combinados por `|` e distintos por ano.
- [x] Cards de métricas (CEs, inoperância acumulada, equipamentos, média).
- [x] Gráfico Top 10 CEs por impacto.
- [x] Ranking de equipamentos mais inoperantes.
- [x] Histórico mensal comparando anos.
- [x] Tabela analítica com hover premium.
- [x] Exportação CSV da tabela filtrada (`utf-8-sig`).
- [x] Filtros por ano, equipamento (com endereço) e exibição de sentido.
- [x] Tema escuro + CSS modularizado (glassmorphism, fonte Outfit).
- [x] README com guia de instalação e execução.

## 🛠️ Revisão de código aplicada (2026-10-15)

- [x] **Robustez de caminhos:** CSVs e assets resolvidos via `Path(__file__)` — roda de qualquer diretório.
- [x] **Consistência do Top 10 CEs:** passou a explodir CEs combinadas por `|`.
- [x] **Botão de download:** `key` estável, sem `uuid` aleatório por rerun.
- [x] **Duplicação removida:** helpers de contagem de CE e de tema de gráfico em `components.py`.
- [x] **Imports não usados removidos** e versões fixadas em `requirements.txt`.
- [x] **Aviso de datas inválidas** na sidebar.

## 🔜 Possíveis próximos passos (sugestões)

> Não são pendências obrigatórias — são oportunidades observadas no código.

- [ ] **Virada de ano:** `TAB_2026` e o rótulo "ano atual (2026)" estão fixos. Considerar derivar o ano ativo dinamicamente (ex.: ano corrente) para evitar edição manual a cada ano.
- [ ] **Paleta de anos fixa:** o mapa de cores do histórico mensal cobre só 2024–2026; ao adicionar novos anos será preciso estender `color_discrete_map`.
- [ ] **Teste da integração online:** validar comportamento quando a planilha muda de estrutura ou fica temporariamente fora do ar.
- [ ] **Filtro por mês/período:** hoje o filtro é por ano e equipamento; um recorte por mês poderia ajudar análises pontuais.
- [ ] **Indicador de última atualização:** mostrar data/hora da última carga dos dados online.
- [ ] **Documentar o formato das planilhas de origem** para quem for manter os dados.

## 📌 Observações de manutenção

- A aplicação deve ser executada a partir da pasta `bd_ce` (caminhos relativos).
- O ID da planilha está em `utils/data_loader.py` (`SPREADSHEET_ID`).
- A planilha de 2026 precisa estar compartilhada como "Qualquer pessoa com o link pode ler".
