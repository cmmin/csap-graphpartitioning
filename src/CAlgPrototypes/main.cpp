#include <iostream>
#include <string>
#include <vector>

// Include Scotch.h
#include "includes/scotch.h"

#include "utils.h"
#include "metis.h"

/* ********** */
/* prototypes */
/* ********** */


namespace SCOTCH {
  void version();
} // END namespace SCOTCH




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
  METIS::MetisGraph *graph = METIS::loadGraphFromFile("../../data/oneshot_fennel_weights.txt");
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
