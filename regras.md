# Regras de Negócio e de Dados

> Regras efetivamente implementadas no código (principalmente em `utils/data_loader.py` e `utils/components.py`).

## 1. Conceitos

- **CE (Comunicado de Evento):** registro de uma ocorrência de inoperância de um radar. Identificado por um número (ex.: `CE: 009`).
- **Equipamento / Série:** o radar, identificado por um código numérico (ex.: `337`).
- **Inoperância:** tempo em que o radar ficou fora de operação, registrado em **minutos** e convertido para **horas** na análise.
- **Local / Sentido:** dados cadastrais do equipamento (endereço e sentido da via).

## 2. Fontes por ano

| Ano | Fonte | Observação |
|---|---|---|
| 2024 | CSV local | Sempre estático (histórico) |
| 2025 | CSV local | Sempre estático (histórico) |
| 2026 | Google Sheets (aba `BD_Looker`) | Ano ativo; cai para CSV local se indisponível |

**Regra:** anos anteriores nunca são buscados online — são dados fechados. Apenas o ano ativo (2026) é dinâmico.

## 3. Estrutura esperada dos dados de CE

Cada arquivo/aba de CE deve ter **exatamente 4 colunas**, nesta ordem:

1. `Data`
2. `Equipamento`
3. `Número(s) CE`
4. `Inoperância (Minutos)`

**Regra de validação:** se a origem online retornar número de colunas diferente de 4, considera-se inválida (provável planilha privada) e aciona-se o fallback local.

## 4. Cadastro de locais

Arquivo `Controle_de_CE_-_locais.csv` com 3 colunas: `Série`, `Locais`, `Sentido`.

- A junção com os dados de CE é feita por **Equipamento = Série**.
- Equipamento sem cadastro correspondente recebe `Local = "Não Cadastrado"` e `Sentido = "Não Cadastrado"`.

## 5. Limpeza e normalização

- **Datas:** convertidas com `dayfirst=True` (formato brasileiro `dd/mm/aaaa`); datas inválidas viram `NaT` (`errors="coerce"`).
- **Mês:** derivado da data.
- **Horas:** `Inoperância (Minutos) / 60`.
- **IDs de equipamento/série:** convertidos para string, removendo parte decimal (`337.0` → `337`) e zeros à esquerda (`0337` → `337`). Isso garante que o `merge` entre CE e cadastro funcione.
- **Local/Sentido:** quebras de linha (`\n`) são substituídas por ` / ` para melhorar a exibição em tabelas e seletores.

## 6. Contagem de CEs (regra crítica)

Um mesmo registro pode conter **múltiplas CEs combinadas por pipe**, ex.: `CE: 009 | CE: 010`.

- Para contar CEs, o valor é **dividido pelo separador `|`**, explodido em linhas e cada parte é contada individualmente.
- A contagem é **distinta por (Número da CE + Ano)** — ou seja, a mesma CE repetida em anos diferentes conta como ocorrências separadas, mas repetições dentro do mesmo ano contam uma vez.
- Valores vazios são descartados.

Essa regra vale tanto para o card "Número CE's" quanto para a coluna "Número de CE's" da tabela analítica.

## 7. Métricas (como são calculadas)

| Métrica | Cálculo |
|---|---|
| Número CE's | Contagem distinta de CE por ano (conforme regra 6) |
| Inoperância Acumulada | Soma de `Inoperância_Horas` |
| Equipamentos Afetados | Contagem distinta de `Equipamento` |
| Média Horas / Ocorrência | Média de `Inoperância_Horas` (0 se não houver linhas) |

## 8. Filtros

- **Ano:** multisseleção; por padrão todos os anos vêm selecionados.
- **Equipamento:** opção `"Todos"` + lista `"código - local"`; ao filtrar, extrai-se o código antes do ` - `.
- **Sentido:** campo somente leitura, derivado do equipamento selecionado; `"Todos"` quando nenhum equipamento específico está filtrado; `"Não Cadastrado"` se o equipamento não tiver sentido cadastrado.
- A lista de equipamentos respeita o filtro de ano já aplicado.

## 9. Agregações dos gráficos e tabela

- **Top 10 CEs:** CEs combinadas por `|` são **explodidas** (uma linha por CE) antes da agregação, de forma consistente com o card de métrica e a tabela analítica; em seguida soma-se as horas por (`Numero_CE`, `Ano`), top 10. As horas de um evento que cobre várias CEs são **atribuídas integralmente a cada CE** envolvida (não há rateio).
- **Ranking de equipamentos:** soma de horas por `Equipamento`, top 10.
- **Histórico mensal:** soma de horas por (`Ano`, `Mes`), ordenado cronologicamente, agrupado por ano.
- **Tabela analítica:** agrupada por (`Equipamento`, `Local`, `Sentido`), com nº de CEs e soma de horas (1 casa decimal), ordenada por horas desc.

## 10. Formatação de números (padrão BR)

- Total de horas: separador de milhar `.`, sem decimais (ex.: `1.234h`).
- Média de horas: 1 casa decimal com vírgula (ex.: `12,5h`).

## 11. Exportação

- A tabela analítica **filtrada** é exportada em CSV com encoding `utf-8-sig` (compatível com Excel em português).
- Nome do arquivo: `inoperancia_radares_filtrado.csv`.
