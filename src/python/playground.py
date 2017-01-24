import scotch.graph_mapper as gm

import graphs.hypergraph as hg
import graphs.metisgraph as mg

import scotch.io as sio

import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':
    s = "101"
    #mg.checkGraphFormatString(s)
    metisPath = '../../data/oneshot_fennel_weights.txt'
    scotchPath = "../../tools/scotch/lib/macOS/libscotch.dylib"

    metisG = mg.MetisGraph(metisPath)
    nxG = metisG.toNetworkxGraph()

    data = sio.ScotchGraphArrays();
    data.fromNetworkxGraph(nxG)

    print(data.edgetab)

    #print(nxG.nodes())
    #print(nxG.edges())

    exit()
    mapper = gm.partitionMetis(scotchPath, metisPath)

    exit()
    g, vertices = hg.hyperToGraph()

    labels = {}
    for node in g.nodes():
        labels[node] = str(node)
    nx.draw(g, labels=labels)
    plt.savefig("g.png")
    hg.graphToHypergraph(g)
