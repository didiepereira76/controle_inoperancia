import os
import pandas as pd
import plotly.express as px
import streamlit as st

# Configuração da página - Ícone e Título
st.set_page_config(
    page_title="Controle de Inoperância de Radares",
    page_icon="radar_icon.png",
    layout="wide"
)

# Estilização CSS Avançada - Glassmorphism, Outfit Font, Hover Animations e Tema Escuro
st.markdown("""
<style>
    /* Importação de fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0b0d10 !important;
        color: #e2e8f0 !important;
    }
    
    /* Remover espaço excessivo no topo */
    .block-container { 
        padding-top: 2rem !important; 
        padding-bottom: 2rem !important;
    }
    
    /* Título principal estilizado */
    .dashboard-title {
        color: #c8f050;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: left;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    .dashboard-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        text-align: left;
        margin-bottom: 0rem;
        font-weight: 400;
    }
    
    /* Cartões de Métrica Premium com Efeito Glassmorphism e Glow no Hover */
    .metric-card {
        background: rgba(17, 24, 39, 0.5);
        border: 1px solid rgba(200, 240, 80, 0.15);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(200, 240, 80, 0.4);
        box-shadow: 0 10px 30px rgba(200, 240, 80, 0.12);
        background: rgba(17, 24, 39, 0.75);
    }
    .metric-label { 
        color: #94a3b8; 
        font-size: 0.85rem; 
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
        margin-bottom: 6px; 
    }
    .metric-value { 
        color: #c8f050; 
        font-size: 2.25rem; 
        font-weight: 700; 
        text-shadow: 0 2px 10px rgba(200, 240, 80, 0.15);
    }
    
    /* Seletores da barra lateral e filtros */
    .stSelectbox label, .stMultiSelect label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    /* Contraste dos badges de seleção (Texto preto sobre o verde CET) */
    span[data-baseweb="tag"],
    span[data-baseweb="tag"] span, 
    span[data-baseweb="tag"] svg,
    span[data-baseweb="tag"] button,
    div[data-baseweb="tag"],
    div[data-baseweb="tag"] span,
    div[data-baseweb="tag"] svg,
    div[data-baseweb="tag"] button {
        color: #0b0d10 !important;
        fill: #0b0d10 !important;
    }
    
    /* Separadores de seção modernos */
    hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    /* Tabela Premium customizada (Hover highlight) */
    .premium-table-container {
        max-height: 450px;
        overflow-y: auto;
        border-radius: 12px;
        border: 1px solid rgba(200, 240, 80, 0.15);
        background: rgba(17, 24, 39, 0.5);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }
    .premium-table-container::-webkit-scrollbar { width: 8px; }
    .premium-table-container::-webkit-scrollbar-track { background: transparent; }
    .premium-table-container::-webkit-scrollbar-thumb {
        background: rgba(200, 240, 80, 0.3);
        border-radius: 8px;
    }
    .premium-table-container::-webkit-scrollbar-thumb:hover { background: rgba(200, 240, 80, 0.6); }
    
    .premium-table {
        width: 100%;
        border-collapse: collapse;
        color: #e2e8f0;
        font-size: 0.95rem;
        text-align: left;
    }
    .premium-table thead th {
        position: sticky;
        top: 0;
        background: rgba(11, 13, 16, 0.98);
        color: #94a3b8;
        padding: 1rem 1.25rem;
        font-weight: 600;
        border-bottom: 1px solid rgba(200, 240, 80, 0.3);
        z-index: 1;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.85rem;
    }
    .premium-table tbody tr {
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        background-color: transparent;
    }
    .premium-table tbody tr:last-child {
        border-bottom: none;
    }
    .premium-table tbody tr:hover {
        background-color: rgba(200, 240, 80, 0.12) !important;
        transform: translateX(4px);
        box-shadow: inset 3px 0 0 0 #c8f050;
    }
    .premium-table tbody td {
        padding: 1rem 1.25rem;
        vertical-align: middle;
        transition: color 0.25s ease;
    }
    .premium-table tbody tr:hover td {
        color: #c8f050;
    }
</style>
""", unsafe_allow_html=True)


# Configuração para carregar o ano atual (2026) diretamente do Google Planilhas (Opcional)
# Caso queira integrar online para o ano ativo, insira o ID da sua planilha abaixo.
# Exemplo: SPREADSHEET_ID = "1A2B3C4D..."
# Deixe em branco "" para ler o arquivo CSV local de 2026.
SPREADSHEET_ID = "1b5Mv47_1BnW7yy7U2ijL46qo4vmEDIWNcI0DZiMOWZ0"

