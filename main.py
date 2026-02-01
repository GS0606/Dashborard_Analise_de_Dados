import pandas as pd
import numpy as np


df = pd.read_csv("https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv")

# Tradução das colunas para português brasileiro
colunas_traduzidas = {
    'work_year': 'ano',
    'experience_level': 'senioridade',
    'employment_type': 'contrato',
    'job_title': 'cargo',
    'salary': 'salario',
    'salary_currency': 'usd',
    'salary_in_usd': 'salario_usd',
    'employee_residence': 'residencia',
    'remote_ratio': 'remota',
    'company_location': 'empresa',
    'company_size': 'tamanho_empresa'
}
df = df.rename(columns=colunas_traduzidas)

# Tradução dos valores da coluna 'senioridade'
traducao_senioridade = {
    'EN': 'junior',
    'MI': 'Pleno',
    'SE': 'Senior',
    'EX': 'executivo'
}
df['senioridade'] = df['senioridade'].replace(traducao_senioridade)

traducao_contrato = {
    'FT': 'Tempo Integral',
    'PT': 'Meio Período',
    'CT': 'Contrato',
    'FL': 'Freelancer'
}
df['contrato'] = df['contrato'].replace(traducao_contrato)

traducao_tamanho_empresa = {
    'S': 'Pequena',
    'M': 'Média',
    'L': 'Grande'
}
df['tamanho_empresa'] = df['tamanho_empresa'].replace(traducao_tamanho_empresa)

traducao_remota = {
    0: 'Presencial',
    50: 'Híbrido',
    100: 'Remoto'
}
df['remota'] = df['remota'].replace(traducao_remota)

# print(df.head(10))  # Exibe as 10 primeiras linhas do DataFrame
# print(df.describe(include='object'))  # Mostra estatísticas descritivas das colunas numéricas
# print(df.info())  # Exibe informações gerais sobre o DataFrame
# print(df.shape)  # Mostra o formato (linhas, colunas) do DataFrame
# print(df.columns)  # Lista os nomes das colunas do DataFrame
# print(df["remota"].value_counts())  # Conta os valores únicos na coluna 'remota'
# print(df.isnull().sum())  # Verifica valores nulos no DataFrame
# print(df[df.isnull().any(axis=1)])  # Verifica se há alguma linha com valores nulos

df_limpo = df.dropna()
print(df_limpo.info())  # Exibe informações gerais sobre o DataFrame limpo
# print(df_limpo.isnull().sum())  # Verifica valores nulos no DataFrame limpo

df_limpo = df_limpo.assign(ano = df_limpo['ano'].astype('int64'))
print(df_limpo.head(10))
print(df_limpo.info())  # Exibe informações gerais sobre o DataFrame limpo após a conversão do tipo da coluna 'ano' para int64