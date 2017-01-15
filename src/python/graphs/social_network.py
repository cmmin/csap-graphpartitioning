
class SocialNetworkGraph:
    ''' Class represents a social network file and handles read/write to file '''
    def __init__(self):
        self.nodes = []
        self.edges = {}

    def load(self, filePath):
        ''' load the social network file '''
        with open(filePath, 'r') as f:
            lineNum = 0
            numNodes = 0
            numEdges = 0
            for line in f:
                # clean the line of text, removing unwanted characters
                line = self._cleanLine(line)
                # split each line, to get its parts
                parts = line.split(" ")

                if(lineNum == 0):
                    # this is the first line in the file
                    numNodes = int(parts[0])
                    numEdges = int(parts[1])
                    print("Parsing social network file with " + str(numNodes) + " nodes and " + str(numEdges) + " edges.")
                else:
                    self.nodes.append(lineNum)
                    edges = []
                    for part in parts:
                        if(len(part) > 0):
                            edges.append(int(part))
                    self.edges[lineNum] =  edges
                # increment lineNum
                lineNum += 1

    def save(self, filePath):
        with open(filePath, 'w+') as f:
            # first line
            f.write(str(self.numNodes()) + " " + str(self.numEdges()))

            for node in self.nodes:
                s = ""
                for edge in self.edges[node]:
                    if(len(s) > 0):
                        s += " "
                    s += str(edge)
                f.write('\n' + s)

    def numNodes(self):
        return len(self.nodes)

    def numEdges(self):
        numEdges = 0
        for node in self.nodes:
            numEdges += len(self.edges[node])
        return int(numEdges / 2)

    def _cleanLine(self, line):
        line = line.replace("\n", "")
        line = line.replace("\r", "")
        return line