# Se a planilha online for usada, defina o nome exato da aba para os dados de 2026
TAB_2026 = "BD_Looker"


# Carregamento de Dados com Caching e suporte híbrido (Apenas 2026 pode ser online)
# ttl=600 garante que se a planilha online for usada, ela se auto-atualizará a cada 10 minutos
@st.cache_data(ttl=600)
def carregar_dados_sistema():
    # Anos anteriores (2024 e 2025) são sempre carregados localmente (dados estáticos)
    df24 = pd.read_csv("Controle_de_CE_2024_-_BD_Looker.csv", encoding="utf-8")
    df25 = pd.read_csv("Controle_de_CE_2025_-_BD_Looker.csv", encoding="utf-8")
    df24.columns = ["Data", "Equipamento", "Numero_CE", "Inoperancia_Minutos"]
    df25.columns = ["Data", "Equipamento", "Numero_CE", "Inoperancia_Minutos"]
    df24["Ano"] = 2024
    df25["Ano"] = 2025
    
    # Carrega dados do ano atual (2026)
    if SPREADSHEET_ID:
        try:
            url_26 = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={TAB_2026}"
            df26 = pd.read_csv(url_26, encoding="utf-8")
            # Validação crítica: se a planilha do Google não estiver compartilhada publicamente,
            # a requisição retorna a página HTML de login do Google. O Pandas lê a página sem gerar erro,
            # mas o DataFrame resultante tem um formato incorreto (geralmente dezenas de colunas vazias).
            # Um arquivo correto de CE deve ter exatamente 4 colunas de dados.
            if len(df26.columns) != 4:
                raise ValueError("Formato de colunas incorreto. Planilha possivelmente privada.")
            df26.columns = ["Data", "Equipamento", "Numero_CE", "Inoperancia_Minutos"]
            st.sidebar.success("⚡ Dados de 2026 carregados online da Planilha Google!")
        except Exception as e:
            st.sidebar.warning("⚠️ Não foi possível carregar 2026 online (verifique se a planilha está compartilhada para 'Qualquer pessoa com o link' ler). Carregando arquivo local.")
            df26 = pd.read_csv("Controle_de_CE_2026_-_BD_Looker.csv", encoding="utf-8")
            df26.columns = ["Data", "Equipamento", "Numero_CE", "Inoperancia_Minutos"]
    else:
        df26 = pd.read_csv("Controle_de_CE_2026_-_BD_Looker.csv", encoding="utf-8")
        df26.columns = ["Data", "Equipamento", "Numero_CE", "Inoperancia_Minutos"]
        
    df26["Ano"] = 2026
    
    df = pd.concat([df24, df25, df26], ignore_index=True)
    df.columns = ["Data", "Equipamento", "Numero_CE", "Inoperancia_Minutos", "Ano"]
    
    # Carregamento de locais sempre local (dados estáticos de cadastro)
    locais = pd.read_csv("Controle_de_CE_-_locais.csv", encoding="utf-8")
    locais.columns = ["Serie", "Locais", "Sentido"]

        
    # Processamento e Limpeza Compartilhada
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")
    
    # IMPORTANTE: Alinha o ano da Data com o Ano correspondente do arquivo de origem
    df["Data"] = df.apply(
        lambda row: row["Data"].replace(year=row["Ano"]) if pd.notna(row["Data"]) else row["Data"], 
        axis=1
    )
    
    # IMPORTANTE: Filtra datas no futuro (evita exibir dados futuros para o ano corrente)
    df = df[df["Data"].isna() | (df["Data"] <= pd.Timestamp.now())]
    
    df["Mes"] = df["Data"].dt.month
    df["Inoperancia_Horas"] = df["Inoperancia_Minutos"] / 60
    
    # Limpeza preventiva dos IDs de equipamento (remove decimais indesejados e zeros à esquerda)
    df["Equipamento"] = df["Equipamento"].astype(str).str.split('.').str[0].str.lstrip("0")
    
    locais["Serie"] = locais["Serie"].astype(str).str.split('.').str[0].str.lstrip("0")
    
    # Tratamento de quebras de linha nas colunas do cadastro de locais (melhora visual de tabelas/selectboxes)
    locais["Locais"] = locais["Locais"].astype(str).str.replace(r'\r?\n', ' / ', regex=True).str.strip()
    locais["Sentido"] = locais["Sentido"].astype(str).str.replace(r'\r?\n', ' / ', regex=True).str.strip()
    
    # Mesclar dados de CE com as informações cadastrais de locais
    df = df.merge(locais, left_on="Equipamento", right_on="Serie", how="left")
    
    # Preencher valores nulos caso algum equipamento não esteja cadastrado na planilha Controle_de_CE_-_locais.csv
    df["Locais"] = df["Locais"].fillna("Não Cadastrado")
    df["Sentido"] = df["Sentido"].fillna("Não Cadastrado")
    
    # Garante string no Equipamento após merge
    df["Equipamento"] = df["Equipamento"].astype(str)
    return df


