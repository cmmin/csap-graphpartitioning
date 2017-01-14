import graphviz as gv

def _loadSocialNetworkGroup(path):
    group = {}

    with open(path, 'r') as f:
        vertexID = 1
        for line in f:
            line = line.strip()
            if(len(line)):
                try:
                    group[vertexID] = int(line)
                except ValueError as err:
                    print(line)
                vertexID += 1

    return group

def socialNetworkToD3JSON(graph, partitionsFile, outFile):
    partitions = _loadSocialNetworkGroup(partitionsFile)

    json = '{\n  "nodes": [\n'

    isFirst = True
    for node in graph.nodes:
        if isFirst == False:
            json += ",\n"
        k = partitions[node]
        json += '    {"id":"' + str(node) + '", "group":' + str(k) + '}'
        isFirst = False

    json += '\n  ],\n  "links": [\n'

    existingEdges = []

    isFirst = True
    for node in graph.nodes:
        for edge in graph.edges[node]:
            # compute edgecode
            edgecode = 'n' + str(node) + 'n' + str(edge)
            if(edge < node):
                edgecode = 'n' + str(edge) + 'n' + str(node)

            if edgecode in existingEdges:
                continue
            else:
                existingEdges.append(edgecode)

            if isFirst == False:
                json += ",\n"


            json += '    {"source": "' + str(node) + '", "target": "' + str(edge) + '", "value":1}'

            isFirst = False
    json += "\n  ]\n}"

    with open(outFile, 'w+') as f:
        f.write(json)

def socialNetworkToDot(graph, outpath, debug=False):
    dot = gv.Graph(format='svg')

    for node in graph.nodes:
        dot.node(str(node), str(node))

    existingEdges = []

    if debug:
        print("Populating Dot Graph")

    for node in graph.nodes:
        for edge in graph.edges[node]:
            # compute edgecode
            edgecode = 'n' + str(node) + 'n' + str(edge)
            if(edge < node):
                edgecode = 'n' + str(edge) + 'n' + str(node)

            if edgecode in existingEdges:
                continue
            else:
                existingEdges.append(edgecode)

            dot.edge(str(node), str(edge))

    if debug:
        print("Rendering Dot Graph")

    dot.render(filename=outpath)

    if debug:
        print("Dot Graph Rendered")
