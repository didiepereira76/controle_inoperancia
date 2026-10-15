# Memória do Projeto

> Resumo de contexto, decisões e convenções para que qualquer pessoa (ou IA) consiga continuar o projeto sem reler todo o código.

## O que é

Dashboard Streamlit da **GTSV (Gerência de Tecnologia em Sistema Viário / CET)** para monitorar a **inoperância de radares** de trânsito. Lê registros de CEs (Comunicados de Evento), consolida por ano/equipamento/local e exibe métricas, gráficos e tabela analítica. Somente leitura.

## Vocabulário

- **CE:** Comunicado de Evento = uma ocorrência de inoperância (ex.: `CE: 009`).
- **Série / Equipamento:** código do radar (ex.: `337`).
- **Inoperância:** tempo fora de operação (registrado em minutos, exibido em horas).
- **Locais / Sentido:** cadastro do equipamento (endereço e sentido da via).

## Arquivos-chave

| Arquivo | Papel |
|---|---|
| `dashboard.py` | Orquestra UI: página, filtros, chama componentes |
| `utils/data_loader.py` | Carrega/normaliza dados; constante `MESES`; `SPREADSHEET_ID` |
| `utils/components.py` | `render_metrics`, `render_impact_charts`, `render_monthly_history`, `render_analytical_table` |
| `.streamlit/config.toml` | Tema escuro global |
| `assets/styles.css` | CSS (cards, tabela, fonte Outfit) |
| CSVs `*_BD_Looker.csv` | Dados de CE por ano |
| `Controle_de_CE_-_locais.csv` | Cadastro de equipamentos |

## Decisões importantes (e porquês)

- **2024/2025 sempre locais; 2026 online com fallback.** → anos antigos são fechados; o ano ativo precisa estar atualizado, mas sem depender de internet.
- **Validação por nº de colunas (== 4).** → planilha Google privada retorna HTML de login que o Pandas lê sem erro; checar colunas detecta isso e aciona o CSV local.
- **IDs de equipamento limpos (sem `.0` e sem zeros à esquerda).** → necessário para o `merge` entre dados de CE e cadastro de locais funcionar.
- **CEs podem vir combinadas por `|`.** → sempre dividir/explodir antes de contar ou ranquear; contagem distinta por (CE + Ano). Isso vale nos **três** pontos: card de métrica, gráfico Top 10 e tabela analítica (helpers `_explodir_ces` / `_contar_ces_unicas` em `components.py`). No Top 10, as horas de um evento multi-CE são atribuídas integralmente a cada CE (sem rateio).
- **Sem banco de dados.** → volume pequeno e fluxo da equipe já é planilha.
- **Cache `ttl=600`.** → equilíbrio entre dados frescos e desempenho; há botão para forçar recarga.

## Convenções

- Idioma: **português do Brasil**; números formatados em padrão BR.
- Tema: fundo escuro `#0b0d10`, acento verde CET `#c8f050`, fonte `Outfit`.
- Executar **a partir da pasta `bd_ce`** (caminhos de CSV são relativos).
- CSV exportado em `utf-8-sig` (abre certo no Excel PT-BR).

## Pontos de atenção / dívidas conhecidas

- **Ano ativo fixo em "2026"** (texto e `TAB_2026`) — revisar na virada de ano.
- **Paleta de cores por ano** cobre só 2024–2026 — estender ao adicionar anos.
- **Requisito de compartilhamento** da planilha Google: "Qualquer pessoa com o link pode ler".
- `SPREADSHEET_ID` atual: `1b5Mv47_1BnW7yy7U2ijL46qo4vmEDIWNcI0DZiMOWZ0` (aba `BD_Looker`).
- **Segurança da tabela:** `to_html` em `render_analytical_table` escapa o conteúdo por padrão; **nunca** usar `escape=False`, pois os dados vêm de planilha pública.

## Revisão de código aplicada (2026-10-15)

- Caminhos de CSV e assets agora resolvidos via `Path(__file__)` (`BASE_DIR`) — roda de qualquer diretório.
- `key` do botão de download tornada estável (`"btn_export_csv"`), sem `uuid` aleatório por rerun.
- Top 10 CEs passou a explodir CEs combinadas (consistência entre painéis).
- Lógica de CE e layout de gráficos extraídos para helpers em `components.py` (fim da duplicação).
- Aviso na sidebar quando há datas inválidas; `requirements.txt` com versões mínimas fixadas.

## Como rodar

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## Documentos relacionados

- `prd.md` — requisitos de produto
- `arquitetura.md` — arquitetura técnica
- `regras.md` — regras de negócio e de dados
- `design.md` — identidade visual
- `tarefas.md` — feito + próximos passos
