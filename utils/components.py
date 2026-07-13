import streamlit as st
import plotly.express as px
import pandas as pd

def render_metrics(dff):
    """
    Calcula e renderiza os cartões de métricas premium na tela.
    """
    # Correção na contagem de CEs: trata corretamente valores agrupados por pipe (ex: "CE: 09 | CE: 10")
    all_ces = dff["Numero_CE"].dropna().str.split(r'\s*\|\s*').explode().str.strip().unique()
    total_ce = len([ce for ce in all_ces if ce])
    
    total_horas = dff["Inoperancia_Horas"].sum()
    total_equip = dff["Equipamento"].nunique()
    media_horas = dff["Inoperancia_Horas"].mean() if len(dff) > 0 else 0
    
    # Formatação de números no padrão brasileiro
    total_horas_fmt = f"{total_horas:,.0f}".replace(",", ".")
    media_horas_fmt = f"{media_horas:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Número CE'S</div>
            <div class='metric-value'>{total_ce}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Inoperância Acumulada</div>
            <div class='metric-value'>{total_horas_fmt}h</div>
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
            <div class='metric-value'>{media_horas_fmt}h</div>
        </div>
        """, unsafe_allow_html=True)

def render_impact_charts(dff):
    """
    Gera e renderiza a seção contendo os gráficos do Top 10 CEs e Ranking de Equipamentos.
    """
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

def render_monthly_history(dff, meses_dict):
    """
    Gera e exibe o gráfico de histórico de inoperância agrupado por ano/mês.
    """
    st.markdown("#### 📅 Histórico de Inoperância por Mês")
    mes_group = (dff.groupby(["Ano", "Mes"])["Inoperancia_Horas"]
                 .sum().reset_index())
    mes_group["Mês Nome"] = mes_group["Mes"].map(meses_dict)
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

def render_analytical_table(dff):
    """
    Renderiza a tabela analítica interativa e o botão para exportação em CSV.
    """
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
        file_name="inoperancia_radares_filtrado.csv",
        mime="text/csv"
    )
