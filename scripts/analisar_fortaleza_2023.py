#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisador de Diarias da Prefeitura de Fortaleza - 2023
Detecta padroes de possiveis irregularidades nos dados de transparencia
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re

# Ler o arquivo CSV
print("=" * 80)
print("ANALISE DE DIARIAS - PREFEITURA DE FORTALEZA 2023")
print("=" * 80)

# Caminho do arquivo recebido
arquivo_csv = r'C:\Users\Administrator\.openclaw\media\inbound\transparencia-diarias-2023---92095f57-9250-4ee7-a746-4bc49d920b2c.csv'

# Ler com encoding UTF-8 e separador ;
df = pd.read_csv(arquivo_csv, sep=';', encoding='utf-8-sig', on_bad_lines='skip')

# Limpar espacos em branco nos nomes das colunas e corrigir encoding
df.columns = df.columns.str.strip()

# Mapear colunas (com encoding corrigido manualmente)
col_valor = [c for c in df.columns if 'Valor' in c][0]
col_benef = [c for c in df.columns if 'Benefici' in c][0]
col_status = [c for c in df.columns if 'Situa' in c][0]
col_unidade = [c for c in df.columns if 'Unidade' in c][0]
col_destino = [c for c in df.columns if 'Destino' in c][0]
col_periodo = [c for c in df.columns if 'Per' in c][0]
col_motivo = [c for c in df.columns if 'Motivo' in c][0]

print(f"\nColunas detectadas:")
print(f"  Valor: {col_valor}")
print(f"  Beneficiario: {col_benef}")
print(f"  Status: {col_status}")

# Converter valores para numerico
df[col_valor] = pd.to_numeric(df[col_valor], errors='coerce')

print(f"\nTotal de registros: {len(df)}")

# ============================================================
# 1. RESUMO GERAL
# ============================================================
print("\n" + "=" * 80)
print("1. RESUMO GERAL")
print("=" * 80)

print(f"\nTotal gasto em diarias: R$ {df[col_valor].sum():,.2f}")
print(f"Media por diaria: R$ {df[col_valor].mean():,.2f}")
print(f"Maior diaria: R$ {df[col_valor].max():,.2f}")
print(f"Menor diaria: R$ {df[col_valor].min():,.2f}")

# Status dos empenhos
print("\n--- Status dos Empenhos ---")
status_counts = df[col_status].value_counts()
print(status_counts)

# ============================================================
# 2. TOP BENEFICIARIOS
# ============================================================
print("\n" + "=" * 80)
print("2. TOP 20 BENEFICIARIOS (por valor total)")
print("=" * 80)

top_beneficiarios = df.groupby(col_benef)[col_valor].sum().sort_values(ascending=False).head(20)
for i, (nome, valor) in enumerate(top_beneficiarios.items(), 1):
    print(f"{i:2d}. {nome[:50]:<50} R$ {valor:>12,.2f}")

# ============================================================
# 3. TOP DESTINOS
# ============================================================
print("\n" + "=" * 80)
print("3. TOP 20 DESTINOS (por valor total)")
print("=" * 80)

top_destinos = df.groupby(col_destino)[col_valor].sum().sort_values(ascending=False).head(20)
for i, (destino, valor) in enumerate(top_destinos.items(), 1):
    print(f"{i:2d}. {str(destino)[:50]:<50} R$ {valor:>12,.2f}")

# ============================================================
# 4. ANALISE DE VIAGENS INTERNACIONAIS
# ============================================================
print("\n" + "=" * 80)
print("4. VIAGENS INTERNACIONAIS (contendo 'EX' no destino)")
print("=" * 80)

viagens_int = df[df[col_destino].str.contains('-EX', na=False)]
print(f"\nTotal de viagens internacionais: {len(viagens_int)}")
print(f"Valor total: R$ {viagens_int[col_valor].sum():,.2f}")

# Top internacionais
top_int = viagens_int.groupby(col_destino)[col_valor].sum().sort_values(ascending=False).head(10)
print("\n--- Top 10 destinos internacionais ---")
for destino, valor in top_int.items():
    print(f"  {str(destino):<40} R$ {valor:>12,.2f}")

# ============================================================
# 5. DETECCAO DE POSSIVEIS IRREGULARIDADES
# ============================================================
print("\n" + "=" * 80)
print("5. DETECCAO DE POSSIVEIS IRREGULARIDADES")
print("=" * 80)

# 5.1 Pagamentos duplicados (mesmo beneficiario, mesmo periodo, mesmo valor)
print("\n--- 5.1 Possiveis pagamentos duplicados ---")
df_pagos = df[df[col_status] == 'Pago']
duplicados = df_pagos.groupby([col_benef, col_periodo, col_valor]).size()
duplicados = duplicados[duplicados > 1].sort_values(ascending=False)

if len(duplicados) > 0:
    print(f"Encontrados {len(duplicados)} casos de possiveis duplicacoes:")
    for (benef, periodo, valor), count in duplicados.head(10).items():
        print(f"  {str(benef)[:40]:<40} | {str(periodo):<20} | R$ {valor:>10,.2f} | {count}x")
else:
    print("Nenhum pagamento duplicado identificado")

