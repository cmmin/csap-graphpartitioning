import os
import os.path


if __name__ == '__main__':
    dataDir = '../../../../data/'

    fixedPartitions = os.path.join(dataDir, 'oneshot_fennel_partitions_fixed.txt')
    partitions = os.path.join(dataDir, 'oneshot_fennel_partitions.txt')

    vertexPartitions = []
    vertexPartitionsFixed = []

    with open(partitions, 'r') as f:
        for line in f:
            line = line.strip()
            partition = int(line)
            vertexPartitions.append(partition)

    with open(fixedPartitions, 'r') as f:
        for line in f:
            line = line.strip()
            partition = int(line)
            vertexPartitionsFixed.append(partition)

    nPart = len(vertexPartitions)
    nPartFixed = len(vertexPartitionsFixed)

    if(nPart == nPartFixed):
        print("Vertices Found =", nPart)
    else:
        print("Number of vertices in fixed and nonfixed files don't match:", nPart, "!=", nPartFixed)
        exit()

    nDifferences = 0
    vertexID = 0
    for partition in vertexPartitions:
        fixedPartition = vertexPartitionsFixed[vertexID]

        if(partition == fixedPartition):
            pass
        else:
            nDifferences += 1

        vertexID += 1

    print("Differences in vertex partition allocations=", nDifferences)
