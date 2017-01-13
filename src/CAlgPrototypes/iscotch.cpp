#include "iscotch.h"

#include "metis.h"

namespace ISCOTCH {

void version() {
  int major, minor, patch;
  SCOTCH_version(&major, &minor, &patch);
  std::cout << "SCOTCH Version: " << major << "." << minor << "." << patch;
}

SCOTCH_Arch *createSCOTCHArch() {
  SCOTCH_Arch* arch = SCOTCH_archAlloc();
  int success = SCOTCH_archInit(arch);
  return arch;
}

void deleteSCOTCHArch(SCOTCH_Arch *arch) {
  if(arch) {
    SCOTCH_archExit(arch);
    delete arch;
  }
}

SCOTCH_Graph *createSCOTCHGraph() {
  SCOTCH_Graph *graph = SCOTCH_graphAlloc();
  int success = SCOTCH_graphInit(graph);
  return graph;
}

void deleteSCOTCHGraph(SCOTCH_Graph *graph) {
  if(graph) {
    SCOTCH_graphExit(graph);
    delete graph;
  }
}

SCOTCH_Strat *createSCOTCHStrategy() {
  SCOTCH_Strat *strat = SCOTCH_stratAlloc();
  if(SCOTCH_stratInit(strat) == 0) {
    std::string strategy = "f";
    SCOTCH_stratGraphMap(strat, strategy.c_str());
    return strat;
  }
  return 0;
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

  int success = SCOTCH_graphBuild(graph, baseval, vertnbr, metisData->verttab, 0, metisData->velotab, 0, edgenbr, metisData->edgetab, metisData->edlotab);

  if(success == 0) {
    return true;
  }

  return false;
}

bool checkGraph(SCOTCH_Graph *graph) {
  if(SCOTCH_graphCheck(graph) == 0) {
    return true;
  }
  return false;
}

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
