#ifndef _I_SCOTCH_
#define _I_SCOTCH_

#include <iostream>
#include "includes/scotch.h"

namespace METIS {
  struct MetisGraph;
}

namespace ISCOTCH {
  void version();

  SCOTCH_Arch *createSCOTCHArch();
  void deleteSCOTCHArch(SCOTCH_Arch *arch);

  SCOTCH_Graph *createSCOTCHGraph();
  void deleteSCOTCHGraph(SCOTCH_Graph* graph);

  SCOTCH_Strat *createSCOTCHStrategy();

  bool graphBuild(SCOTCH_Graph * graph, METIS::MetisGraph *metisData);
  bool checkGraph(SCOTCH_Graph *graph);

  bool graphMap(SCOTCH_Graph *graph, SCOTCH_Arch *arch, SCOTCH_Strat *strat, int * parttab);

}

#endif
