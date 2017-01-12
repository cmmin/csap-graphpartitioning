#ifndef _METIS_H
#define _METIS_H

#include <string>
#include <map>
#include <vector>

/*

METIS FILE format

n = number of nodes
lineN = n + 1 = number of lines in file (excluding comment lines)

'%' as first character = comment line



*/



namespace METIS {
  // represents the different types of METIS graph formats
  enum GraphFormats {
    GraphFormat_DEFAULT         = 0b0000,
    GraphFormat_EdgeWeights     = 0b0001,
    GraphFormat_VertexWeights   = 0b0010,
    GraphFormat_VertexSize      = 0b0100
  };

  /// @brief Checks that the format string of METIS format is valid.
  /// checks that format string consists of 0,1s and adds 0 if length < 3.
  /// @returns false if string is not 0,1s and > 3. Sets format to 000 if string is empty.
  bool graphFormatStringValid(std::string &format);

  struct MetisEdge {
    int u;
    int v;
    int weight;

    MetisEdge(int u, int v, int weight = -1);
    std::pair<int, int> getPair();
  };

  struct MetisVertex {
    int vertexID;
    int vertexSize;
    int * vertexWeights;
    std::map <std::pair<int, int>, MetisEdge *> edges;

    MetisVertex(int id, int vertexSize = -1, int *weights = 0);
    bool addEdge(MetisEdge *edge);
    bool hasEdge(std::pair<int, int> uvPair);

  };

  struct MetisGraph {
    int numNodes;
    int numUniqueEdges;
    std::string formatStr;

    int format;
    int vertexWeightsSize;
    int *nodeWeights;

    MetisGraph(int numNodes, int numUniqueEdges, std::string formatStr = "111", int vertexWeightsSize = 0);

    void setGraphFormat(std::string formatStr);
    void parseFormat();
    bool isGraphFormatFlagSet(int graphFormatFlag);
    void print();

  };

  MetisGraph  *loadGraphFromFile(std::string path);
  MetisGraph  *parseMETISHeader(std::string &header);
  void parseMETISNodeLine(std::string line, int nodeID, MetisGraph *graph);
  bool lineIsComment(std::string &line);
  void cleanLine(std::string &line);

} // end namespace METIS


#endif