df = carregar_dados_sistema()

MESES = {1:"jan", 2:"fev", 3:"mar", 4:"abr", 5:"mai", 6:"jun",
         7:"jul", 8:"ago", 9:"set", 10:"out", 11:"nov", 12:"dez"}

# Cabeçalho da página com logotipo alinhado à esquerda
col_logo, col_title = st.columns([1, 15])
with col_logo:
    # Ajuste de espaçamento vertical para centralizar o logotipo com o título
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    st.image("radar_icon.png", width=64)
with col_title:
    st.markdown("<h1 class='dashboard-title'>Controle de Inoperância de Radares</h1>", unsafe_allow_html=True)
    st.markdown("<p class='dashboard-subtitle'>Santos/SP - Painel Inteligente de Monitoramento e Manutenção de Equipamentos</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Bloco de Filtros
col1, col2, col3 = st.columns(3)
with col1:
    anos = sorted(df["Ano"].unique().tolist())
    ano_sel = st.multiselect("Ano", anos, default=anos)
with col2:
    # UX aprimorada: mapeamento do seletor de equipamentos mostrando também o endereço
    df_equip_map = df[df["Ano"].isin(ano_sel)][["Equipamento", "Locais"]].drop_duplicates().sort_values("Equipamento")
    df_equip_map["Exibicao"] = df_equip_map["Equipamento"] + " - " + df_equip_map["Locais"]
    equipamentos = ["Todos"] + df_equip_map["Exibicao"].tolist()
    equip_sel = st.selectbox("Equipamento", equipamentos)
with col3:
    # Mostra o sentido como suporte/informação do equipamento selecionado (estilizado como input desabilitado para manter o alinhamento nativo)
    if equip_sel != "Todos":
        equip_code = equip_sel.split(" - ")[0]
        sentidos_eq = df[df["Equipamento"] == equip_code]["Sentido"].dropna().unique()
        sentido_str = sentidos_eq[0] if len(sentidos_eq) > 0 else "Não Cadastrado"
    else:
        sentido_str = "Todos"
    
    st.text_input("Sentido do Equipamento", value=sentido_str, disabled=True)



# Processa filtros
dff = df[df["Ano"].isin(ano_sel)].copy()

if equip_sel != "Todos":
    # Extrai o ID numérico do equipamento da string combinada "Código - Local"
    equip_code = equip_sel.split(" - ")[0]
    dff = dff[dff["Equipamento"] == equip_code]


st.markdown("<hr>", unsafe_allow_html=True)

# Cálculo de Métricas com correções
c1, c2, c3, c4 = st.columns(4)

# Correção na contagem de CEs: trata corretamente valores agrupados por pipe (ex: "CE: 09 | CE: 10")
all_ces = dff["Numero_CE"].dropna().str.split(r'\s*\|\s*').explode().str.strip().unique()
total_ce = len([ce for ce in all_ces if ce])

total_horas = dff["Inoperancia_Horas"].sum()
total_equip = dff["Equipamento"].nunique()
media_horas = dff["Inoperancia_Horas"].mean() if len(dff) > 0 else 0

with c1:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Número(s) CE</div>
        <div class='metric-value'>{total_ce}</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Inoperância Acumulada</div>
        <div class='metric-value'>{total_horas:,.0f}h</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Equipamentos Afetados</div>
        <div class='metric-value'>{total_equip}</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Média Horas / Ocorrência</div>
        <div class='metric-value'>{media_horas:.1f}h</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("#### ⏳ CEs com maior impacto (Top 10)")
    ce_group = (dff.groupby("Numero_CE")["Inoperancia_Horas"]
                .sum().sort_values(ascending=True).tail(10).reset_index())
    fig_ce = px.bar(ce_group, x="Inoperancia_Horas", y="Numero_CE",
                    orientation="h", text="Inoperancia_Horas",
                    color_discrete_sequence=["#c8f050"],
                    labels={"Inoperancia_Horas": "Inoperância em Horas", "Numero_CE": "Número de CE's"})
    
    # Customização visual do gráfico (bordas arredondadas, fundo transparente, tooltip premium)
    fig_ce.update_traces(
        texttemplate="%{text:.1f}h", 
        textposition="outside",
        hovertemplate="<b>%{y}</b><br><b>Inoperância:</b> %{x:.1f} horas<extra></extra>",
        marker=dict(cornerradius=6)
    )
    fig_ce.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#cbd5e1", 
        margin=dict(l=10, r=40, t=10, b=10),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False), 
        height=360
    )
    st.plotly_chart(fig_ce, width="stretch", config={'displayModeBar': False})

