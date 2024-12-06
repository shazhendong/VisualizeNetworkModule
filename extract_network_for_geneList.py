# This py python file extract subnetwork for a list of genes from a network file.
# Input: geneList ([geneListName].txt), networkFile (default: scr/ppi/HumanInteractome_350k.tsv), outputFileName (default: [geneListName].gml)

import sys
import scr.mapgene as mg
import scr.ppi as ppi

def process_geneList(file_geneList):
    geneList = []
    with open(file_geneList, 'r') as f: # read geneList and return a list of gene ncbi ids
        for line in f:
            geneList.append(line.strip())
    
    geneList = list(set(geneList)) # remove duplicates
    MappingGene = mg.init_geneName_mapping() # initialize MappingGene
    geneList_ncbi = [mg.map_symbol_to_HGNC_to_NCBI(gene, MappingGene) for gene in geneList] # map geneList to NCBI
    print('Following entries are not mapped: ' + str([geneList[i] for i in range(len(geneList_ncbi)) if geneList_ncbi[i] is None])) # print the corresponding entries in geneList that return None
    geneList_ncbi = [gene for gene in geneList_ncbi if gene is not None] # remove None entries
    return geneList_ncbi

def extract_network_for_geneList(geneList_ncbi, file_network):
    # load network class
    Interactome = ppi.Interactome(pathG=file_network)
    # get subnetwork
    subnetwork = Interactome.get_subnetwork(geneList_ncbi)
    return subnetwork

def annotate_network(subnetwork, query_name):
    # annotate the subnetwork. for nodes add symbol attribute and query attribute, for edges add query attributes. return the annotated subnetwork
    MappingGene = mg.init_geneName_mapping() # initialize MappingGene
    # annotate nodes
    for node in subnetwork.nodes():
        symbol = mg.map_NCBI_to_HGNC_to_symbol(node, MappingGene)
        subnetwork.nodes[node]['symbol'] = symbol
        subnetwork.nodes[node]['query'] = query_name
    # annotate edges
    for edge in subnetwork.edges():
        subnetwork.edges[edge]['query'] = query_name
    return subnetwork
    

# main function
if __name__ == "__main__":
    # read parameters
    file_geneList = sys.argv[1]
    if len(sys.argv) > 2:
        file_network = sys.argv[2]
    else:
        file_network = 'scr/ppi/HumanInteractome_350k.tsv'

    print('Extracting network for gene list: ' + file_geneList + ' from network file: ' + file_network)

    # read geneList
    geneList_ncbi = process_geneList(file_geneList)
    print('Gene list: ' + str(geneList_ncbi))

    # extract subnetwork
    subnetwork = extract_network_for_geneList(geneList_ncbi, file_network)
    
    # annotate subnetwork
    subnetwork = annotate_network(subnetwork, file_geneList.split('.')[0])

    # write subnetwork
    outputFileName = file_geneList.split('.')[0] + '.gml'
    ppi.write_gml(subnetwork, outputFileName)



