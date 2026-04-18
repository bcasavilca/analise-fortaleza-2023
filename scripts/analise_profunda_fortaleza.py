#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analise Profunda - Dados de Diarias Fortaleza 2023
Investiga padroes especificos de possiveis irregularidades
"""

import pandas as pd
import numpy as np

# Ler arquivo
arquivo_csv = r'C:\Users\Administrator\.openclaw\media\inbound\transparencia-diarias-2023---92095f57-9250-4ee7-a746-4bc49d920b2c.csv'
df = pd.read_csv(arquivo_csv, sep=';', encoding='utf-8-sig', on_bad_lines='skip')

# Mapear colunas
col_valor = [c for c in df.columns if 'Valor' in c][0]
col_benef = [c for c in df.columns if 'Benefici' in c][0]
col_status = [c for c in df.columns if 'Situa' in c][0]
col_unidade = [c for c in df.columns if 'Unidade' in c][0]
col_destino = [c for c in df.columns if 'Destino' in c][0]
col_periodo = [c for c in df.columns if 'Per' in c][0]
col_motivo = [c for c in df.columns if 'Motivo' in c][0]
col_empenho = [c for c in df.columns if 'empenho' in c.lower()][0]

df[col_valor] = pd.to_numeric(df[col_valor], errors='coerce')
df_pagos = df[df[col_status] == 'Pago'].copy()

print("=" * 90)
print("ANALISE PROFUNDA - DADOS SUSPEITOS")
print("=" * 90)

# ============================================================
# 1. ANALISE DO PROGRAMA "PROFESSORES SEM FRONTEIRAS"
# ============================================================
print("\n" + "=" * 90)
print("1. PROGRAMA 'PROFESSORES SEM FRONTEIRAS' - VIAGENS PARA ESPANHA")
print("=" * 90)

professores = df_pagos[df_pagos[col_motivo].str.contains('PROFESSOR', case=False, na=False)]
print(f"\nTotal de viagens relacionadas a professores: {len(professores)}")
print(f"Valor total: R$ {professores[col_valor].sum():,.2f}")

caceres = professores[professores[col_destino].str.contains('CACERES', case=False, na=False)]
print(f"\nViagens para Caceres (Espanha): {len(caceres)}")
print(f"Valor total Caceres: R$ {caceres[col_valor].sum():,.2f}")
print(f"Media por pessoa: R$ {caceres[col_valor].mean():,.2f}")
print("\n--- Lista de beneficiarios (Caceres) ---")
for _, row in caceres.sort_values(col_valor, ascending=False).iterrows():
    print(f"  R$ {row[col_valor]:>10,.2f} | {row[col_benef][:40]:<40}")

# ============================================================
# 2. ANALISE DA VIAGEM PARA LIMERICK (IRLANDA)
# ============================================================
print("\n" + "=" * 90)
print("2. VIAGEM PARA LIMERICK (IRLANDA) - DEZEMBRO 2023")
print("=" * 90)

limerick = df_pagos[df_pagos[col_destino].str.contains('LIMERICK', case=False, na=False)]
print(f"\nTotal de pessoas: {len(limerick)}")
print(f"Valor total: R$ {limerick[col_valor].sum():,.2f}")
print(f"Media por pessoa: R$ {limerick[col_valor].mean():,.2f}")
print(f"Valores individuais: R$ {limerick[col_valor].unique()}")

# Por que alguns pagaram mais?
print("\n--- Analise de valores diferenciados ---")
limerick_altos = limerick[limerick[col_valor] > 17640]
if len(limerick_altos) > 0:
    print(f"\n{len(limerick_altos)} pessoas com valor maior (R$ 24.696):")
    for _, row in limerick_altos.iterrows():
        print(f"  {row[col_benef][:45]:<45} | {row[col_valor]:>10,.2f}")
        print(f"    Motivo: {str(row[col_motivo])[:60]}...")

# ============================================================
# 3. ANALISE DO IPEM (INSTITUTO DE PESOS E MEDIDAS)
# ============================================================
print("\n" + "=" * 90)
print("3. INSTITUTO DE PESOS E MEDIDAS (IPEM) - ANALISE DETALHADA")
print("=" * 90)

ipem = df_pagos[df_pagos[col_unidade].str.contains('PESOS', case=False, na=False)]
print(f"\nTotal de diarias: {len(ipem)}")
print(f"Valor total: R$ {ipem[col_valor].sum():,.2f}")

# Funcionarios com mais viagens
print("\n--- Top 10 funcionarios IPEM (por numero de viagens) ---")
ipem_benef = ipem[col_benef].value_counts().head(10)
for nome, count in ipem_benef.items():
    total = ipem[ipem[col_benef] == nome][col_valor].sum()
    print(f"  {str(nome)[:45]:<45} | {count:>3} viagens | R$ {total:>10,.2f}")

# Analise de Antonio Luiz Pereira Franco (o que mais viajou)
print("\n--- Antonio Luiz Pereira Franco (43 viagens) - Detalhe ---")
antonio = ipem[ipem[col_benef].str.contains('ANTONIO LUIZ PEREIRA FRANCO', case=False, na=False)]
print(f"Total gasto: R$ {antonio[col_valor].sum():,.2f}")
print(f"Media por viagem: R$ {antonio[col_valor].mean():,.2f}")
print(f"Destinos principais:")
dests = antonio[col_destino].value_counts().head(10)
for dest, count in dests.items():
    print(f"    {str(dest)[:40]:<40} | {count:>2}x")

# ============================================================
# 4. ANALISE DO GABINETE DO PREFEITO E VICE
# ============================================================
print("\n" + "=" * 90)
print("4. GABINETE DO PREFEITO E VICE-PREFEITO")
print("=" * 90)

gabinete = df_pagos[df_pagos[col_unidade].str.contains('GABINETE', case=False, na=False)]
print(f"\nTotal gasto: R$ {gabinete[col_valor].sum():,.2f}")
print(f"Numero de viagens: {len(gabinete)}")
print(f"Media por viagem: R$ {gabinete[col_valor].mean():,.2f}")

print("\n--- Lista de viagens do Gabinete ---")
for _, row in gabinete.sort_values(col_valor, ascending=False).iterrows():
    print(f"\n  R$ {row[col_valor]:>10,.2f} | {row[col_benef][:35]:<35}")
    print(f"    Destino: {row[col_destino]}")
    print(f"    Periodo: {row[col_periodo]}")

# ============================================================
# 5. ANALISE DE VIAGENS DE TURISMO (Secretaria de Turismo)
# ============================================================
print("\n" + "=" * 90)
print("5. SECRETARIA MUNICIPAL DO TURISMO")
print("=" * 90)

turismo = df_pagos[df_pagos[col_unidade].str.contains('TURISMO', case=False, na=False)]
print(f"\nTotal gasto: R$ {turismo[col_valor].sum():,.2f}")
print(f"Numero de viagens: {len(turismo)}")

print("\n--- Viagens internacionais do Turismo ---")
turismo_int = turismo[turismo[col_destino].str.contains('-EX', case=False, na=False)]
for _, row in turismo_int.sort_values(col_valor, ascending=False).iterrows():
    print(f"\n  R$ {row[col_valor]:>10,.2f} | {row[col_benef][:35]:<35}")
    print(f"    Destino: {row[col_destino]}")
    print(f"    Motivo: {str(row[col_motivo])[:70]}...")

# ============================================================
# 6. COMPARATIVO: EDUCACAO vs OUTRAS AREAS
# ============================================================
print("\n" + "=" * 90)
print("6. COMPARATIVO: FUNDOS MUNICIPAIS")
print("=" * 90)

fundos = {
    'EDUCACAO': df_pagos[df_pagos[col_unidade].str.contains('EDUCACAO', case=False, na=False)],
    'SAUDE': df_pagos[df_pagos[col_unidade].str.contains('SAUDE', case=False, na=False)],
    'ASSISTENCIA SOCIAL': df_pagos[df_pagos[col_unidade].str.contains('ASSISTENCIA', case=False, na=False)],
}

print("\n--- Comparativo de Fundos ---")
for nome, dados in fundos.items():
    total = dados[col_valor].sum()
    count = len(dados)
    intl = len(dados[dados[col_destino].str.contains('-EX', na=False)])
    media = dados[col_valor].mean() if count > 0 else 0
    print(f"\n{nome}:")
    print(f"  Viagens: {count:>4} | Total: R$ {total:>14,.2f} | Media: R$ {media:>10,.2f}")
    print(f"  Viagens internacionais: {intl}")

# ============================================================
# 7. ANALISE DE EMPENHOS NULOS/REPETIDOS
# ============================================================
print("\n" + "=" * 90)
print("7. EMPENHOS - ANALISE DE DOCUMENTACAO")
print("=" * 90)

# Empenhos nulos
empenhos_nulos = df_pagos[df_pagos[col_empenho].isna() | (df_pagos[col_empenho] == 'null')]
print(f"\nEmpenhos nulos/registros sem documentacao: {len(empenhos_nulos)}")
print(f"Valor total destes registros: R$ {empenhos_nulos[col_valor].sum():,.2f}")

# Empenhos repetidos
print("\n--- Empenhos utilizados multiplas vezes ---")
emp_rep = df_pagos[df_pagos[col_empenho].notna() & (df_pagos[col_empenho] != 'null')]
rep_counts = emp_rep[col_empenho].value_counts()
repetidos = rep_counts[rep_counts > 1]
if len(repetidos) > 0:
    print(f"\n{len(repetidos)} empenhos usados mais de uma vez:")
    for empenho, count in repetidos.head(10).items():
        print(f"  Empenho {empenho}: {count} vezes")
        # Mostrar os beneficiarios deste empenho
        benefs = emp_rep[emp_rep[col_empenho] == empenho][col_benef].unique()
        print(f"    Beneficiarios: {', '.join([str(b)[:30] for b in benefs])}")
else:
    print("Nenhum empenho repetido encontrado")

# ============================================================
# 8. GASTOS COM HOSPEDAGEM vs DIARIAS
# ============================================================
print("\n" + "=" * 90)
print("8. ANALISE DE MOTIVOS - TIPOS DE DESPESA")
print("=" * 90)

# Categorizar por tipo de motivo
def categorizar_motivo(motivo):
    if pd.isna(motivo):
        return 'Nao informado'
    m = str(motivo).upper()
    if 'CONGRESSO' in m or 'SEMINARIO' in m or 'EVENTO' in m:
        return 'Eventos/Congressos'
    elif 'REUNIAO' in m:
        return 'Reunioes'
    elif 'CURSO' in m or 'CAPACITACAO' in m:
        return 'Cursos/Capacitacao'
    elif 'FISCALIZACAO' in m or 'VERIFICACAO' in m:
        return 'Fiscalizacao Tecnica'
    elif 'INTERCAMBIO' in m or 'PROFESSOR' in m:
        return 'Intercambio Internacional'
    else:
        return 'Outros'

df_pagos['Categoria'] = df_pagos[col_motivo].apply(categorizar_motivo)
print("\n--- Gastos por categoria ---")
cat_gastos = df_pagos.groupby('Categoria')[col_valor].agg(['sum', 'count', 'mean'])
for cat in cat_gastos.index:
    total = cat_gastos.loc[cat, 'sum']
    count = cat_gastos.loc[cat, 'count']
    media = cat_gastos.loc[cat, 'mean']
    print(f"  {cat:<30} | {count:>4} viagens | R$ {total:>12,.2f} | Media: R$ {media:>8,.2f}")

print("\n" + "=" * 90)
print("ANALISE PROFUNDA CONCLUIDA")
print("=" * 90)
