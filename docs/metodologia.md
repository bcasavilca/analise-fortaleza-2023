# Metodologia da Análise

## Fonte dos Dados

- **Origem:** Portal da Transparência da Prefeitura de Fortaleza
- **URL:** http://transparencia.fortaleza.ce.gov.br/
- **Arquivo:** Diárias do exercício de 2023
- **Data de obtenção:** 18 de Abril de 2026

## Ferramentas Utilizadas

- **Python 3.12**
- **Pandas:** Análise de dados tabulares
- **Git/GitHub:** Versionamento e publicação

## Critérios de Suspeição

### 1. Valores Atípicos
- Diárias superiores a **R$ 10.000,00**
- Baseado em percentil 95% da distribuição

### 2. Pagamentos Duplicados
- Mesmo beneficiário
- Mesmo período
- Mesmo valor
- Repetição 2x ou mais

### 3. Viagens em Grupo
- 5 ou mais pessoas
- Mesmo destino
- Mesmo período
- Possível "turismo de grupo"

### 4. Empenhos Compartilhados
- Mesmo número de empenho
- Diferentes beneficiários
- Questionamento sobre controle orçamentário

## Limitações

1. **Não temos acesso** aos processos administrativos completos
2. **Não podemos verificar** se as viagens realmente ocorreram
3. **Não temos acesso** a documentos comprobatórios (passagens, hotéis)
4. **Não verificamos** se os eventos mencionados existiram

## Princípios Éticos

- Dados públicos obtidos via LAI
- Análise objetiva e baseada em fatos
- Foco em padrões estatísticos, não em pessoas
- Transparência total da metodologia

## Reprodutibilidade

Qualquer pessoa pode reproduzir esta análise:
1. Baixar os dados originais do Portal da Transparência
2. Executar os scripts Python disponíveis em `/scripts`
3. Verificar os resultados

## Contato

Para dúvidas sobre a metodologia: abrir issue no repositório.
