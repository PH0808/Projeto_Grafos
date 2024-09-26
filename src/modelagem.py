import pandas as pd

# Carrega o arquivo CSV
df = pd.read_csv(r"../rsc/dados_original/201809_CPGF.csv", encoding='latin1', delimiter=';')

# O resto do código permanece o mesmo
# Filtra as linhas onde 'NOME FAVORECIDO' não é igual a 'Sigiloso', 'NÃO SE APLICA' ou 'SEM INFORMACAO'
# df = df[~df['NOME FAVORECIDO'].isin(['Sigiloso', 'NAO SE APLICA', 'SEM INFORMACAO'])]

df['VALOR TRANSAÇÃO'] = df['VALOR TRANSAÇÃO'].str.replace(',', '.').astype(float)

vertices = pd.unique(pd.concat([df['NOME ÓRGÃO SUPERIOR'], df['NOME FAVORECIDO']]))

# Criando dataframes para os vertices
vertices_df = pd.DataFrame(vertices, columns=['Id'])
vertices_df['Label'] = vertices_df['Id']  # A coluna Label será igual à Id

# Lidar com duplicatas nas arestas (se houver múltiplas, somamos os pesos)
arestas_df = df[['NOME ÓRGÃO SUPERIOR', 'NOME FAVORECIDO', 'VALOR TRANSAÇÃO']]
arestas_df.columns = ['Source', 'Target', 'Weight']

# Agrupar por 'Source' e 'Target' para combinar arestas duplicadas (somar os pesos)
arestas_df = arestas_df.groupby(['Source', 'Target'], as_index=False).agg({'Weight': 'sum'})

# 4. Salvar os arquivos para o Gephi
vertices_df.to_csv('../rsc/vertices.csv', index=False)
arestas_df.to_csv('../rsc/arestas.csv', index=False)

print(arestas_df['Target'].value_counts())
