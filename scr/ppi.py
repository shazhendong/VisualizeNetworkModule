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