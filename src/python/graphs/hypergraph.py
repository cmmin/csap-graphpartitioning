
# http://nbviewer.jupyter.org/github/atteroTheGreatest/hypergraph/blob/master/notebooks/hypergraphs_1.ipynb?create=1

# clique: https://en.wikipedia.org/wiki/Clique_(graph_theory)
import networkx as nx
import matplotlib.pyplot as plt

def hyperToGraph():
    xpins = [0, 5, 7, 11, 13, 15, 19, 21, 25, 27, 29, 31]
    pins = [2, 3, 5, 6, 9, 0, 1, 0, 1, 2, 3, 1, 3, 4, 5, 4, 5, 6, 7, 6, 7, 8, 9, 10, 11, 8, 11, 8, 10, 2, 5]

    print(len(xpins))
    print(len(pins))

    vertices = {}

    for xpinID in range(0, len(xpins)):
        pinIDStart = xpins[xpinID]

        if(xpinID + 1 == len(xpins)):
            # last
            break

        pinIDEnd = xpins[xpinID + 1]

        hyperedges = []
        for pinID in range(pinIDStart, pinIDEnd):
            #s += str(pins[pinID]) + ','
            hyperedges.append(pins[pinID])

        print("Hyperedges: ", hyperedges)

        while len(hyperedges) > 0:
            # take the last element
            vertex = hyperedges[len(hyperedges) - 1]
            hyperedges.pop()

            for other in hyperedges:
                addEdge(vertices, vertex, other)

    for vertex in vertices:
        print("Vertex", vertex, "edges:", vertices[vertex])


    G = nx.Graph()
    G.add_nodes_from(list(vertices.keys()))
    # add edges
    for vertex in vertices:
        for edge in vertices[vertex]:
            G.add_edge(vertex, edge)

    return (G, vertices)

def addEdge(vertices, v1, v2):
    if v1 not in vertices:
        vertices[v1] = []
    if v2 not in vertices:
        vertices[v2] = []

    if v2 not in vertices[v1]:
        vertices[v1].append(v2)
    if v1 not in vertices[v2]:
        vertices[v2].append(v1)


def graphToHypergraph(graph):
    c = nx.find_cliques(graph)
    print(list(c))
