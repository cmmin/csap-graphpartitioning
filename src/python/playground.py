import scotch.graph_mapper as gm

import graphs.hypergraph as hg
import graphs.metisgraph as mg

import scotch.io as sio
import scotch.scotch as sct

import networkx as nx
import matplotlib.pyplot as plt

import utilities.system_utils as sysutils

import patoh.patoh as pat

if __name__ == '__main__':
    libPath = pat.defaultLibraryPath()
    print(libPath)
    patoh = pat.LibPatoh(libPath)
    #print(patoh.version())

    exit()
    libraryPath = sct.defaultLibraryPath()
    print(libraryPath, sct.testSetup(libraryPath))
    #exit()
    #mg.checkGraphFormatString(s)
    metisPath = 'csap-graphpartitioning/data/oneshot_fennel_weights.txt'
    '''
    if sysutils.getOS() == sysutils.OS.macOS:
        scotchPath = "../../tools/scotch/lib/macOS/libscotch.dylib"
    if sysutils.getOS() == sysutils.OS.linux:
        scotchPath = "/usr/local/lib/scotch/libscotch.so"
        #scotchPath = "/home/voreno/Downloads/scotch_6.0.4/src/libscotch/libscotch.so"
    '''
    import os
    #print(os.path.isfile(scotchPath), scotchPath)

    print(os.path.isfile(metisPath), metisPath)
    print(os.getcwd())
    metisPath

    metisG = mg.MetisGraph(metisPath)
    nxG = metisG.toNetworkxGraph()

    data = sio.ScotchGraphArrays();
    data.fromNetworkxGraph(nxG)

    #mapper = gm.partitionMetis(libraryPath, metisPath)
    mapper = gm.GraphMapper(scotchLibPath = libraryPath, numPartitions = 4)
    mapper.initialize(data)
    ok = mapper.graphMap()

    data.debugPrint()
    print(ok, mapper.scotchData._parttab)

    mapper.delObjects()

    print(mapper.scotchLib.architecture)
