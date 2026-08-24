"""
Script para geração da base de dados chamados_ti.csv
Gera ~10.000 registros com problemas propositais de qualidade de dados
para serem tratados no notebook de análise.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# ── Reprodutibilidade ──────────────────────────────────────────────────────────
random.seed(42)
np.random.seed(42)

# ── Parâmetros gerais ─────────────────────────────────────────────────────────
N = 10_000
DATA_INICIO = datetime(2024, 1, 1)
DATA_FIM    = datetime(2024, 12, 31)

# ── Domínios limpos (valores corretos) ────────────────────────────────────────
SETORES = ["Financeiro", "Recursos Humanos", "Comercial",
           "Logística", "Administrativo", "Produção", "TI"]

CATEGORIAS = ["Hardware", "Software", "Rede", "Sistema",
              "Acesso", "Impressora", "E-mail"]

SUBCATEGORIAS = {
    "Hardware":   ["Notebook", "Desktop", "Monitor", "Teclado/Mouse", "Headset"],
    "Software":   ["Office", "ERP", "Antivírus", "Navegador", "Teams"],
    "Rede":       ["Sem Internet", "VPN", "Wi-Fi", "Lentidão", "Firewall"],
    "Sistema":    ["Falha no Sistema", "Travamento", "Erro de Login", "Atualização", "Backup"],
    "Acesso":     ["Bloqueio de Conta", "Reset de Senha", "Permissão", "Active Directory", "E-mail Corporativo"],
    "Impressora": ["Sem Impressão", "Atolamento", "Driver", "Toner", "Conexão"],
    "E-mail":     ["Caixa Cheia", "Erro de Envio", "Spam", "Configuração", "Assinatura"],
}

PRIORIDADES = ["Baixa", "Média", "Alta", "Crítica"]
PRIORIDADE_PESOS = [0.35, 0.40, 0.17, 0.08]

STATUS = ["Aberto", "Em andamento", "Finalizado", "Cancelado"]
STATUS_PESOS = [0.06, 0.10, 0.78, 0.06]

TECNICOS = [
    "Ana Lima", "Carlos Souza", "Fernanda Costa", "João Pereira",
    "Lucas Mendes", "Marina Oliveira", "Rafael Torres", "Tatiane Alves",
]

# SLA (horas) por prioridade
SLA_MAP = {"Crítica": 4, "Alta": 8, "Média": 24, "Baixa": 48}

# Peso de chamados por setor (Comercial e Financeiro mais sobrecarregados)
SETOR_PESOS = [0.20, 0.12, 0.22, 0.14, 0.10, 0.12, 0.10]


def data_aleatoria(inicio, fim):
    delta = fim - inicio
    return inicio + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def horas_resolucao_por_prioridade(prioridade):
    """Gera horas de resolução com distribuição realista por prioridade."""
    bases = {"Crítica": (2, 12), "Alta": (4, 20), "Média": (10, 50), "Baixa": (20, 80)}
    low, high = bases[prioridade]
    return round(random.uniform(low, high), 1)


# ── Geração dos registros limpos ───────────────────────────────────────────────
registros = []

for i in range(1, N + 1):
    setor      = random.choices(SETORES, weights=SETOR_PESOS)[0]
    categoria  = random.choices(CATEGORIAS)[0]
    subcat     = random.choice(SUBCATEGORIAS[categoria])
    prioridade = random.choices(PRIORIDADES, weights=PRIORIDADE_PESOS)[0]
    status     = random.choices(STATUS, weights=STATUS_PESOS)[0]
    tecnico    = random.choice(TECNICOS)

    data_abertura = data_aleatoria(DATA_INICIO, DATA_FIM)

    horas = horas_resolucao_por_prioridade(prioridade)
    sla   = SLA_MAP[prioridade]

    if status in ("Finalizado", "Cancelado"):
        data_fechamento = data_abertura + timedelta(hours=horas)
        sla_status = "Dentro do SLA" if horas <= sla else "Fora do SLA"
    else:
        data_fechamento = None
        horas = None
        sla_status = None

    satisfacao = None
    if status == "Finalizado":
        # Satisfação entre 1 e 5; chamados críticos/fora SLA tendem a ter nota menor
        base_satisfacao = 3.5 if sla_status == "Fora do SLA" else 4.2
        satisfacao = round(min(5, max(1, np.random.normal(base_satisfacao, 0.8))), 1)

    registros.append({
        "id_chamado":        i,
        "data_abertura":     data_abertura.strftime("%Y-%m-%d %H:%M:%S"),
        "data_fechamento":   data_fechamento.strftime("%Y-%m-%d %H:%M:%S") if data_fechamento else None,
        "setor":             setor,
        "categoria":         categoria,
        "subcategoria":      subcat,
        "prioridade":        prioridade,
        "tecnico":           tecnico,
        "status":            status,
        "horas_resolucao":   horas,
        "sla_horas":         sla,
        "sla_status":        sla_status,
        "satisfacao_cliente": satisfacao,
    })

df = pd.DataFrame(registros)

# ══════════════════════════════════════════════════════════════════════════════
# INSERÇÃO PROPOSITAL DE PROBLEMAS DE QUALIDADE DE DADOS
# ══════════════════════════════════════════════════════════════════════════════

# 1. Duplicatas (≈1 % dos registros)
idx_dup = df.sample(frac=0.01, random_state=1).index
df = pd.concat([df, df.loc[idx_dup]], ignore_index=True)

# 2. Variações de grafia nas categorias (case, espaços, acentuação)
variantes_categoria = {
    "Hardware":   ["hardware", "HARDWARE", " Hardware", "Hardware "],
    "Software":   ["software", "SOFTWARE", "Softwre"],       # typo intencional
    "Rede":       ["rede", "REDE", " Rede"],
    "Sistema":    ["sistema", "SISTEMA", "Sisitema"],         # typo intencional
    "Acesso":     ["acesso", "ACESSO", " Acesso "],
    "Impressora": ["impressora", "IMPRESSORA", "Impresora"],  # typo intencional
    "E-mail":     ["e-mail", "Email", "E-Mail", "EMAIL"],
}

# Aplica variantes em ~8 % dos registros
mask_cat = df.sample(frac=0.08, random_state=2).index
for idx in mask_cat:
    cat_original = df.at[idx, "categoria"]
    if cat_original in variantes_categoria:
        df.at[idx, "categoria"] = random.choice(variantes_categoria[cat_original])

# 3. Variações de grafia nos setores
variantes_setor = {
    "Financeiro":       ["financeiro", "FINANCEIRO", "Financeiro "],
    "Recursos Humanos": ["Recursos humanos", "RECURSOS HUMANOS", "RH", "Rec. Humanos"],
    "Comercial":        ["comercial", "COMERCIAL", "Comercial "],
    "Logística":        ["Logistica", "logística", "LOGISTICA"],
    "Administrativo":   ["administrativo", "ADMINISTRATIVO", "Admnistrativo"],  # typo
    "Produção":         ["producao", "PRODUCAO", "Produção "],
    "TI":               ["ti", "T.I.", "T.I"],
}

mask_set = df.sample(frac=0.08, random_state=3).index
for idx in mask_set:
    set_original = df.at[idx, "setor"]
    if set_original in variantes_setor:
        df.at[idx, "setor"] = random.choice(variantes_setor[set_original])

# 4. Valores ausentes em colunas chave
# Setor ausente (~0.5 %)
df.loc[df.sample(frac=0.005, random_state=4).index, "setor"] = None
# Técnico ausente (~0.8 %)
df.loc[df.sample(frac=0.008, random_state=5).index, "tecnico"] = None
# Prioridade ausente (~0.5 %)
df.loc[df.sample(frac=0.005, random_state=6).index, "prioridade"] = None
# Satisfação ausente em alguns finalizados (~3 %)
mask_fin = df[df["status"] == "Finalizado"].sample(frac=0.03, random_state=7).index
df.loc[mask_fin, "satisfacao_cliente"] = None

# 5. Datas em formatos diferentes (~2 % das datas de abertura)
mask_datas = df.sample(frac=0.02, random_state=8).index
for idx in mask_datas:
    val = df.at[idx, "data_abertura"]
    if val and isinstance(val, str):
        try:
            dt = datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
            # Alterna entre formatos
            fmt = random.choice(["%d/%m/%Y %H:%M", "%d-%m-%Y", "%m/%d/%Y"])
            df.at[idx, "data_abertura"] = dt.strftime(fmt)
        except Exception:
            pass

# 6. Espaços extras em nomes de técnicos (~1 %)
mask_tec = df.sample(frac=0.01, random_state=9).index
for idx in mask_tec:
    val = df.at[idx, "tecnico"]
    if isinstance(val, str):
        df.at[idx, "tecnico"] = " " + val + " "

# 7. Valores inconsistentes de horas_resolucao (negativos ou zero) em ~0.3 %
mask_hrs = df[df["horas_resolucao"].notna()].sample(frac=0.003, random_state=10).index
for idx in mask_hrs:
    df.at[idx, "horas_resolucao"] = random.choice([-1.0, 0.0, -5.5])

# 8. sla_status com variações de grafia em ~2 %
variantes_sla = {
    "Dentro do SLA": ["dentro do sla", "DENTRO DO SLA", "Dentro do Sla"],
    "Fora do SLA":   ["fora do sla",   "FORA DO SLA",   "Fora do Sla"],
}
mask_sla = df[df["sla_status"].notna()].sample(frac=0.02, random_state=11).index
for idx in mask_sla:
    val = df.at[idx, "sla_status"]
    if val in variantes_sla:
        df.at[idx, "sla_status"] = random.choice(variantes_sla[val])

# Embaralha o dataframe
df = df.sample(frac=1, random_state=99).reset_index(drop=True)

# ── Salva o CSV ────────────────────────────────────────────────────────────────
os.makedirs("data", exist_ok=True)
df.to_csv("data/chamados_ti.csv", index=False, encoding="utf-8-sig")

print(f"[OK] Base gerada com {len(df):,} registros em data/chamados_ti.csv")
print(f"   Colunas: {list(df.columns)}")
print(f"   Duplicatas: {df.duplicated().sum()}")
print(f"   Nulos:\n{df.isnull().sum()}")
