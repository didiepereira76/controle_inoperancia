# 📊 Controle de Inoperância de Radares - Guia de Execução

Este guia contém o passo a passo para configurar e executar o dashboard de monitoramento de radares em qualquer outro computador.

---

## 📂 Arquivos Necessários
Copie a pasta inteira do projeto contendo os seguintes arquivos:
*   `dashboard.py` - Código principal da aplicação Streamlit.
*   `requirements.txt` - Arquivo com as bibliotecas que devem ser instaladas.
*   `radar_icon.png` - Logotipo/ícone personalizado do radar.
*   `.streamlit/config.toml` - Configuração do tema escuro global.
*   **Dados Estáticos (CSVs Locais):**
    *   `Controle_de_CE_2024_-_BD_Looker.csv`
    *   `Controle_de_CE_2025_-_BD_Looker.csv`
    *   `Controle_de_CE_2026_-_BD_Looker.csv`
    *   `Controle_de_CE_-_locais.csv`

---

## 🛠️ Passo a Passo para Configuração

### Passo 1: Instalar o Python
Certifique-se de que o computador de destino possui o Python instalado (versão **3.8** ou superior).
*   **Download:** [python.org/downloads](https://www.python.org/downloads/)
*   *Nota no Windows:* Durante a instalação, marque a caixinha **"Add Python to PATH"** (Adicionar Python ao PATH).

### Passo 2: Instalar as Dependências (Bibliotecas)
1. Abra o terminal do sistema (Prompt de Comando ou PowerShell no Windows, ou Terminal no macOS/Linux).
2. Navegue até a pasta do projeto (ou abra o terminal diretamente a partir dela).
3. Execute o comando abaixo para instalar de uma só vez as bibliotecas necessárias (Pandas, Plotly e Streamlit):
   ```bash
   pip install -r requirements.txt
   ```

### Passo 3: Executar o Dashboard
Com as bibliotecas instaladas, execute o comando abaixo no terminal:
```bash
streamlit run dashboard.py
```
O Streamlit iniciará um servidor local e abrirá automaticamente o painel estilizado no seu navegador de internet padrão.

---

## 🌐 Integração com o Google Planilhas (Online)
O dashboard está programado para buscar as informações do ano atual (**2026**) diretamente online. 

### Como funciona:
*   O ID da planilha de 2026 está definido no topo do arquivo `dashboard.py`:
    ```python
    SPREADSHEET_ID = "1b5Mv47_1BnW7yy7U2ijL46qo4vmEDIWNcI0DZiMOWZ0"
    ```
*   A aplicação consome a aba nomeada especificamente como **`BD_Looker`**.
*   **Requisito de Compartilhamento:** A planilha no Google Drive precisa estar com a permissão definida para **"Qualquer pessoa com o link pode ler (Leitor)"**. 
*   **Fallback Automático:** Caso o computador esteja sem internet ou a planilha esteja privada, o painel exibirá um alerta na barra lateral e carregará os dados locais salvos no arquivo `Controle_de_CE_2026_-_BD_Looker.csv` automaticamente, sem quebrar ou parar o sistema.
