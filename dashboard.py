import os
import pandas as pd
import streamlit as st
from utils.data_loader import carregar_dados_sistema, MESES
from utils.components import (
    render_metrics,
    render_impact_charts,
    render_monthly_history,
    render_analytical_table
)

# Configuração da página - Ícone e Título
st.set_page_config(
    page_title="Controle de Inoperância de Radares",
    page_icon="radar_icon.png",
    layout="wide"
)

# Estilização CSS Avançada - Carregada do arquivo modularizado
if os.path.exists("assets/styles.css"):
    with open("assets/styles.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carrega a base de dados
df = carregar_dados_sistema()

# Cabeçalho da página com logotipo alinhado à esquerda
col_logo, col_title = st.columns([1, 15])
with col_logo:
    # Ajuste de espaçamento vertical para centralizar o logotipo com o título
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    st.image("radar_icon.png", width=64)
with col_title:
    st.markdown("<h1 class='dashboard-title'>Controle de Inoperância de Radares</h1>", unsafe_allow_html=True)
    st.markdown("<p class='dashboard-subtitle'>GTSV - Gerência de Tecnologia em Sistema Viário</p>", unsafe_allow_html=True)
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

# 1. Métricas principais
render_metrics(dff)

st.markdown("<br>", unsafe_allow_html=True)

# 2. Gráficos de impacto (Top 10 CEs e Ranking de Equipamentos)
render_impact_charts(dff)

st.markdown("<hr>", unsafe_allow_html=True)

# 3. Histórico Mensal
render_monthly_history(dff, MESES)

st.markdown("<hr>", unsafe_allow_html=True)

# 4. Detalhes analíticos e Exportação em Tabela
render_analytical_table(dff)
