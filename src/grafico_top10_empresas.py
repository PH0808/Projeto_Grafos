import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("../rsc/arestas.csv")

filtro_empresas = ["Sigiloso", "NAO SE APLICA", "SEM INFORMACAO"]
empresas = df[~df['Target'].isin(filtro_empresas)]['Target'].unique()
# Cria o grafo
G = nx.Graph()

for _, linha in df.iterrows():
    orgao_superior: str = linha['Source']
    empresa: str = linha['Target']
    valor_gasto: float = linha['Weight']
    # Adiciona o vertice e arestas ao grafo
    if empresa == "Sigiloso" or empresa == "NAO SE APLICA" or empresa == "SEM INFORMACAO":
        continue

    G.add_edge(orgao_superior, empresa, weight=valor_gasto)

centralidade = nx.degree_centrality(G)
intermediacao = nx.betweenness_centrality(G)
proximidade = nx.closeness_centrality(G)

contratos_por_empresa = {}
for v1, v2 in G.edges():
    fornecedor = v1 if v1 in df['Target'].unique() else v2
    if fornecedor not in contratos_por_empresa:
        contratos_por_empresa[fornecedor] = 0
    contratos_por_empresa[fornecedor] += 1

contratos_ordenados = sorted(contratos_por_empresa.items(), key=lambda x: x[1], reverse=True)
top_10_empresas = [empresa for empresa, _ in contratos_ordenados[:10]]

centralidade_top10 = {e: centralidade[e] for e in top_10_empresas if e in centralidade}
intermediacao_top10 = {e: intermediacao[e] for e in top_10_empresas if e in intermediacao}
proximidade_top10 = {e: proximidade[e] for e in top_10_empresas if e in proximidade}


def plot_metricas(metricas, titulo):
    empresas = list(metricas.keys())
    valores = list(metricas.values())

    plt.figure(figsize=(10, 6))
    x_pos = np.arange(len(empresas))

    plt.bar(x_pos, valores)
    plt.xticks(x_pos, empresas, rotation=45, ha='right', fontsize=10)
    plt.ylabel(titulo)
    plt.title(f'{titulo} das 10 Empresas com Mais Contratos')
    plt.tight_layout()
    plt.show()

plot_metricas(centralidade_top10, 'Centralidade')
plot_metricas(intermediacao_top10, 'Intermediação')
plot_metricas(proximidade_top10, 'Proximidade')