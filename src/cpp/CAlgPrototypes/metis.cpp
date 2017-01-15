#include "metis.h"

#include <iostream>
#include <fstream> // for reading file
#include <vector>
#include <algorithm>


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

    //std::cout << "Created Edge: " << this->u << " " << this->v << std::endl;
  }

  std::pair<int, int> MetisEdge::getPair() {
    return std::make_pair(this->u, this->v);
  }

  MetisVertex::MetisVertex(int id, int vertexSize, std::vector<int>weights)
    : vertexID(id), vertexSize(vertexSize), vertexWeights(weights)
  {}

  bool MetisVertex::addEdge(MetisEdge *edge) {
    if(edge == 0) {
      return false;
    }

    std::pair<int, int> uvPair = edge->getPair();

    if(this->hasEdge(uvPair)) {
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

  int MetisVertex::numEdges() {
    return this->edges.size();
  }


  bool graphFormatStringValid(std::string &format) {
    const int len = format.length();

    if(len == 0) {
      format = "000";
    }
    if(len == 1) {
      format = "00" + format;
    }
    if(len == 2) {
      format = "0" + format;
    }

    if(len > 3) {
      std::cout << "Format String Length != 3" << std::endl;
      return false;
    }

    const char zero = '0';
    const char one = '1';
    for(int c = 0; c < len; c++) {
      char chr = format[c];
      if(chr != zero && chr != one) {
        return false;
      }
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
      this->formatStr = "000";
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

      int edgeWeights = Utils::charToNum(this->formatStr[2]);
      int vertWeights = Utils::charToNum(this->formatStr[1]);
      int vertSize = Utils::charToNum(this->formatStr[0]);

      std::cout << vertWeights << ":" << edgeWeights << ":" << vertSize << std::endl;

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
    return ((this->format & graphFormatFlag) > 0);
  }

  void MetisGraph::print() {
    std::cout << "Nodes=" << this->numNodes << " UniqueEdges=" << this->numUniqueEdges << " format=" << this->formatStr << std::endl;

    if(this->isGraphFormatFlagSet(GraphFormat_EdgeWeights)) {
      std::cout << "Edge Weights = on" << std::endl;
    }
    if(this->isGraphFormatFlagSet(GraphFormat_VertexWeights)) {
      std::cout << "Vertex Weights = on" << std::endl;
    }
    if(this->isGraphFormatFlagSet(GraphFormat_VertexSize)) {
      std::cout << "Vertex Size = on" << std::endl;
    }
  }

  bool MetisGraph::addVertex(MetisVertex *vertex) {
    if(vertex) {
      std::map <std::pair<int, int>, MetisEdge *>::iterator edgeIt;
      for(edgeIt = vertex->edges.begin(); edgeIt != vertex->edges.end(); edgeIt++) {
        if(this->isEdgeUnique(edgeIt->second) == true) {
          // add edge
          this->uniqueEdges.push_back(edgeIt->first);
        }
      }
      std::map <int, MetisVertex *>::iterator vIt = this->vertices.find(vertex->vertexID);
      if(vIt == this->vertices.end()) {
        // add vertex
        this->vertices[vertex->vertexID] = vertex;
      }
      return true;
    }
    return false;
  }

  bool MetisGraph::isEdgeUnique(MetisEdge *edge) {
    if(edge) {
      for(int i = 0; i < this->uniqueEdges.size(); i++) {
        std::pair<int, int> e = this->uniqueEdges[i];
        if(e.first > e.second) {
          std::cout << "Edge first > second" << std::endl;
        }
        if(edge->u == e.first && edge->v == e.second) {
          return false;
        }
      }
      return true;
    }
    return false;
  }


  int MetisGraph::numVertices() {
    return this->vertices.size();
  }

  int MetisGraph::numEdges() {
    return this->uniqueEdges.size();
  }


  void MetisGraph::computeArrays() {

      // populate vertices & edges
      this->verttab = new int[this->numVertices() + 1];
      this->edgetab = new int[this->numEdges() * 2];

      this->edlotab = new int[this->numEdges() * 2];
      this->velotab = new int[this->numVertices()];

      int vtabID = 0;
      std::map<int, MetisVertex *>::iterator it;
      for(it = this->vertices.begin(); it != this->vertices.end(); it++) {
        this->verttab[it->first - 1] = vtabID;
        this->velotab[it->first - 1] = 1; // TODO vertex weights
        // populate edges
        int count = 0;
        std::map <std::pair<int, int>, MetisEdge *>::iterator eit;
        for(eit = it->second->edges.begin(); eit != it->second->edges.end(); eit++) {
          int otherID = eit->second->getOtherVertex(it->first);

          this->edgetab[vtabID + count] = otherID - 1;
          this->edlotab[vtabID + count] = eit->second->weight;

          count++;
        }
        // update vtabID
        vtabID += it->second->numEdges();
      }
      this->verttab[this->numVertices()] = vtabID;


  }


MetisGraph *loadGraphFromFile(std::string path) {
  std::ifstream infile(path.c_str());

  MetisGraph *graph= 0;

  bool isFirstLine = true;
  std::string line;
  int nodeID = 1;
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
      //break;
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
    int ncon = 1; // default is 1

    if(numElems > 2) {
      format = elems[2];
    }

    if(numElems > 3) {
      ncon = Utils::strToNum(elems[3]);
    }

    MetisGraph *graph = new MetisGraph(numNodes, numEdges, format, ncon);
    //graph->print();
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

  //std::cout << "Min size= " << minSize << std::endl;

  int nodeSize = 0;
  std::vector<int> vertexWeights;;

  if(values.size() < minSize) {
    // parse error, cannot extract the right number of parameters from node
    std::cout << "Vertex [" << nodeID << "] Parsing: wrong number of parameters. Expecting a minimum of " << minSize << " but found " << values.size();

    return;
  }


  int idStart = 0;
  if(graph->isGraphFormatFlagSet(GraphFormat_VertexSize)) {
    std::cout << "parseMETISNodeLine() - extracting vertexSize - not sure this should ever run." << std::endl;
    // OK, can extract vertex size
    nodeSize = values[0];
    idStart = 1;
  }

  if(graph->isGraphFormatFlagSet(GraphFormat_VertexWeights)) {
    //int w_i = 0;
    for(int i = idStart; i <= idStart + graph->vertexWeightsSize; i++) {
      vertexWeights.push_back(values[i]);
      //w_i++;
    }
    idStart += graph->vertexWeightsSize;
  }

  // create a vertex
  MetisVertex *vertex = new MetisVertex(nodeID, 1, vertexWeights);

  // extract edge/weight pair
  for(int i = idStart; i < nParts; i++) {
    int node = values[i];
    int edgeW = 0;
    if(graph->isGraphFormatFlagSet(GraphFormat_EdgeWeights)) {
      // we must also extract edge weight
      if(i + 1 < nParts) {
        i++;
        edgeW = values[i];

        // create edge
        MetisEdge *edge = new MetisEdge(nodeID, node, edgeW);

        // add edge to vertex
        if(vertex->addEdge(edge) == false) {
          delete edge;
        }
      }
      else {
        std::cout << "Error: cannot extract edge weight for vertex " << nodeID << std::endl;
        break;
      }
    }
  }

  // add vertex to graph
  graph->addVertex(vertex);
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
  //line.erase(std::find(line.begin(), line.end(), '\n'));
  //line.erase(std::find(line.begin(), line.end(), '\r'));
}


} // END namespace METIS
