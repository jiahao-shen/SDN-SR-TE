import networkx as nx
import networkx.algorithms.approximation
import matplotlib.pyplot as plt
import random
#
# G = nx.erdos_renyi_graph(15, 0.3)
# for edge in G.edges:
#     G.add_weighted_edges_from([(edge[0], edge[1], random.randint(1, 10))])
#
# edge_labels = nx.get_edge_attributes(G, "weight")
# pos = nx.spring_layout(G)
# nx.draw_networkx(G, pos)
# nx.draw_networkx_edge_labels(G, pos, edge_labels)
# print(nx.shortest_path(G, 0, 3, weight='weight'), nx.shortest_path_length(G, 0, 3, weight='weight'))
# plt.axis("off")
# plt.show()
