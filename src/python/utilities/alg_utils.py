import numpy as np
import networkx as nx


def addEdgeToIndex(edges, uv):
    if uv[0] in edges:
        edges[uv[0]].append(uv[1])
    else:
        edges[uv[0]] = [uv[1]]

def uvOrder(node1, node2):
    if node1 < node2:
        return [node1, node2]
    else:
        return [node2, node1]

def randNumInRange(maxRangeVal):
    # zero is min rangeval
    if maxRangeVal <= 0:
        return 0

    val = 0
    while True:
        val = int(np.floor(abs(np.random.randn(1)[0]) * maxRangeVal))
        if val >= 0 and val <= maxRangeVal:
            break
    return val

def pickRandPartition(num_partitions):
    return randNumInRange(num_partitions - 1)

def delVirtualEdges(G, virtualEdges):
    for key in list(virtualEdges.keys()):
        for val in virtualEdges[key]:
            try:
                G.remove_edge(key, val)
            except Exception as err:
                pass

def minPartitionCounts(assignments, num_partitions):
    #print(assignments)
    partitions = {}
    for i in range(num_partitions):
        partitions[i] = 0

    for partition in assignments:
        if partition < 0:
            continue
        if partition in partitions:
            partitions[partition] += 1
        else:
            partitions[partition] = 1

    minCount = len(assignments) + 1
    minCountPartition = -1
    for key in list(partitions.keys()):
        if partitions[key] < minCount:
            minCount = partitions[key]
            minCountPartition = key

    if minCountPartition < 0:
        minCountPartition = pickRandPartition(num_partitions)

    return minCountPartition

def updateNodeMapping(G, otherG = None):
    G2 = nx.Graph()

    indexed = {}
    for i, n in enumerate(G.nodes()):
        indexed[n] = i

    for n in G.nodes():
        G2.add_node(indexed[n])

        try:
            weight = otherG.node[n]['weight']
            G2.node[indexed[n]]['weight'] = weight
        except Exception as e:
            pass

        for neighbor in G.neighbors(n):
            G2.add_edge(indexed[n], indexed[neighbor])

            try:
                weight = otherG[n][neighbor]['weight']
                G2[indexed[n]][indexed[neighbor]]['weight'] = weight
            except Exception as e:
                pass

    return G2


def getOtherNodeInPartition(currentNode, partition, arrived_nodes, assignments):
    partitionNodes = []
    for i in range(0, len(assignments)):
        if assignments[i] == partition:
            # collect nodeIDs that are of this partition and not current node
            if currentNode != arrived_nodes[i]:
                partitionNodes.append(i)

    if len(partitionNodes) == 0:
        return None

    # pick one of the nodes
    i = randNumInRange(len(partitionNodes) - 1)
    return arrived_nodes[partitionNodes[i]]

def getIndex(arr, val):
    for i, a in enumerate(arr):
        if a == val:
            return i
    return -1

if __name__ == '__main__':
    node = 3
    partition = 0
    assignments = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
    arrived_nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    for i in range(0, 10):
        otherN = getOtherNodeInPartition(node, partition, arrived_nodes, assignments)
        print(otherN)


    index = {}
    addEdgeToIndex(index, uvOrder(10,2))
    addEdgeToIndex(index, uvOrder(2,3))
    addEdgeToIndex(index, uvOrder(1,2))

    print(index)


    print(getIndex(arrived_nodes, 7))
