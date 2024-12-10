# This python script expand node based on a specific attribute. The values in that attribute will be unpacked into separate attributes.
# Usage: python expand_nodes.py <input_gml> <node_attribute>
# Output: expanded-node_<node_attribute>_<input_gml>

import networkx as nx
import sys

def expand_nodes(input_gml, node_attribute):
    # Step 1: Read the GML file into a graph use read MultiGraph to allow multiple edges between nodes
    G = nx.read_gml(input_gml)

    # Print the number of nodes and edges
    print(f"Loaded a graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    # Step 2: Collect nodes to modify in a separate list
    nodes_to_modify = []
    for node, data in G.nodes(data=True):
        if node_attribute in data:
            values = data[node_attribute].split(",")  # Split values by comma
            if len(values) > 1:
                nodes_to_modify.append((node, data))  # Collect nodes to modify
            else:
                G.nodes[node][node_attribute + "_" + values[0].strip()] = 1
                G.nodes[node]["expanded_by_" + node_attribute] = 0 # only one value, no need to expand
    
    # Step 3: add node attribute
    for node, data in nodes_to_modify:
        # get attribute value from the node
        value = data[node_attribute]
        for v in value.split(","):
            G.nodes[node][node_attribute + "_" + v.strip()] = 1
        # add attribute to the node to indicate this node has been expanded by the attribute
        G.nodes[node]["expanded_by_" + node_attribute] = 1
    
    # Print the number of nodes and edges after expansion
    print(f"Expanded to {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    return G

if __name__ == "__main__":
    if len(sys.argv) > 3:
        print("Usage: python expand_nodes.py <input_gml> <node_attribute>")
        sys.exit(1)

    input_gml = sys.argv[1]
    node_attribute = sys.argv[2]

    # Process the network
    expanded_graph = expand_nodes(input_gml, node_attribute)

    # Save the resulting network to a new GML file
    output_gml = "expanded-node_" + node_attribute + "_" + input_gml
    nx.write_gml(expanded_graph, output_gml)
    print(f"Expanded network saved to {output_gml}")