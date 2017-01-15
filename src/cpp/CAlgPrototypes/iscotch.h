#ifndef _I_SCOTCH_
#define _I_SCOTCH_

#include <iostream>
#include "includes/scotch.h"

// forward declaration
namespace METIS {
  struct MetisGraph;
}

namespace ISCOTCH {

  /// Represents the available strategies from SCOTCH
  enum StrategyTypes {
    StrategyType_Default,
    StrategyType_GraphMapBuild
  };

  /// @brief SCOTCH_version()
  void version();

  /* ********************* */
  /* Architecture ROUTINES */
  /* ********************* */


  /// @brief Allocates memory for a SCOTCH_Arch object and initializes it.
  /// @return The pointer to the object if SCOTCH calls were successful, otherwise returns 0
  SCOTCH_Arch *createSCOTCHArch();
  /// @brief Deallocates memory and deletes SCOTCH_Arch object
  void deleteSCOTCHArch(SCOTCH_Arch *arch);

  /// @brief Builds a scotch architecture given a graph and strategy
  /// @return True if architeture is built successfully
  bool buildSCOTCHArch(SCOTCH_Arch *arch, SCOTCH_Graph *graph, SCOTCH_Strat *strat);


  /* ************** */
  /* Graph ROUTINES */
  /* ************** */
  /// @brief Creates an empty default SCOTCH_Graph
  /// @return Valid object pointer or 0 if insuccessful instantiation.
  SCOTCH_Graph *createSCOTCHGraph();

  /// @brief Deallocates memory and deletes object pointed at by graph.
  bool deleteSCOTCHGraph(SCOTCH_Graph* graph);

  bool checkGraph(SCOTCH_Graph *graph);

  bool graphBuild(SCOTCH_Graph * graph, METIS::MetisGraph *metisData);


  /* ***************** */
  /* Strategy ROUTINES */
  /* ***************** */

  SCOTCH_Strat *createSCOTCHStrategy(StrategyTypes strategy);

  /* ****************** */
  /* Partition ROUTINES */
  /* ****************** */

  bool graphMap(SCOTCH_Graph *graph, SCOTCH_Arch *arch, SCOTCH_Strat *strat, int * parttab);

}

#endif
