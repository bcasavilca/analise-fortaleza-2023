# Análise de Dados de Transparência - Prefeitura de Fortaleza 2023

Este repositório contém análise dos dados de diárias da Prefeitura de Fortaleza (CE) referentes ao exercício de 2023.

## 📊 Resumo Executivo

- **Total de registros analisados:** 808
- **Valor total em diárias:** R$ 2.909.155,03
- **Média por diária:** R$ 3.600,44
- **Status:** 774 pagos | 26 anulados | 8 não aprovados

## 🚨 Principais Achados

### 1. Viagens Internacionais (174 viagens)
- **Valor total:** R$ 2.088.895,25
- **Representam:** 71,8% do gasto total
- **Destinos principais:**
  - Limerick (Irlanda): R$ 490.392,00
  - Cáceres (Espanha): R$ 482.328,00
  - Grenoble (França): R$ 425.598,00

### 2. Suspeitas de Irregularidades

#### 🔴 Limerick (Irlanda) - Dezembro 2023
- 27 pessoas para intercâmbio "Professores Sem Fronteiras"
- **Problema:** 2 pessoas receberam R$ 24.696,00 (40% a mais que os outros R$ 17.640,00)
- **Beneficiárias com valor maior:**
  - MARISA BOTAO DE AQUINO
  - ALINE GADELHA FIGUEIREDO RIBEIRO

#### 🔴 Empenhos Compartilhados
- **113 empenhos** utilizados por mais de uma pessoa
- Exemplo: Empenho 150 usado por 4 pessoas diferentes

#### 🔴 Gabinete do Vice-Prefeito
- **José Elcio Batista:** Múltiplas viagens internacionais caras
  - Nairobi: R$ 17.710,00
  - Nova York: R$ 12.397,00
  - Barcelona: R$ 10.605,00

### 3. Desproporção entre Áreas

| Área | Viagens | Total | Média | Internacionais |
|------|---------|-------|-------|----------------|
| **EDUCAÇÃO** | 136 | **R$ 1.548.724** | **R$ 11.387** | **113** |
| SAÚDE | 41 | R$ 56.810 | R$ 1.385 | 0 |
| ASSISTÊNCIA SOCIAL | 4 | R$ 5.700 | R$ 1.425 | 0 |

**A Educação gastou 27x mais que a Saúde!**

## 📁 Estrutura do Repositório

```
├── README.md                          # Este arquivo
├── dados/                             # Dados brutos (se permitido)
├── scripts/                           # Scripts de análise
│   ├── analisar_fortaleza_2023.py    # Análise geral
│   └── analise_profunda_fortaleza.py  # Análise detalhada
├── resultados/                        # Resultados gerados
│   ├── resumo_executivo.md
│   └── suspeitos_fortaleza_2023.csv   # Registros suspeitos
└── docs/                              # Documentação
    └── metodologia.md
```

## 🔍 Scripts Disponíveis

### Análise Geral (`analisar_fortaleza_2023.py`)
- Resumo estatístico
- Top beneficiários
- Top destinos
- Detecção de duplicados
- Análise de valores atípicos

### Análise Profunda (`analise_profunda_fortaleza.py`)
- Programa Professores Sem Fronteiras
- Detalhamento IPEM
- Gabinete do Prefeito/Vice
- Secretaria de Turismo
- Análise de empenhos
- Categorização de gastos

## 🎯 Recomendações

1. **Investigar valores diferenciados** em viagens para Limerick
2. **Auditar empenhos compartilhados** (113 casos)
3. **Verificar justificativas** das viagens internacionais do Gabinete
4. **Comparar políticas** de diárias entre Educação e Saúde

## 📄 Fonte dos Dados

Portal da Transparência da Prefeitura de Fortaleza
- URL: http://transparencia.fortaleza.ce.gov.br/
- Dados obtidos em: Abril/2026

## 👤 Autor

Análise realizada por @bcasavilca
Data: 18 de Abril de 2026

## 📜 Licença

Dados públicos obtidos via Lei de Acesso à Informação (LAI).
Análise livre para fins jornalísticos e acadêmicos.
