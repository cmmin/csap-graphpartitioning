import graphs.metisgraph as mg
import scotch.io as sio
from scotch.scotch import LibScotch

if __name__ == '__main__':
    s = "101"
    #mg.checkGraphFormatString(s)
    path = '../../data/oneshot_fennel_weights.txt'

    graph = mg.MetisGraph(path)

    scotchArrays = sio.ScotchGraphArrays()
    scotchArrays.fromMetisGraph(graph)

    sgraph = LibScotch("../../tools/scotch/lib/macOS/libscotch.dylib")

    sgraph.createSCOTCHGraph()
    print(sgraph.buildSCOTCHGraphFromData(scotchArrays))
