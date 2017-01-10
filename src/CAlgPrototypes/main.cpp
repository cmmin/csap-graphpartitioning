#include <iostream>
#include <string>
#include <fstream> // for reading file
#include <sstream> // for reading from file
#include <vector>

// Include Scotch.h
#include "includes/scotch.h"


/* ********** */
/* prototypes */
/* ********** */

namespace METIS {
  enum GraphFormat {
    GraphFormat_DEFAULT = 0b0000,
    GraphFormat_EdgeWeights = 0b0001,
    GraphFormat_NodeWeights = 0b0010
  };


  struct MetisGraph {
    int numNodes;
    int numUniqueEdges;
    std::string formatStr;

    int format;

    int *nodeWeights;

    MetisGraph(int numNodes, int numUniqueEdges, std::string formatStr = "")
      : numNodes(numNodes),
      numUniqueEdges(numUniqueEdges),
      formatStr(formatStr)
    {
      this->nodeWeights = new int[numNodes];

      this->parseFormat();
    }

    void parseFormat() {
      const int len = this->formatStr.length();
      if(len == 0) {
        this->format = GraphFormat::GraphFormat_DEFAULT;
      }
      else if(len == 3) {

      }
    }

    void print() {
      std::cout << "Nodes=" << this->numNodes << " UniqueEdges=" << this->numUniqueEdges << " format=" << this->formatStr << std::endl;
    }

  };
} // end namespace METIS

namespace SCOTCH {
  void version();
} // END namespace SCOTCH

namespace Utils {
  void split(const std::string &s, char delim, std::vector<std::string> &elems);
  std::vector<std::string> split(const std::string &s, char delim);
  int strToNum(std::string &s);
}

METIS::MetisGraph  *loadGraphFromFile(std::string path);
METIS::MetisGraph  *parseMETISHeader(std::string &header);
void parseMETISNodeLine(std::string line, int nodeID, METIS::MetisGraph *graph);

/*
void loadGraph(std::string path) {
  SCOTCH_Graph * graph = SCOTCH_graphAlloc();
  SCOTCH_graphInit(graph);

  int baseVal = 0;
  int vertnbr = 1000; // number of vertices


}
*/

/**** MAIN ***/

int main(int argc, char*argv[]) {
  METIS::MetisGraph *graph = loadGraphFromFile("../../data/oneshot_fennel_weights.txt");
  if(graph) {
    graph->print();
  }

  int arr [100] = {};
  std::cout << (sizeof(arr)/sizeof(*arr)) << std::endl;

}


namespace SCOTCH {
  void version() {
    int major, minor, patch;
    SCOTCH_version(&major, &minor, &patch);
    std::cout << "SCOTCH Version: " << major << "." << minor << "." << patch;
  }
} // END namepsace SCOTCH

namespace Utils {
void split(const std::string &s, char delim, std::vector<std::string> &elems) {
    std::stringstream ss;
    ss.str(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        elems.push_back(item);
    }
}


std::vector<std::string> split(const std::string &s, char delim) {
    std::vector<std::string> elems;
    split(s, delim, elems);
    return elems;
}

int strToNum(std::string &s) {
  return atoi(s.c_str());
}

} // END namespace Utils



METIS::MetisGraph *loadGraphFromFile(std::string path) {
  std::ifstream infile(path);

  METIS::MetisGraph *graph= 0;

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

METIS::MetisGraph  *parseMETISHeader(std::string &header) {
  std::vector<std::string> elems = Utils::split(header, ' ');

  if(elems.size() == 3) {
    std::cout << "METIS Graph Standard Header found." << std::endl;


    int numNodes = Utils::strToNum(elems[0]);
    int numEdges = Utils::strToNum(elems[1]);
    std::string format = elems[2];

    METIS::MetisGraph *graph = new METIS::MetisGraph(numNodes, numEdges, format);
    return graph;
  }
  else {
    std::cout << "METIS Graph Standard Header NOT found, not enough parameters: " << std::endl << "\t" << header << std::endl;
    return 0;
  }
}

void parseMETISNodeLine(std::string line, int nodeID, METIS::MetisGraph *graph) {
  if(graph == 0) {
    return;
  }

  std::vector<std::string> parts = split(line, ' ')



}
