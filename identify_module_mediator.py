# This python script identify the mediator genes that connect two gene lists in a network.
# Usage: python identify_module_mediator.py <network.gml> <ppi> (default: HumanInteractome_350k.tsv) 

import sys
import networkx as nx
import scr.ppi as ppi
import numpy as np
import scr.mapgene as mg

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python identify_module_mediator.py <network.gml> <ppi> (default: HumanInteractome_350k.tsv)")
        sys.exit(1)

    network_gml = sys.argv[1]
    if len(sys.argv) > 2:
        ppi_file = sys.argv[2]
    else:
        ppi_file = 'scr/ppi/HumanInteractome_350k.tsv'

    # Load the network
    G_module = nx.read_gml(network_gml)

    # Load the PPI network
    G_PPI = ppi.Interactome(pathG=ppi_file).G

    # 1. get the pairwise distance between all nodes in G_module
    # get nodes in G_module
    nodes = list(G_module.nodes())
    # compute pairwise distance of nodes in G_PPI
    m_distance = np.zeros((len(nodes), len(nodes)))
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            try:
                m_distance[i, j] = nx.shortest_path_length(G_PPI, nodes[i], nodes[j])
            except nx.NetworkXNoPath:
                m_distance[i, j] = np.inf
            m_distance[j, i] = m_distance[i, j]
    
    # 2. get the node pairs eligible for mediator identification. (distance = 2 and do not have path in G_module)
    eligible_pairs = []
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if m_distance[i, j] == 2:
                eligible_pairs.append((nodes[i], nodes[j]))
    
    # check if the eligible pairs have path in G_module
    for pair in eligible_pairs:
        try:
            path = nx.shortest_path(G_module, pair[0], pair[1])
            # print(f"Path between {pair[0]} and {pair[1]}: {path}")
            eligible_pairs.remove(pair)
        except nx.NetworkXNoPath:
            pass
    # print(f"Number of eligible pairs: {len(eligible_pairs)}")
    
    # 3. identify the mediator genes for each eligible pair
    arr_mediator_genes = []
    for pair in eligible_pairs:
        # get all shortest paths between the pair
        shortest_paths = list(nx.all_shortest_paths(G_PPI, pair[0], pair[1]))
        # get the mediator genes
        mediator_genes = set()
        for path in shortest_paths:
            mediator_genes.update(path[1:-1])
        arr_mediator_genes.append(mediator_genes)
    
    # 4. identify mediator genes for all eligible pairs
    arr_mediator_gene = [] # the mediator genes used for linking pairs
    arr_pairsLinked = [] # the pairs linked by the mediator genes

    # while eligible pairs is not empty
    while len(eligible_pairs) > 0:
        # get the frequency of mediator genes in arr_mediator_genes
        mediator_freq = {}
        for mediator_genes in arr_mediator_genes:
            for gene in mediator_genes:
                mediator_freq[gene] = mediator_freq.get(gene, 0) + 1
        # sort mediator_freq by frequency
        sorted_mediator_freq = sorted(mediator_freq.items(), key=lambda x: x[1], reverse=True)
        # get the mediator gene with the highest frequency
        mediator_gene = sorted_mediator_freq[0][0]
        # add the mediator gene to arr_mediator_gene
        # print(f"Mediator gene: {mediator_gene}")
        arr_mediator_gene.append(mediator_gene)
        # get the pairs in eligible_pairs linked by the mediator gene and remove them from eligible pairs
        pairsLinked = []
        arr_linked_pairs_ids = []
        for i in range(len(eligible_pairs)):
            if mediator_gene in arr_mediator_genes[i]:
                pairsLinked.append(eligible_pairs[i])
                arr_linked_pairs_ids.append(i)
        arr_pairsLinked.append(pairsLinked)
        # remove the linked pairs from eligible pairs and arr_mediator_genes based on arr_linked_pairs_ids 
        for i in sorted(arr_linked_pairs_ids, reverse=True):
            eligible_pairs.pop(i)
            arr_mediator_genes.pop(i)
        # print(pairsLinked)
        # print(f"Number of eligible pairs: {len(eligible_pairs)}")
        # print('-----------------------------------')
    
    # 5. add mediator genes to the network with edges to the linked pairs
    mappingGene = mg.init_geneName_mapping()
    # print(arr_mediator_gene)
    for i in range(len(arr_mediator_gene)):
        mediator_gene = arr_mediator_gene[i]
        pairsLinked = arr_pairsLinked[i]
        # add mediator gene to the network, with attributes symbol and query equal to "network_gml".split('.')[0] + "_mediator"
        # print(f"Mediator gene: {mediator_gene}")
        G_module.add_node(mediator_gene + "_mediator", symbol=mg.map_NCBI_to_HGNC_to_symbol(mediator_gene, mappingGene), query=network_gml.split('.')[0] + "_mediator")
        # add edges between mediator gene and linked pairs with attribute query equal to "network_gml".split('.')[0] + "_mediator"
        for pair in pairsLinked:
            # check if mediator_gene, pair[0] is not in G_module
            if not G_module.has_edge(mediator_gene + "_mediator", pair[0]):
                G_module.add_edge(mediator_gene + "_mediator", pair[0], query=network_gml.split('.')[0] + "_mediator")
            # check if mediator_gene, pair[1] is not in G_module
            if not G_module.has_edge(mediator_gene + "_mediator", pair[1]):
                G_module.add_edge(mediator_gene + "_mediator", pair[1], query=network_gml.split('.')[0] + "_mediator")
    
    # 6. save the network with mediator genes
    output_gml = "mediated_" + network_gml
    nx.write_gml(G_module, output_gml)
    # print(f"Mediated network saved to {output_gml}")