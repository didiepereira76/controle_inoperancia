# Arquitetura — Controle de Inoperância de Radares

> Descrição da arquitetura real do sistema já construído.

## 1. Stack

- **Linguagem:** Python 3.8+
- **Framework de UI:** Streamlit
- **Dados:** Pandas
- **Gráficos:** Plotly Express
- **Fontes:** CSV local + Google Planilhas (via endpoint `gviz/tq` em CSV)

Dependências (`requirements.txt`): `pandas`, `plotly`, `streamlit`.

## 2. Estrutura de pastas

```
bd_ce/
├── dashboard.py                 # Ponto de entrada / orquestração da UI
├── requirements.txt             # Dependências
├── radar_icon.png               # Ícone/logotipo
├── README.md                    # Guia de instalação e execução
├── .streamlit/
│   └── config.toml              # Tema escuro global do Streamlit
├── assets/
│   └── styles.css               # CSS customizado (cards, tabela, tema)
├── utils/
│   ├── data_loader.py           # Carga, limpeza e junção dos dados
│   └── components.py            # Componentes visuais (métricas, gráficos, tabela)
└── dados (CSV):
    ├── Controle_de_CE_2024_-_BD_Looker.csv
    ├── Controle_de_CE_2025_-_BD_Looker.csv
    ├── Controle_de_CE_2026_-_BD_Looker.csv   # fallback do ano ativo
    └── Controle_de_CE_-_locais.csv           # cadastro de equipamentos
```

## 3. Camadas

O projeto segue uma separação simples em três camadas:

1. **Orquestração / UI (`dashboard.py`)**
   - Configura página e tema, carrega CSS.
   - Monta cabeçalho, filtros e chama os componentes na ordem da tela.
   - Aplica os filtros ao DataFrame antes de repassar aos componentes.

2. **Dados (`utils/data_loader.py`)**
   - `carregar_dados_sistema()` — função única, cacheada (`@st.cache_data(ttl=600)`), que:
     - Lê 2024 e 2025 de CSV local.
     - Lê 2026 do Google Sheets (com validação) ou cai para CSV local.
     - Normaliza colunas, trata datas, deriva mês e horas.
     - Limpa IDs de equipamento e faz `merge` com o cadastro de locais.
   - Exporta a constante `MESES` (mapa número → nome abreviado).

3. **Componentes (`utils/components.py`)**
   - `render_metrics(dff)` — cards de métricas.
   - `render_impact_charts(dff)` — Top 10 CEs + ranking de equipamentos.
   - `render_monthly_history(dff, meses_dict)` — histórico mensal por ano.
   - `render_analytical_table(dff)` — tabela analítica + exportação CSV.

## 4. Fluxo de dados

```
CSV 2024/2025 (local) ─┐
Google Sheets 2026 ────┼─► concat ─► normaliza ─► merge(locais) ─► df
CSV 2026 (fallback) ───┘                                            │
Cadastro locais (CSV) ──────────────────────────────────────────────┘
                                                                     │
                          dashboard.py aplica filtros (ano, equip)  ─► dff
                                                                     │
                     render_metrics / impact_charts / monthly / table
```

## 5. Integração com Google Planilhas

- URL consumida:
  `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={TAB_2026}&_t={timestamp}`
- `SPREADSHEET_ID` e `TAB_2026` ficam no topo de `utils/data_loader.py`.
- O `timestamp` evita cache do lado do Google.
- **Validação crítica:** se a planilha estiver privada, o Google devolve HTML de login; o Pandas lê sem erro mas gera colunas demais. Por isso valida-se `len(df26.columns) != 4` → dispara fallback.
- **Requisito:** a planilha precisa estar como "Qualquer pessoa com o link pode ler".

## 6. Cache e atualização

- `@st.cache_data(ttl=600)` → recarrega a cada 10 minutos.
- Botão **"🔄 Atualizar Dados da Planilha"** chama `st.cache_data.clear()` + `st.rerun()` para forçar recarga imediata.

## 7. Configuração / tema

- `.streamlit/config.toml` define o tema global (fundo escuro, cor primária verde `#c8f050`).
- `assets/styles.css` sobrepõe estilos para cards (glassmorphism), tabela premium e tipografia (fonte `Outfit`).

## 8. Execução

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

> **Importante:** os caminhos dos CSVs são relativos, então a aplicação deve ser executada **a partir da pasta do projeto** (`bd_ce`).

## 9. Decisões de arquitetura (e porquês)

- **Sem banco de dados:** os volumes são pequenos e a fonte natural já é planilha; CSV/Sheets mantém o fluxo de trabalho existente da equipe.
- **Híbrido online/offline:** o ano ativo precisa estar sempre atualizado (online), mas o sistema não pode depender de conectividade → fallback local.
- **Modularização (`utils/`):** separar carga de dados dos componentes visuais facilita manutenção e teste visual isolado.
- **CSS externo:** manter o visual fora do `dashboard.py` deixa o código de orquestração limpo.
