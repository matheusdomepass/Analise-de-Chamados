# 📊 Análise de Chamados de Suporte de TI com Python

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pandas-2.x-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/Matplotlib-3.x-11557c?style=for-the-badge&logo=matplotlib&logoColor=white"/>
  <img src="https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Concluído-22C55E?style=for-the-badge"/>
</p>

---

## 📋 Sobre o Projeto

Este projeto simula o trabalho de um **Analista de Dados Júnior** dentro de uma empresa de médio porte que opera um service desk de suporte técnico de TI.

A empresa atua em sete áreas: **Financeiro, Comercial, Logística, Recursos Humanos, Produção, Administrativo e TI**. Ao longo de **2024**, foram registrados aproximadamente **10.000 chamados técnicos** atendidos por uma equipe de 8 técnicos de suporte.

A análise parte de uma **base de dados bruta com problemas reais de qualidade** — duplicatas, valores ausentes, erros de digitação e formatos inconsistentes — e evolui até a geração de indicadores e insights acionáveis para a gestão.

---

## 🎯 Problema de Negócio

A gestão de TI identificou que os **SLAs (Service Level Agreements)** estão sendo frequentemente descumpridos e que a **satisfação dos usuários internos** tem caído. Sem dados confiáveis e análises estruturadas, não é possível tomar decisões embasadas.

As principais perguntas que este projeto responde:

| # | Pergunta de Negócio |
|---|---|
| 1 | Qual setor gera mais chamados de suporte? |
| 2 | Qual categoria de problema é mais recorrente? |
| 3 | Qual o tempo médio de resolução por categoria? |
| 4 | Qual percentual dos chamados é resolvido dentro do SLA? |
| 5 | Quais setores têm maior número de chamados fora do SLA? |
| 6 | Qual técnico finalizou mais chamados? Quem resolve mais rápido? |
| 7 | Como os chamados evoluíram ao longo dos meses de 2024? |
| 8 | Qual a satisfação média dos clientes internos? |
| 9 | Existe relação entre prioridade e tempo de resolução? |

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| **Python 3.10+** | Linguagem principal |
| **Pandas** | Manipulação e análise de dados |
| **Matplotlib** | Visualização de dados |
| **Jupyter Notebook** | Ambiente de análise interativa |
| **CSV** | Fonte de dados |

---

## 📁 Estrutura do Projeto

```
analise-chamados-ti/
│
├── data/
│   └── chamados_ti.csv          ← Base de dados com ~10.000 registros
│
├── notebooks/
│   └── analise_chamados.ipynb   ← Notebook principal com toda a análise
│
├── images/
│   ├── 01_chamados_por_setor.png
│   ├── 02_chamados_por_categoria.png
│   ├── 03_evolucao_mensal.png
│   ├── 04_tempo_resolucao_categoria.png
│   ├── 05_sla_analise.png
│   ├── 06_chamados_por_prioridade.png
│   └── 07_desempenho_tecnicos.png
│
├── gerar_dados.py               ← Script que gera a base de dados
├── requirements.txt             ← Dependências do projeto
└── README.md
```

---

## 🔢 Etapas do Projeto

```
1. Geração da Base de Dados
   └── Script Python que cria ~10.000 registros com problemas de qualidade

2. Carregamento e Entendimento
   └── df.head() | df.info() | df.describe() | df.shape | isnull | duplicated

3. Limpeza e Tratamento dos Dados
   ├── Remoção de duplicatas
   ├── Padronização de textos (strip + title case)
   ├── Correção de erros de digitação nas categorias
   ├── Conversão de datas (formatos mistos → datetime)
   ├── Tratamento de valores ausentes
   ├── Remoção de valores inconsistentes (horas negativas)
   └── Criação de colunas auxiliares (mês, dia da semana)

4. Indicadores Principais (KPIs)
   └── Total | Finalizados | Abertos | Críticos | SLA | Satisfação | Tempo Médio

5. Análise Exploratória de Dados
   └── Agrupamentos por setor, categoria, prioridade, técnico e período

6. Visualizações
   └── 7 gráficos com Matplotlib

7. Insights e Recomendações
   └── Conclusões baseadas nos dados reais encontrados
```

---

## 📊 Principais Indicadores (KPIs)

| KPI | Descrição |
|---|---|
| **Total de Chamados** | Volume total registrado no período |
| **Chamados Finalizados** | Quantidade e percentual de chamados encerrados |
| **Chamados em Aberto** | Demandas ainda não resolvidas |
| **Chamados Críticos** | Chamados com prioridade máxima |
| **Tempo Médio de Resolução** | Média em horas para fechar um chamado |
| **% Cumprimento do SLA** | Percentual resolvido dentro do prazo acordado |
| **Satisfação Média** | Nota média dos usuários (escala 1–5) |

---

## 💡 Principais Insights

> Os insights abaixo são baseados nos dados reais gerados e analisados no notebook.

1. **O setor Comercial** concentrou a maior quantidade de chamados durante o período analisado, indicando alta dependência de infraestrutura de TI ou necessidade de treinamento de usuários.

2. **Hardware e Software** são as categorias com maior volume de chamados, reforçando a necessidade de um programa de manutenção preventiva.

3. **O cumprimento do SLA está abaixo do ideal**, indicando que a equipe pode estar sobrecarregada ou que os prazos precisam ser renegociados.

4. **A categoria com maior tempo médio de resolução** apresenta um gargalo operacional que pode exigir reforço de equipe ou melhoria de processos.

5. **A distribuição de chamados entre técnicos é desigual**, com alguns profissionais com volume muito superior aos demais, o que pode levar à sobrecarga e queda de qualidade.

6. **A satisfação dos clientes internos** está diretamente ligada ao cumprimento do SLA — chamados dentro do prazo recebem avaliações consistentemente mais altas.

---

## ⚙️ Como Executar

### 1. Clone o repositório
```bash
git clone https://github.com/matheusdomepass/analise-chamados-ti.git
cd analise-chamados-ti
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Gere a base de dados
```bash
python gerar_dados.py
```

### 4. Execute o Jupyter Notebook
```bash
jupyter notebook notebooks/analise_chamados.ipynb
```

> O notebook já está configurado para ler o arquivo `data/chamados_ti.csv` automaticamente.

---

## 🧪 Problemas de Qualidade na Base (Propositais)

A base foi gerada com os seguintes problemas para simular dados reais corporativos:

| Problema | Descrição |
|---|---|
| **Duplicatas** | ~1% dos registros estão duplicados |
| **Valores ausentes** | Setor, técnico e prioridade com nulos |
| **Erros de grafia** | `"Softwre"`, `"Sisitema"`, `"Impresora"` |
| **Variações de caixa** | `"COMERCIAL"`, `"comercial"`, `"Comercial"` |
| **Espaços extras** | `" Hardware"`, `"Financeiro "` |
| **Formatos de data mistos** | `YYYY-MM-DD`, `DD/MM/YYYY`, `MM/DD/YYYY` |
| **Valores inconsistentes** | Horas de resolução negativas ou zero |

---

## 👤 Autor

**Matheus Domeneghetti Passatuto**

[![GitHub](https://img.shields.io/badge/GitHub-matheusdomepass-181717?style=for-the-badge&logo=github)](https://github.com/matheusdomepass)

---

*Projeto desenvolvido como portfólio de Análise de Dados — 2024*
