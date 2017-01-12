#include "metis.h"

#include <iostream>
#include <fstream> // for reading file


#include "utils.h"

namespace METIS {

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

  MetisGraph::MetisGraph(int numNodes, int numUniqueEdges, std::string formatStr)
    : numNodes(numNodes),
    numUniqueEdges(numUniqueEdges),
    formatStr(formatStr)
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

      int vertWeights = Utils::charToNum(&this->formatStr[2]);
      int edgeWeights = Utils::charToNum(&this->formatStr[1]);
      int vertLabels = Utils::charToNum(&this->formatStr[0]);

      if(vertWeights == 1) {
        this->format = (this->format | GraphFormat_VertexWeights);
      }
      if(edgeWeights == 1) {
        this->format = (this->format | GraphFormat_EdgeWeights);
      }
      if(vertLabels == 1) {
        this->format = (this->format | GraphFormat_VertexLabels);
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
  while(std::getline(infile, line)) {
    //std::isstringstream iss(line);
    if(isFirstLine) {
      graph = parseMETISHeader(line);

      if(graph == 0) {
        std::cout << "Error: could not generate METIS Graph from header string." << std::endl;
        return 0;
      }
      isFirstLine = false;
    }
    else {
      std::cout << line << std::endl;
      break;
    }
  }

  return graph;
}

MetisGraph * parseMETISHeader(std::string &header) {
  std::vector<std::string> elems = Utils::split(header, ' ');

  if(elems.size() == 3) {
    std::cout << "METIS Graph Standard Header found." << std::endl;


    int numNodes = Utils::strToNum(elems[0]);
    int numEdges = Utils::strToNum(elems[1]);
    std::string format = elems[2];

    MetisGraph *graph = new MetisGraph(numNodes, numEdges, format);
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

  std::vector<std::string> parts = Utils::split(line, ' ');



}


} // END namespace METIS
