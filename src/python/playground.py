import scotch.graph_mapper as gm


if __name__ == '__main__':
    s = "101"
    #mg.checkGraphFormatString(s)
    metisPath = '../../data/oneshot_fennel_weights.txt'
    scotchPath = "../../tools/scotch/lib/macOS/libscotch.dylib"

    mapper = gm.partitionMetis(scotchPath, metisPath)
    
