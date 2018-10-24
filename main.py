#! /usr/local/bin/python3.7
# -*- coding: utf-8
import algorithm
import warnings
warnings.filterwarnings('ignore')

G, pos, destination_nodes, g_edge_labels = algorithm.generate_network_topology()
shortest_path_tree = algorithm.generate_shortest_path_tree(G, pos, destination_nodes, g_edge_labels)
steiner_tree = algorithm.generate_steiner_tree(G, pos, destination_nodes, g_edge_labels)
widest_shortest_path = algorithm.generate_widest_shortest_path(G, pos, destination_nodes, g_edge_labels)

# Widest Shortest Path
# maximum_spanning_tree = nx.maximum_spanning_tree(G)
# nx.draw_networkx(maximum_spanning_tree, pos, node_color=NODE_COLOR)
# nx.draw_networkx_nodes(G, pos, [0], node_color=SOURCE_NODE_COLOR)
# nx.draw_networkx_nodes(G, pos, destination_node_list, node_color=DESTINATION_NODE_COLOR)
# nx.draw_networkx_edge_labels(G, pos, g_edge_labels)
# plt.axis('off')
# plt.show()

