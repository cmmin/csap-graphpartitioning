from utilities.clibrary_loader import CLibrary
from scotch.scotch import LibScotch
from ctypes import cdll

from graphs.social_network import SocialNetworkGraph

import networkit

if __name__ == '__main__':
    scotch = LibScotch("../../tools/scotch/lib/macOS/libscotch.dylib")
    print(scotch.version())

    # load socialnetwork using networkit
    nkGraph = networkit.graphio.METISGraphReader().read("../../data/socialNetwork_all_edges.txt")
