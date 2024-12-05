import pickle

def init_geneName_mapping(data_dir='scr/mapgene/MappingGene.pkl'):
    with open(data_dir, 'rb') as f:
        MappingGene = pickle.load(f)
    return MappingGene

def map_symbol_to_HGNC_to_NCBI(symbol, MappingGene):
    # return a NCBI Gene ID
    # if symbol is not in MappingGene['S2H'], return None and print warning
    if symbol not in MappingGene['S2H']:
        return None
    HGNC = MappingGene['S2H'][symbol]
    if HGNC not in MappingGene['H2E']:
        return None
    NCBI = MappingGene['H2E'][HGNC]
    return NCBI

def map_NCBI_to_HGNC_to_symbol(NCBI, MappingGene):
    # return a symbol
    # if NCBI is not in MappingGene['E2H'], return None and print warning
    if NCBI not in MappingGene['E2H']:
        return None
    HGNC = MappingGene['E2H'][NCBI]
    if HGNC not in MappingGene['H2S']:
        return None
    symbol = MappingGene['H2S'][HGNC]
    return symbol