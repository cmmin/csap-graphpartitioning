#include "iscotch.h"

#include "metis.h"

namespace ISCOTCH {

void version() {
  int major, minor, patch;
  SCOTCH_version(&major, &minor, &patch);
  std::cout << "SCOTCH Version: " << major << "." << minor << "." << patch;
}


/* ********************* */
/* Architecture ROUTINES */
/* ********************* */


SCOTCH_Arch *createSCOTCHArch() {
  SCOTCH_Arch* arch = SCOTCH_archAlloc();
  if(SCOTCH_archInit(arch) == 0) {
    // successfully initialized architecture
    return arch;
  }
  return 0;
}

void deleteSCOTCHArch(SCOTCH_Arch *arch) {
  if(arch) {
    SCOTCH_archExit(arch);
    delete arch;
  }
}

bool buildSCOTCHArch(SCOTCH_Arch *arch, SCOTCH_Graph *graph, SCOTCH_Strat *strat) {
  // build the architecture: pg 78
  if(arch == 0 || graph == 0 || strat == 0) {
    return false;
  }

  /* Pg. 78
  archptr   pointer to architecture
  graphptr  pointer to graph
  listnbr   number of vertices through which decomposition is restricted
  listtab   the list of vertices onto which the architecture is restricted
  straptr   pointer to the strategy (must have been built before?)

  */
  int listnbr = 0;
  int *listtab = 0;

  return SCOTCH_archBuild(arch, graph, listnbr, listtab, strat) == 0 ? true : false;
}

/* ************** */
/* Graph ROUTINES */
/* ************** */

SCOTCH_Graph *createSCOTCHGraph() {
  SCOTCH_Graph *graph = SCOTCH_graphAlloc();
  if(SCOTCH_graphInit(graph) == 0) {
    return graph;
  }

  return 0;
}

bool deleteSCOTCHGraph(SCOTCH_Graph *graph) {
  if(graph) {
    SCOTCH_graphExit(graph);
    delete graph;
    return true;
  }
  return false;
}

bool checkGraph(SCOTCH_Graph *graph) {
  return (SCOTCH_graphCheck(graph) == 0) ? true : false;
}


bool graphBuild(SCOTCH_Graph * graph, METIS::MetisGraph *metisData)
{
  if(graph == 0 || metisData == 0) {
    return false;
  }

  int baseval = 0;
  int vertnbr = metisData->numVertices();

  //int *verttab; // andjacency index array = vertnbr + 1; adjacency_start
  //int *vendtab; // set to null
  //int *velotab; // vertex load array = vertnbr = node weights
  //int *vlbltab; // vertex label array

  int edgenbr = metisData->numEdges() * 2;
  //int *edgetab; // adjacency array = adjacency_list
  //int *edlotab; // arc load array = edge weights

  return SCOTCH_graphBuild(graph, baseval, vertnbr, metisData->verttab, 0, metisData->velotab, 0, edgenbr, metisData->edgetab, metisData->edlotab) == 0 ? true : false;
}


/* ***************** */
/* Strategy ROUTINES */
/* ***************** */

SCOTCH_Strat *createSCOTCHStrategy(StrategyTypes strategy) {
  SCOTCH_Strat *strat = SCOTCH_stratAlloc();

  if(SCOTCH_stratInit(strat) == 0) {

    int success = -1;

    switch(strategy) {
      case StrategyType_GraphMapBuild: {
        // Manual: 8.15.4
        // Strategy string:

        std::string strategyStr = "f";
        success = SCOTCH_stratGraphMap(strat, strategyStr.c_str());
        break;
      }
      case StrategyType_Default:
      default: {
        // return the default strategy
        return strat;
      }

    }

    if(success == 0) {
      // strategy created successfully
      return strat;
    }
    return 0;
  }
  return 0;
}

/* ****************** */
/* Partition ROUTINES */
/* ****************** */

bool graphMap(SCOTCH_Graph *graph, SCOTCH_Arch *arch, SCOTCH_Strat *strat, int *parttab) {
  if(graph == 0) {
    std::cout << "Graph Pointer error" << std::endl;
  }
  if(arch == 0) {
    std::cout << "Arch Pointer error" << std::endl;
  }
  if(strat == 0) {
    std::cout << "Strat Pointer error" << std::endl;
  }
  if(parttab == 0) {
    std::cout << "parttab Pointer error" << std::endl;
  }

  if(graph == 0 || arch == 0 || strat == 0 || parttab == 0) {
    std::cout << "Pointer error" << std::endl;
    return false;
  }
  int success = SCOTCH_graphMap(graph, arch, strat, parttab);
  if(success == 0) {
    return true;
  }
  return false;

}


} // END namespace ISCOTCH
