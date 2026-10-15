from pathlib import Path

import pandas as pd
import streamlit as st

# Diretório raiz do projeto (bd_ce/), para que os CSVs sejam encontrados
# independentemente de qual pasta a aplicação foi iniciada.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuração para carregar o ano atual (2026) diretamente do Google Planilhas (Opcional)
# Caso queira integrar online para o ano ativo, insira o ID da sua planilha abaixo.
# Deixe em branco "" para ler o arquivo CSV local de 2026.
SPREADSHEET_ID = "1b5Mv47_1BnW7yy7U2ijL46qo4vmEDIWNcI0DZiMOWZ0"

# Se a planilha online for usada, defina o nome exato da aba para os dados de 2026
TAB_2026 = "BD_Looker"

# Dicionário de meses para exibição amigável
MESES = {
    1: "jan", 2: "fev", 3: "mar", 4: "abr", 5: "mai", 6: "jun",
    7: "jul", 8: "ago", 9: "set", 10: "out", 11: "nov", 12: "dez"
}


def _limpar_id(serie):
    """Normaliza IDs de equipamento/série: remove parte decimal e zeros à
    esquerda, evitando que um ID que seja só zeros vire string vazia."""
    s = serie.astype(str).str.split('.').str[0].str.lstrip("0")
    return s.replace("", "0")

# Carregamento de Dados com Caching e suporte híbrido (Apenas 2026 pode ser online)
# ttl=600 garante que se a planilha online for usada, ela se auto-atualizará a cada 10 minutos
@st.cache_data(ttl=600)
def carregar_dados_sistema():
    # Anos anteriores (2024 e 2025) são sempre carregados localmente (dados estáticos)
    df24 = pd.read_csv(BASE_DIR / "Controle_de_CE_2024_-_BD_Looker.csv", encoding="utf-8")
    df25 = pd.read_csv(BASE_DIR / "Controle_de_CE_2025_-_BD_Looker.csv", encoding="utf-8")
    df24.columns = ["Data", "Equipamento", "Numero_CE", "Inoperancia_Minutos"]
    df25.columns = ["Data", "Equipamento", "Numero_CE", "Inoperancia_Minutos"]
    df24["Ano"] = 2024
    df25["Ano"] = 2025
    
    # Carrega dados do ano atual (2026)
    if SPREADSHEET_ID:
        try:
            import time
            timestamp = int(time.time())
            url_26 = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={TAB_2026}&_t={timestamp}"
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
            df26 = pd.read_csv(BASE_DIR / "Controle_de_CE_2026_-_BD_Looker.csv", encoding="utf-8")
            df26.columns = ["Data", "Equipamento", "Numero_CE", "Inoperancia_Minutos"]
    else:
        df26 = pd.read_csv(BASE_DIR / "Controle_de_CE_2026_-_BD_Looker.csv", encoding="utf-8")
        df26.columns = ["Data", "Equipamento", "Numero_CE", "Inoperancia_Minutos"]
        
    df26["Ano"] = 2026

    df = pd.concat([df24, df25, df26], ignore_index=True)

    # Carregamento de locais sempre local (dados estáticos de cadastro)
    locais = pd.read_csv(BASE_DIR / "Controle_de_CE_-_locais.csv", encoding="utf-8")
    locais.columns = ["Serie", "Locais", "Sentido"]

    # Tratamento da data
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")

    # Avisa quando há datas que não puderam ser interpretadas (ficam de fora do histórico mensal)
    qtd_datas_invalidas = int(df["Data"].isna().sum())
    if qtd_datas_invalidas:
        st.sidebar.info(f"ℹ️ {qtd_datas_invalidas} registro(s) com data inválida foram ignorados no histórico mensal.")

    df["Mes"] = df["Data"].dt.month
    df["Inoperancia_Horas"] = df["Inoperancia_Minutos"] / 60

    # Limpeza preventiva dos IDs de equipamento (remove decimais indesejados e zeros à esquerda)
    df["Equipamento"] = _limpar_id(df["Equipamento"])
    locais["Serie"] = _limpar_id(locais["Serie"])

    # Tratamento de quebras de linha nas colunas do cadastro de locais (melhora visual de tabelas/selectboxes)
    locais["Locais"] = locais["Locais"].astype(str).str.replace(r'\r?\n', ' / ', regex=True).str.strip()
    locais["Sentido"] = locais["Sentido"].astype(str).str.replace(r'\r?\n', ' / ', regex=True).str.strip()
    
    # Mesclar dados de CE com as informações cadastrais de locais
    # (descarta a coluna "Serie" duplicada após o merge)
    df = df.merge(locais, left_on="Equipamento", right_on="Serie", how="left").drop(columns="Serie")

    # Preencher valores nulos caso algum equipamento não esteja cadastrado na planilha Controle_de_CE_-_locais.csv
    df["Locais"] = df["Locais"].fillna("Não Cadastrado")
    df["Sentido"] = df["Sentido"].fillna("Não Cadastrado")

    return df
