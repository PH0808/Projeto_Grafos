import pandas as pd
import networkx as nx

df = pd.read_csv("../rsc/arestas.csv")

# Cria o grafo
G = nx.Graph()

for _, linha in df.iterrows():
    orgao_superior: str = linha['Source']
    empresa: str = linha['Target']
    valor_gasto: float = linha['Weight']
    # Adiciona o vertice e arestas ao grafo
    G.add_edge(orgao_superior, empresa, weight=valor_gasto)

# Criação do arquivo .gexf
nx.write_gexf(G, "../rsc/grafo.gexf")

# 1. Grau de centralidade
centralidade_grau = nx.degree_centrality(G)

# 2. Intermediação
intermediacao = nx.betweenness_centrality(G)

proximidade = nx.closeness_centrality(G)

# 3. Componentes conexas
componentes_conexas = list(nx.connected_components(G))

# 4. Identificação de comunidades
comunidades = nx.algorithms.community.greedy_modularity_communities(G)
# for i, comunidade in enumerate(comunidades):
#     print(f"Comunidade {i + 1}:", comunidade)
print(len(comunidades))

empresas = df['Target']

# Pegando apenas as centralidades, intermediações e proximidades das empresas.
centralidade_empresas = {e: centralidade_grau[e]
                         for e in empresas if e in centralidade_grau}

intermediacao_empresas = {e: intermediacao[e]
                          for e in empresas if e in intermediacao}

proximidade_empresas = {e: proximidade[e]
                        for e in empresas if e in proximidade}

print("quantidade de empresas: ", len(empresas))

# Calculando as médias.
media_centralidade = sum(centralidade_empresas.values()
                         ) / len(centralidade_empresas)

media_intermediacao = sum(intermediacao_empresas.values()
                          ) / len(intermediacao_empresas)

media_proximidade = sum(proximidade_empresas.values()
                        ) / len(proximidade_empresas)

# Vendo as empresas que estão acima da média.
acima_media_centralidade = {e: p for e, p in centralidade_empresas.items()
                            if p > media_centralidade}

acima_media_intermediacao = {e: p for e, p in intermediacao_empresas.items()
                             if p > media_intermediacao}

acima_media_proximidade = {e: p for e, p in proximidade_empresas.items()
                           if p > media_proximidade}

print('quantidade empresas acima da media em centralidade: ',
      len(acima_media_centralidade))

print('quantidade empresas acima da media em intermediacao: ',
      len(acima_media_intermediacao))

print('quantidade empresas acima da media em proximidade: ',
      len(acima_media_proximidade))