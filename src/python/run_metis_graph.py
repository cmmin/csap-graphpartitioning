from graphs.social_network import SocialNetworkGraph
from visualisation.dot import socialNetworkToDot, socialNetworkToD3JSON

if __name__ == '__main__':
    graph = SocialNetworkGraph()
    graph.load("../../data/socialNetwork_out.txt")

    socialNetworkToD3JSON(graph, "../../data/oneshot_fennel_partitions.txt" ,"../../data/socialnetwork.json")