# 5.2 Valores muito altos (outliers)
print("\n--- 5.2 Valores atipicos (acima de R$ 10.000) ---")
valores_altos = df_pagos[df_pagos[col_valor] > 10000].sort_values(col_valor, ascending=False)
if len(valores_altos) > 0:
    print(f"Encontrados {len(valores_altos)} registros com valores > R$ 10.000:")
    for _, row in valores_altos.head(15).iterrows():
        print(f"  R$ {row[col_valor]:>10,.2f} | {str(row[col_benef])[:35]:<35} | {row[col_destino]}")
else:
    print("Nenhum valor atipico identificado")

# 5.3 Viagens para o mesmo destino no mesmo periodo (turismo de grupo?)
print("\n--- 5.3 Viagens em grupo para mesmo destino/periodo ---")
viagens_grupo = df_pagos.groupby([col_destino, col_periodo]).agg({
    col_benef: 'count',
    col_valor: 'sum'
}).sort_values(col_benef, ascending=False)

viagens_grupo = viagens_grupo[viagens_grupo[col_benef] >= 5]
if len(viagens_grupo) > 0:
    print(f"Encontrados {len(viagens_grupo)} casos de viagens em grupo (5+ pessoas):")
    for (destino, periodo), row in viagens_grupo.head(10).iterrows():
        print(f"  {str(destino)[:35]:<35} | {str(periodo):<20} | {row[col_benef]:>3} pessoas | R$ {row[col_valor]:>12,.2f}")
else:
    print("Nenhuma viagem em grupo identificada")

# 5.4 Beneficiarios com muitas viagens
print("\n--- 5.4 Beneficiarios com maior numero de viagens ---")
count_viagens = df_pagos[col_benef].value_counts().head(15)
for nome, count in count_viagens.items():
    total = df_pagos[df_pagos[col_benef] == nome][col_valor].sum()
    print(f"  {str(nome)[:45]:<45} | {count:>3} viagens | R$ {total:>12,.2f}")

# 5.5 Unidades orcamentarias com maior gasto
print("\n--- 5.5 Top 10 Unidades Orcamentarias (por gasto total) ---")
top_unidades = df_pagos.groupby(col_unidade)[col_valor].sum().sort_values(ascending=False).head(10)
for unidade, valor in top_unidades.items():
    count = df_pagos[df_pagos[col_unidade] == unidade].shape[0]
    print(f"  {str(unidade)[:50]:<50} | {count:>4} diarias | R$ {valor:>14,.2f}")

# ============================================================
# 6. RESUMO POR MES
# ============================================================
print("\n" + "=" * 80)
print("6. GASTOS POR MES (baseado no inicio do periodo)")
print("=" * 80)

def extrair_mes(periodo):
    try:
        # Extrair data inicial (formato: DD-MMM-YY)
        data_inicial = str(periodo).split(' a ')[0]
        meses = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
                 'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}
        for mes_pt, num in meses.items():
            if mes_pt in data_inicial.upper():
                return f"2023-{num}"
        return "2023-00"
    except:
        return "2023-00"

df_pagos['Mes'] = df_pagos[col_periodo].apply(extrair_mes)
gasto_por_mes = df_pagos.groupby('Mes')[col_valor].sum().sort_index()

print("\n--- Gasto mensal ---")
for mes, valor in gasto_por_mes.items():
    if mes != "2023-00":
        nome_mes = {'2023-01': 'Jan', '2023-02': 'Fev', '2023-03': 'Mar', '2023-04': 'Abr',
                    '2023-05': 'Mai', '2023-06': 'Jun', '2023-07': 'Jul', '2023-08': 'Ago',
                    '2023-09': 'Set', '2023-10': 'Out', '2023-11': 'Nov', '2023-12': 'Dez'}.get(mes, mes)
        print(f"  {nome_mes}: R$ {valor:>14,.2f}")

# ============================================================
# 7. EXPORTAR RESULTADOS SUSPEITOS
# ============================================================
print("\n" + "=" * 80)
print("7. EXPORTANDO RESULTADOS")
print("=" * 80)

# Criar DataFrame com dados suspeitos
suspeitos = []

# Adicionar duplicados
for (benef, periodo, valor), count in duplicados.items():
    suspeitos.append({
        'Tipo': 'Pagamento duplicado',
        'Beneficiario': benef,
        'Periodo': periodo,
        'Valor': valor,
        'Observacao': f'Repetido {count} vezes'
    })

# Adicionar valores altos
for _, row in valores_altos.iterrows():
    suspeitos.append({
        'Tipo': 'Valor atipico (>R$ 10k)',
        'Beneficiario': row[col_benef],
        'Periodo': row[col_periodo],
        'Valor': row[col_valor],
        'Destino': row[col_destino],
        'Observacao': str(row[col_motivo])[:50] if pd.notna(row[col_motivo]) else ''
    })

if len(suspeitos) > 0:
    df_suspeitos = pd.DataFrame(suspeitos)
    df_suspeitos.to_csv('suspeitos_fortaleza_2023.csv', index=False, encoding='utf-8-sig', sep=';')
    print(f"Exportados {len(suspeitos)} registros suspeitos para 'suspeitos_fortaleza_2023.csv'")
else:
    print("Nenhum registro suspeito para exportar")

print("\n" + "=" * 80)
print("ANALISE CONCLUIDA")
print("=" * 80)
