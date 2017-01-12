#include "metis.h"

#include <iostream>
#include <fstream> // for reading file
#include <vector>


#include "utils.h"

namespace METIS {

  MetisEdge::MetisEdge(int u, int v, int weight)
  {
    if(u > v) {
      this->u = v;
      this->v = u;
    }
    else {
      this->u = u;
      this->v = v;
    }
    this->weight = weight;
  }

  std::pair<int, int> MetisEdge::getPair() {
    return std::make_pair(this->u, this->v);
  }

  MetisVertex::MetisVertex(int id, int vertexSize, int *weights)
    : vertexID(id), vertexSize(vertexSize), vertexWeights(weights)
  {}

  bool MetisVertex::addEdge(MetisEdge *edge) {
    if(edge == 0) {
      return false;
    }

    std::pair<int, int> uvPair = edge->getPair();

    if(hasEdge(uvPair)) {
      return false;
    }
    else {
      this->edges[edge->getPair()] = edge;
    }

    return true;
  }

  bool MetisVertex::hasEdge(std::pair<int, int> uvPair) {
    std::map<std::pair<int, int>, MetisEdge *>::iterator it;
    it = this->edges.find(uvPair);
    if(it != this->edges.end()) {
      // pair exists
      return true;
    }
    return false;
  }


  bool graphFormatStringValid(std::string &format) {
    const int len = format.length();

    if(len > 3) {
      return false;
    }

    const char zero = '0';
    const char one = '1';
    for(int c = 0; c < len; c++) {
      char chr = format[c];
      if(chr != zero or chr != one) {
        return false;
      }
    }

    // all characters are 0 or 1
    // test for length
    if(len == 0) {
      format = "000";
    }
    if(len == 1) {
      format = "00" + format;
    }
    if(len == 2) {
      format = "0" + format;
    }

    return true;
  }

  MetisGraph::MetisGraph(int numNodes, int numUniqueEdges, std::string formatStr, int vertexWeightsSize)
    : numNodes(numNodes),
    numUniqueEdges(numUniqueEdges),
    formatStr(formatStr),
    vertexWeightsSize(vertexWeightsSize)
  {
    this->nodeWeights = new int[numNodes];

    this->parseFormat();
  }


  void MetisGraph::setGraphFormat(std::string formatStr) {
    std::string correctedFormat = formatStr;
    if(graphFormatStringValid(correctedFormat)) {
      this->formatStr = correctedFormat;
    }
    else {
      this->formatStr = "111";
    }

    this->parseFormat();
  }

  void MetisGraph::parseFormat() {
    this->format = GraphFormat_DEFAULT;

    if(graphFormatStringValid(this->formatStr) == false) {
      return;
    }

    if(this->formatStr.length() == 3) {
      // FLAG abc
      // c = vertex weights provided
      // b = edge weights provided
      // a = vertex labels provided

      int vertWeights = Utils::charToNum(&this->formatStr[1]);
      int edgeWeights = Utils::charToNum(&this->formatStr[0]);
      int vertSize = Utils::charToNum(&this->formatStr[2]);

      if(vertWeights == 1) {
        this->format = (this->format | GraphFormat_VertexWeights);
      }
      if(edgeWeights == 1) {
        this->format = (this->format | GraphFormat_EdgeWeights);
      }
      if(vertSize == 1) {
        this->format = (this->format | GraphFormat_VertexSize);
      }
    }
    else {
      // print out unrecognized format
      std::cout << "Unrecognized METIS file format xxx: " << this->formatStr << std::endl;
    }
  }

  bool MetisGraph::isGraphFormatFlagSet(int graphFormatFlag) {
    // return true if format | flag == 1 (flag bit is set)
    return ((this->format | graphFormatFlag) == 1);
  }

