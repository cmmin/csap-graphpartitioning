from utilities.clibrary_loader import CLibrary
from scotch.scotch import LibScotch
from ctypes import cdll

from graphs.social_network import SocialNetworkGraph

if __name__ == '__main__':
    scotch = LibScotch("../tools/scotch/lib/macOS/libscotch.dylib")
    print(scotch.version())
    #lib = CLibrary("../tools/scotch/lib/macOS/libscotch.dylib")
    #lib.load()
    snGraph = SocialNetworkGraph()
    snGraph.load("../data/socialNetwork.txt")

    print(snGraph.numNodes())
    print(snGraph.numEdges())

    snGraph.save("../data/socialNetwork_out.txt")
