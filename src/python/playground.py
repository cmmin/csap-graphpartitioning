import graphs.metisgraph as mg


if __name__ == '__main__':
    s = "101"
    #mg.checkGraphFormatString(s)
    path = '../../data/oneshot_fennel_weights.txt'

    graph = mg.MetisGraph(path)
    graph.printData()


    for vID in graph.vertices:
        vertex = graph.vertices[vID]
        vertex.printData(concise=False)
        if vID > 10:
            break
        if vID == 1:
            print(vertex.hasEdge(710))
            print(graph.vertices[710].hasEdge(2))