  void MetisGraph::print() {
    std::cout << "Nodes=" << this->numNodes << " UniqueEdges=" << this->numUniqueEdges << " format=" << this->formatStr << std::endl;
  }



MetisGraph *loadGraphFromFile(std::string path) {
  std::ifstream infile(path);

  MetisGraph *graph= 0;

  bool isFirstLine = true;
  std::string line;
  int nodeID = 0;
  while(std::getline(infile, line)) {
    // clean each line
    cleanLine(line);

    // TODO output warning if line is empty?

    // skip comment lines
    if(lineIsComment(line)) {
      continue;
    }

    // first line is the comment line
    if(isFirstLine) {
      // parse the header of the graph
      graph = parseMETISHeader(line);

      if(graph == 0) {
        std::cout << "Error: could not generate METIS Graph from header string." << std::endl;
        return 0;
      }

      isFirstLine = false;
    }
    else {
      parseMETISNodeLine(line, nodeID, graph);
      nodeID++;
    }
  }

  return graph;
}

MetisGraph * parseMETISHeader(std::string &header) {
  // Extracts the right parameters from the METIS header
  std::vector<std::string> elems = Utils::split(header, ' ');
  const int numElems = elems.size();
  // n, m, fmt ncon

  if(numElems <= 4 && numElems >= 2) {
    std::cout << "METIS Graph Standard Header found." << std::endl;

    int numNodes = Utils::strToNum(elems[0]);
    int numEdges = Utils::strToNum(elems[1]);

    std::string format = "";
    int ncon = 0;

    if(numElems > 2) {
      format = elems[2];
    }

    if(numElems > 3) {
      ncon = Utils::strToNum(elems[3]);
    }

    MetisGraph *graph = new MetisGraph(numNodes, numEdges, format, ncon);
    return graph;
  }
  else {
    std::cout << "METIS Graph Standard Header NOT found, not enough parameters: " << std::endl << "\t" << header << std::endl;
    return 0;
  }
}

void parseMETISNodeLine(std::string line, int nodeID, MetisGraph *graph) {
  if(graph == 0) {
    return;
  }

  // split the line by spaces
  std::vector<std::string> parts = Utils::split(line, ' ');
  std::vector<int> values;

  const int nParts = parts.size();
  for(int p = 0; p < nParts; p++) {
    int value = Utils::strToNum(parts[p]);
    values.push_back(value);
  }

  int minSize = graph->isGraphFormatFlagSet(GraphFormat_VertexSize) ? 1 : 0;
  minSize += graph->isGraphFormatFlagSet(GraphFormat_VertexWeights) ? graph->vertexWeightsSize : 0;

  std::cout << "Min size= " << minSize << std::endl;

  int nodeSize = 0;
  int vertexWeights [graph->vertexWeightsSize];

  if(values.size() < minSize) {
    // parse error, cannot extract the right number of parameters from node
    std::cout << "Vertex [" << nodeID << "] Parsing: wrong number of parameters. Expecting a minimum of " << minSize << " but found " << values.size();

    return;
  }

  // extract values
  int idStart = 0;
  if(graph->isGraphFormatFlagSet(GraphFormat_VertexSize)) {
    // OK, can extract vertex size
    nodeSize = values[0];
    idStart = 1;
  }

  if(graph->isGraphFormatFlagSet(GraphFormat_VertexWeights)) {
    int w_i = 0;
    for(int i = idStart; i <= idStart + graph->vertexWeightsSize; i++) {
      vertexWeights[w_i] = values[i];
      w_i++;
    }
    idStart += graph->vertexWeightsSize;
  }

  // extract edge/weight pair
  for(int i = idStart; i < nParts; i++) {
    int node = values[i];
    int edgeW = 0;
    if(graph->isGraphFormatFlagSet(GraphFormat_EdgeWeights)) {
      // we must also extract edge weight
      if(i + 1 < nParts) {
        i++;
        edgeW = values[i];
      }
      else {
        std::cout << "Error: cannot extract edge weight for vertex " << nodeID << std::endl;
        break;
      }
    }
  }

}

bool lineIsComment(std::string &line) {
  if(line.length() == 0) {
    return false;
  }

  char c = line[0];
  const char percent = '%';
  if (c == percent) {
    return true;
  }

  return false;
}

void cleanLine(std::string &line) {
  line.erase(std::remove(line.begin(), line.end(), '\n'), line.end());
  line.erase(std::remove(line.begin(), line.end(), '\r'), line.end());
}


} // END namespace METIS
