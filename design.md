# Design e Identidade Visual

> Diretrizes visuais efetivamente aplicadas (ver `.streamlit/config.toml` e `assets/styles.css`).

## 1. Conceito

Tema **escuro premium** com acento verde (identidade CET), efeitos de *glassmorphism* nos cards e realces suaves no hover. Layout em largura total (`layout="wide"`).

## 2. Paleta de cores

| Uso | Cor | Hex |
|---|---|---|
| Fundo principal | preto azulado | `#0b0d10` |
| Fundo secundário (cards/painéis) | cinza-azulado | `#111827` / `rgba(17,24,39,0.5)` |
| Cor primária / acento | verde CET | `#c8f050` |
| Texto principal | quase branco | `#e2e8f0` |
| Texto secundário / labels | cinza | `#94a3b8` |
| Texto de gráficos | cinza claro | `#cbd5e1` |

Gradiente de verde usado no histórico mensal por ano:

| Ano | Cor |
|---|---|
| 2024 | `#c8f050` |
| 2025 | `#84cc16` |
| 2026 | `#10b981` |

## 3. Tipografia

- Fonte principal: **Outfit** (Google Fonts), pesos 300–700.
- Fallback: `sans-serif`.
- Título do dashboard: 2.5rem, peso 700, cor verde, alinhado à esquerda.
- Subtítulo: 1.05rem, cinza (`#94a3b8`).
- Labels de métrica: maiúsculas, `letter-spacing` 1.2px, peso 600.

## 4. Componentes visuais

### Cabeçalho
- Ícone `radar_icon.png` (64px) à esquerda + título e subtítulo "GTSV - Gerência de Tecnologia em Sistema Viário".
- Separadores `<hr>` com borda translúcida entre seções.

### Cards de métrica (`.metric-card`)
- Fundo translúcido + `backdrop-filter: blur(10px)` (glassmorphism).
- Borda verde sutil; `border-radius` 12px.
- **Hover:** eleva (`translateY(-4px)`), intensifica borda e sombra com *glow* verde.
- Valor em verde, 2.25rem, com leve `text-shadow`.

### Gráficos (Plotly)
- Fundo transparente (`paper_bgcolor` e `plot_bgcolor` em `rgba(0,0,0,0)`).
- Barras verdes com `cornerradius: 6` (cantos arredondados).
- Eixos sem grade; rótulos de valor externos às barras (ex.: `120h`).
- Tooltips customizados (`hovertemplate`) com rótulos em negrito.
- Barra de ferramentas do Plotly oculta (`displayModeBar: False`).
- Gráficos horizontais para CEs (facilita leitura de rótulos longos) e verticais para equipamentos/meses.

### Tabela premium (`.premium-table`)
- Container com rolagem (`max-height: 450px`), borda verde e cantos arredondados.
- Cabeçalho fixo (`sticky`) em maiúsculas.
- **Hover na linha:** destaque verde translúcido, leve deslize (`translateX(4px)`), barra verde à esquerda e texto em verde.
- Scrollbar customizada em verde.

## 5. Padrões de UX

- **Filtro de equipamento mostra o endereço** junto ao código, facilitando a identificação.
- **Sentido** aparece como campo desabilitado para manter alinhamento visual com os demais filtros, sem permitir edição.
- **Feedback de origem dos dados** na barra lateral: mensagem de sucesso (online) ou aviso (fallback local).
- **Botão de atualização** sempre visível na sidebar.
- **Formatação numérica brasileira** em todos os indicadores.

## 6. Ícones (emoji) por seção

| Seção | Ícone |
|---|---|
| Atualizar dados | 🔄 |
| Top 10 CEs | ⏳ |
| Ranking de equipamentos | 🚦 |
| Histórico mensal | 📅 |
| Tabela analítica | 📋 |
| Exportar CSV | 📥 |

## 7. Responsividade / layout

- Grid do Streamlit em colunas: filtros em 3 colunas; métricas em 4; gráficos de impacto em 2.
- Layout `wide` para aproveitar telas largas (uso em desktop).