with col_b:
    st.markdown("#### 🚦 Ranking de Equipamentos mais Inoperantes")
    eq_group = (dff.groupby("Equipamento")["Inoperancia_Horas"]
                .sum().sort_values(ascending=False).head(10).reset_index())
    eq_group["Equipamento"] = eq_group["Equipamento"].astype(str)
    fig_eq = px.bar(eq_group, x="Equipamento", y="Inoperancia_Horas",
                    text="Inoperancia_Horas",
                    color_discrete_sequence=["#c8f050"],
                    labels={"Inoperancia_Horas": "Inoperância em Horas"})
    
    # Customização visual (bordas arredondadas, fundo transparente, tooltip premium)
    fig_eq.update_traces(
        texttemplate="%{text:.0f}h", 
        textposition="outside",
        hovertemplate="<b>Radar Série:</b> %{x}<br><b>Total Inoperância:</b> %{y:.1f} horas<extra></extra>",
        marker=dict(cornerradius=6)
    )
    fig_eq.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#cbd5e1", 
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(showgrid=False, type="category"),
        yaxis=dict(showgrid=False, showticklabels=False),
        height=360
    )
    st.plotly_chart(fig_eq, width="stretch", config={'displayModeBar': False})

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("#### 📅 Histórico de Inoperância por Mês")
mes_group = (dff.groupby(["Ano", "Mes"])["Inoperancia_Horas"]
             .sum().reset_index())
mes_group["Mês Nome"] = mes_group["Mes"].map(MESES)
mes_group["Período"] = mes_group["Mês Nome"] + "/" + mes_group["Ano"].astype(str).str[-2:]
mes_group = mes_group.sort_values(["Ano", "Mes"])
mes_group["Ano"] = mes_group["Ano"].astype(str)

# Paleta de verde moderno em degradê para os anos
fig_mes = px.bar(mes_group, x="Período", y="Inoperancia_Horas",
                 color="Ano", barmode="group",
                 color_discrete_map={"2024": "#c8f050", "2025": "#84cc16", "2026": "#10b981"},
                 text="Inoperancia_Horas",
                 custom_data=["Ano"],
                 labels={"Inoperancia_Horas": "Inoperância em Horas"})

fig_mes.update_traces(
    texttemplate="%{text:.0f}h", 
    textposition="outside",
    hovertemplate="<b>Mês:</b> %{x}<br><b>Ano:</b> %{customdata[0]}<br><b>Inoperância:</b> %{y:.1f} horas<extra></extra>",
    marker=dict(cornerradius=6)
)
fig_mes.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", 
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#cbd5e1", 
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(showgrid=False, type="category"),
    yaxis=dict(showgrid=False, showticklabels=False),
    legend=dict(
        bgcolor="rgba(17, 24, 39, 0.6)", 
        title="Ano",
        font=dict(color="#cbd5e1")
    ),
    height=320
)
st.plotly_chart(fig_mes, width="stretch", config={'displayModeBar': False})

st.markdown("<hr>", unsafe_allow_html=True)

# Seção de Detalhes por Equipamento com opção de exportação dos dados
st.markdown("#### 📋 Detalhe Analítico por Equipamento")

# Agregação precisa tratando CEs combinados
nunique_ces = lambda x: len(x.dropna().str.split(r'\s*\|\s*').explode().str.strip().unique())

tabela = (dff.groupby(["Equipamento", "Locais", "Sentido"])
          .agg(CEs=("Numero_CE", nunique_ces), Horas=("Inoperancia_Horas", "sum"))
          .reset_index().sort_values("Horas", ascending=False)
          .rename(columns={"Equipamento": "Série", "Locais": "Local", "Horas": "Inoperância em Horas", "CEs": "Número de CE's"}))
tabela["Inoperância em Horas"] = tabela["Inoperância em Horas"].round(1)

# Exibe tabela analítica com HTML customizado para o hover dinâmico
html_table = tabela.to_html(classes="premium-table", index=False, border=0, justify="left")
st.markdown(f'<div class="premium-table-container">{html_table}</div><br>', unsafe_allow_html=True)

# Botão de exportação
csv_buffer = tabela.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 Exportar Tabela Analítica (CSV)",
    data=csv_buffer,
    file_name=f"inoperancia_radares_filtrado.csv",
    mime="text/csv"
)
