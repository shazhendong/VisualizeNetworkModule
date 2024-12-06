import numpy as np
import networkx as nx
import random

class Interactome(object):
    def __init__(self, pathG="scr/ppi/HumanInteractome_350k.tsv"):
        self.G = nx.read_edgelist(pathG, delimiter="\t", data=[("src", str), ("typ", str)])
        self.G.remove_edges_from(nx.selfloop_edges(self.G))

    def get_PPI(self):
        # remove self loops
        self.G.remove_edges_from(nx.selfloop_edges(self.G))
        return self.G

    def get_subnetwork(self, gene_list):
        # remove None from gene_list
        gene_list = [gene for gene in gene_list if gene is not None]
        G = self.get_PPI()
        return G.subgraph(gene_list)

def write_gml(subnetwork, outputFileName):
    nx.write_gml(subnetwork, outputFileName)

def read_gml(file_gml):
    return nx.read_gml(file_gml)

def augment_networks(net_1, net_2, dup_edge=True):
    # augment net_1 with net_2. return the augmented network
    # dup_edge: if True, duplicate edges are allowed. if False, duplicate edges are not allowed
    # add nodes
    for node in net_2.nodes():
        if node not in net_1.nodes():
            # add node to net_1
            net_1.add_node(node)
            # add attributes to node in net_1
            for key in net_2.nodes[node].keys():
                net_1.nodes[node][key] = net_2.nodes[node][key]
        else:
            # augment attributes of node in net_1
            for key in net_2.nodes[node].keys():
                # get existing attributes in net_1
                values = net_1.nodes[node].get(key).split(',')
                # get new attributes in net_2
                values_new = net_2.nodes[node].get(key).split(',')
                for value in values_new:
                    if value not in values:
                        values.append(value)
                sorted_values = sorted(values)
                # update attributes in net_1
                net_1.nodes[node][key] = ','.join(sorted_values)
    # add edges
    for edge in net_2.edges():
        if edge not in net_1.edges():
            # add edge to net_1 including attributes
            net_1.add_edge(edge[0], edge[1])
            for key in net_2.edges[edge].keys():
                net_1.edges[edge][key] = net_2.edges[edge][key]
        else:
            #  augment attributes of edge in net_1
            for key in net_2.edges[edge].keys():
                # get existing attributes in net_1
                values = net_1.edges[edge].get(key).split(',')
                # get new attributes in net_2
                values_new = net_2.edges[edge].get(key).split(',')
                for value in values_new:
                    if value not in values:
                        values.append(value)
                sorted_values = sorted(values)
                # update attributes in net_1
                net_1.edges[edge][key] = ','.join(sorted_values)
    return net_1