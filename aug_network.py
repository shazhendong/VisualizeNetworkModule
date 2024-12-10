# This py aug network_1 one with network_2 and return the merged network.
# Usage: python aug_network.py <network_1> <network_2>
# Output: merged.gml
# The nodes and edges of network_2 will be added to network_1, if they are not already present in network_1.s

import sys
import networkx as nx

if __name__ == "__main__":
    file_network_1 = sys.argv[1]
    file_network_2 = sys.argv[2]

    print('Augmenting network: ' + file_network_1 + ' with network: ' + file_network_2)

    # read network_1 and network_2
    G1 = nx.read_gml(file_network_1)
    G2 = nx.read_gml(file_network_2)

    # print number of nodes and edges in each network
    print('Network 1: ' + str(len(G1.nodes())) + ' nodes, ' + str(len(G1.edges())) + ' edges')
    print('Network 2: ' + str(len(G2.nodes())) + ' nodes, ' + str(len(G2.edges())) + ' edges')

    # augment nodes in network_1 with nodes in network_2
    for node in G2.nodes():
        if node not in G1.nodes():
            G1.add_node(node, **G2.nodes[node])

    # augment edges in network_1 with edges in network_2
    for edge in G2.edges():
        if edge not in G1.edges():
            G1.add_edge(edge[0], edge[1], **G2.edges[edge])
    
    # write augmented network
    outputFileName = 'augmented.gml'
    nx.write_gml(G1, outputFileName)