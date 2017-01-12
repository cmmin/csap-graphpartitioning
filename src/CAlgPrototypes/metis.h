#ifndef _METIS_H
#define _METIS_H

#include <string>

namespace METIS {
  // represents the different types of METIS graph formats
  enum GraphFormats {
    GraphFormat_DEFAULT         = 0b0000,
    GraphFormat_VertexWeights   = 0b0001,
    GraphFormat_EdgeWeights     = 0b0010,
    GraphFormat_VertexLabels    = 0b0100
  };

  /// @brief Checks that the format string of METIS format is valid.
  /// checks that format string consists of 0,1s and adds 0 if length < 3.
  /// @returns false if string is not 0,1s and > 3. Sets format to 000 if string is empty.
  bool graphFormatStringValid(std::string &format);

  struct MetisGraph {
    int numNodes;
    int numUniqueEdges;
    std::string formatStr;

    int format;
    int *nodeWeights;

    MetisGraph(int numNodes, int numUniqueEdges, std::string formatStr = "000");

    void setGraphFormat(std::string formatStr);
    void parseFormat();
    bool isGraphFormatFlagSet(int graphFormatFlag);
    void print();

  };

  MetisGraph  *loadGraphFromFile(std::string path);
  MetisGraph  *parseMETISHeader(std::string &header);
  void parseMETISNodeLine(std::string line, int nodeID, MetisGraph *graph);

} // end namespace METIS


#endif
