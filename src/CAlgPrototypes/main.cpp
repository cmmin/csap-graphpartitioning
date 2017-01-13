#include <iostream>
#include <string>
#include <vector>

// Include Scotch.h
#include "includes/scotch.h"

#include "utils.h"
#include "metis.h"
#include "iscotch.h"

/* ********** */
/* prototypes */
/* ********** */


/**** MAIN ***/
int main(int argc, char*argv[]) {
  METIS::MetisGraph *graph = METIS::loadGraphFromFile("../../data/oneshot_fennel_weights.txt");
  if(graph) {
    graph->print();
    std::cout << graph->numEdges() << "edges; " << graph->numVertices() << "vertices;" << std::endl;

    graph->computeArrays();

    SCOTCH_Graph *scotchGraph = ISCOTCH::createSCOTCHGraph();
    if(ISCOTCH::graphBuild(scotchGraph, graph)) {
      std::cout << "Created scotch graph from metis." << std::endl;
    }
    else {
      std::cout << "Problem instantiating SCOTCH graph from metis." << std::endl;
    }

    std::cout << "SCOTCH Graph Check = " << ISCOTCH::checkGraph(scotchGraph) << std::endl;

    // map

    SCOTCH_Arch *arch = ISCOTCH::createSCOTCHArch();
    //std::string strategy = "f";
    SCOTCH_Strat *strategy = ISCOTCH::createSCOTCHStrategy();
    int * parttab = new int[graph->numVertices()];

    if(ISCOTCH::graphMap(scotchGraph, arch, strategy, parttab)) {
      std::cout << "Successfully ran graphMap." << std::endl;
    }
    else {
      std::cout << "Failed to run graphMap." << std::endl;
    }

  }

}
