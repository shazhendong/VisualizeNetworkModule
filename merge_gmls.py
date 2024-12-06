# This python script merge the gmls files into one gmls file.
# Usage: python merge_gmls.py <gml_file_1> <gml_file_2> ... <gml_file_n>
# Output: merged.gml

import sys
import scr.ppi as ppi


if __name__ == "__main__":
    gml_files = sys.argv[1:]
    print('Merging gml files: ' + str(gml_files))

    # read gml files
    gmls = [ppi.read_gml(file_gml) for file_gml in gml_files]

    # print number of nodes and edges in each gml
    for i in range(len(gmls)):
        print('Gml ' + str(i) + ': ' + str(len(gmls[i].nodes())) + ' nodes, ' + str(len(gmls[i].edges())) + ' edges')
    
    # merge gmls
    merged = gmls[0]
    for i in range(1, len(gmls)):
        merged = ppi.augment_networks(merged, gmls[i])
    
    # write merged gml
    outputFileName = 'merged.gml'
    ppi.write_gml(merged, outputFileName)