import scotch.graph_mapper as gm

import graphs.hypergraph as hg
import graphs.metisgraph as mg

import scotch.io as sio
import scotch.scotch as sct

import networkx as nx
import matplotlib.pyplot as plt

import utilities.system_utils as sysutils

if __name__ == '__main__':
    lP = sct.defaultLibraryPath()
    print(lP, sct.testSetup(lP))
    exit()
    #mg.checkGraphFormatString(s)
    metisPath = '../../data/oneshot_fennel_weights.txt'
    if sysutils.getOS() == sysutils.OS.macOS:
        scotchPath = "../../tools/scotch/lib/macOS/libscotch.dylib"
    if sysutils.getOS() == sysutils.OS.linux:
        scotchPath = "/usr/local/lib/scotch/libscotch.so"
        #scotchPath = "/home/voreno/Downloads/scotch_6.0.4/src/libscotch/libscotch.so"

    import os
    print(os.path.isfile(scotchPath))

    print(scotchPath)

    metisG = mg.MetisGraph(metisPath)
    nxG = metisG.toNetworkxGraph()

    data = sio.ScotchGraphArrays();
    data.fromNetworkxGraph(nxG)

    print(data.edgetab)

    mapper = gm.partitionMetis(scotchPath, metisPath)

    exit()
    g, vertices = hg.hyperToGraph()

    labels = {}
    for node in g.nodes():
        labels[node] = str(node)
    nx.draw(g, labels=labels)
    plt.savefig("g.png")
    hg.graphToHypergraph(g)
