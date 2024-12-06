import networkx as nx
import sys

def expand_edges(input_gml, edge_attribute):
    # Step 1: Read the GML file into a graph
    G = nx.read_gml(input_gml)

    # Print the number of nodes and edges
    print(f"Loaded a MultiGraph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    # Step 2: Transform the graph into a MultiGraph for multiple edges
    if not isinstance(G, nx.MultiGraph):
        G = nx.MultiGraph(G)

    # Step 3: Collect edges to modify in a separate list
    edges_to_modify = []
    for u, v, data in G.edges(data=True):
        if edge_attribute in data:
            values = data[edge_attribute].split(",")  # Split values by comma
            if len(values) > 1:
                edges_to_modify.append((u, v, data))  # Collect edges to modify

    # Step 4: Modify the graph
    for u, v, data in edges_to_modify:
        # Remove the original edge
        G.remove_edge(u, v)

        # Add a new edge for each value
        values = data[edge_attribute].split(",")
        for value in values:
            new_data = data.copy()
            new_data[edge_attribute] = value.strip()  # Remove extra spaces
            G.add_edge(u, v, **new_data)

    # Print the number of nodes and edges after expansion
    print(f"Expanded to {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    return G

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python expand_edges.py <input_gml> <edge_attribute>")
        sys.exit(1)

    input_gml = sys.argv[1]
    edge_attribute = sys.argv[2]

    # Process the network
    expanded_graph = expand_edges(input_gml, edge_attribute)

    # Save the resulting network to a new GML file
    output_gml = "expanded_" + edge_attribute + "_" + input_gml
    nx.write_gml(expanded_graph, output_gml)
    print(f"Expanded network saved to {output_gml}")
