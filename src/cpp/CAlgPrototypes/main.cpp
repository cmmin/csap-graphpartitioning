#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <stdexcept> // for exceptions
#include <fstream> // for writing to file
#include <cstdlib> // for itoa
//#include <stdlib.h>
#include <cstring>

// Include Scotch.h
#include "includes/scotch.h"

#include "utils.h"
#include "metis.h"
#include "iscotch.h"


/// @brief Runs graphMap on the metis input file
void graphMap();

/// @brief Runs graphMapFixed on the metis input file
void graphMapFixed();

/// @brief Writes the partition for each vertex
void writePartitions(int *parttab, int numVertices, std::string path);

void compareFixedNotFixed();

/**** MAIN ***/
int main(int argc, char*argv[]) {
  try {
    graphMapFixed();
  }
  catch (const std::exception &e) {
    std::cout << "EXCEPTION running graphMap(): " << e.what() << std::endl;
  }
}

void graphMap() {

  // parameters initialisation
  const int partitionNbr = 10; // number of partitions/k clusters
  int straval = 0; // default strategy value: see pg. 60 SCOTCH for other flag values
  double kbalval = 0.001; // default imbalance tolerance value

  std::string strflags = ""; // stores the flags for the strategy (see SCOTCH 8.3.2 section manual)
  const char * straptr = 0; // c-string pointer for strflags
  if(strflags.length() != 0) {
    straptr = strflags.c_str();
  }

  // Load the METIS graph
  METIS::MetisGraph *metisGraph = METIS::loadGraphFromFile("../../../data/oneshot_fennel_weights.txt");

  // error if not loaded properly
  if(metisGraph == 0) {
    throw std::runtime_error("Could not load Metis graph.");
  }

  // compute arrays for SCOTCH graph
  metisGraph->computeArrays();
  // output basic metis graph stats
  metisGraph->print();

  // create the SCOTCH Graph from the Metis data
  SCOTCH_Graph *scotchGraph = ISCOTCH::createSCOTCHGraph();
  if(ISCOTCH::graphBuild(scotchGraph, metisGraph) == false) {
    throw std::runtime_error("Problem instantiating SCOTCH graph from metis Graph.");
  }
  std::cout << "Created scotch graph from metis." << std::endl;

  // create the architecture object
  SCOTCH_Arch *arch = ISCOTCH::createSCOTCHArch();
  if(arch == 0) {
    throw std::runtime_error("Could not create Architecture object");
  }

  // populate the architecture object for graph partitioning
  if(SCOTCH_archCmplt(arch, (SCOTCH_Num)partitionNbr) != 0) {
    throw std::runtime_error("Could not create a complete graph partitioning architecture");
  }
  std::cout << "Created complete graph partitioning architecture" << std::endl;


  // create the strategy
  SCOTCH_Strat *strategy = ISCOTCH::createSCOTCHStrategy(ISCOTCH::StrategyType_Default);
  if(strategy == 0) {
    throw std::runtime_error("Could not create default strategy object.");
  }

  // populate strategy parameters for graphMap
  // (strategy ptr, scotch_num falgval, s_n partnbr, dbl balrat)
  if(SCOTCH_stratGraphMapBuild(strategy, (SCOTCH_Num)straval, (SCOTCH_Num)partitionNbr, kbalval) != 0) {
    throw std::runtime_error("Could not create strategy for Graph Map Build");
  }


  if(straptr != 0) {
    // use the strategy flags, on the strategy
    SCOTCH_stratGraphMap(strategy, straptr);
  }

  // create the vector of partition values, must be = number of vertices
  int * parttab = new int[metisGraph->numVertices()];

  // run the mapping of the vertices to the partitions
  if(ISCOTCH::graphMap(scotchGraph, arch, strategy, parttab) == false) {
    throw std::runtime_error("Failed to run Graph Map on the data.");
  }
  std::cout << "Successfully ran graphMap." << std::endl;

  // write the partitions to file
  writePartitions(parttab, metisGraph->numVertices(), "../../../data/oneshot_fennel_partitions.txt");

}

void graphMapFixed() {

  // parameters initialisation
  const int partitionNbr = 10; // number of partitions/k clusters
  int straval = 0; // default strategy value: see pg. 60 SCOTCH for other flag values
  double kbalval = 0.001; // default imbalance tolerance value

  std::string strflags = ""; // stores the flags for the strategy (see SCOTCH 8.3.2 section manual)
  const char * straptr = 0; // c-string pointer for strflags
  if(strflags.length() != 0) {
    straptr = strflags.c_str();
  }

  // Load the METIS graph
  METIS::MetisGraph *metisGraph = METIS::loadGraphFromFile("../../../data/oneshot_fennel_weights.txt");

  // error if not loaded properly
  if(metisGraph == 0) {
    throw std::runtime_error("Could not load Metis graph.");
  }

  // compute arrays for SCOTCH graph
  metisGraph->computeArrays();
  // output basic metis graph stats
  metisGraph->print();

  // create the SCOTCH Graph from the Metis data
  SCOTCH_Graph *scotchGraph = ISCOTCH::createSCOTCHGraph();
  if(ISCOTCH::graphBuild(scotchGraph, metisGraph) == false) {
    throw std::runtime_error("Problem instantiating SCOTCH graph from metis Graph.");
  }
  std::cout << "Created scotch graph from metis." << std::endl;

  // create the architecture object
  SCOTCH_Arch *arch = ISCOTCH::createSCOTCHArch();
  if(arch == 0) {
    throw std::runtime_error("Could not create Architecture object");
  }

  // populate the architecture object for graph partitioning
  if(SCOTCH_archCmplt(arch, (SCOTCH_Num)partitionNbr) != 0) {
    throw std::runtime_error("Could not create a complete graph partitioning architecture");
  }
  std::cout << "Created complete graph partitioning architecture" << std::endl;


  // create the strategy
  SCOTCH_Strat *strategy = ISCOTCH::createSCOTCHStrategy(ISCOTCH::StrategyType_Default);
  if(strategy == 0) {
    throw std::runtime_error("Could not create default strategy object.");
  }

  // populate strategy parameters for graphMap
  // (strategy ptr, scotch_num falgval, s_n partnbr, dbl balrat)
  if(SCOTCH_stratGraphMapBuild(strategy, (SCOTCH_Num)straval, (SCOTCH_Num)partitionNbr, kbalval) != 0) {
    throw std::runtime_error("Could not create strategy for Graph Map Build");
  }


  if(straptr != 0) {
    // use the strategy flags, on the strategy
    SCOTCH_stratGraphMap(strategy, straptr);
  }

  // create the vector of partition values, must be = number of vertices
  int * parttab = new int[metisGraph->numVertices()];

  // Pick n number of vertices that should be fixed
  int nFixedVertices = 10;

  for(int i = 0; i < metisGraph->numVertices(); i++) {
    int partitionID = -1;

    if(i < nFixedVertices) {
      partitionID = (i % partitionNbr);
    }
    *(parttab + i) = partitionID;
  }

  // run the mapping of the vertices to the partitions

  if(SCOTCH_graphMapFixed(scotchGraph, arch, strategy, parttab) != 0) {
    throw std::runtime_error("Failed to run Graph Map on the data.");
  }
  std::cout << "Successfully ran graphMapFixed." << std::endl;

  // write the partitions to file
  writePartitions(parttab, metisGraph->numVertices(), "../../../data/oneshot_fennel_partitions_fixed.txt");

}


void writePartitions(int *parttab, int numVertices, std::string path) {
  if(parttab == 0) {
    return;
  }

  std::ofstream file;
  // truncate file on open
  file.open(path.c_str(), std::ofstream::out | std::ofstream::trunc);
  if(file.is_open()) {
    // ok to write
    for(int i = 0; i < numVertices; i++) {
      if(i > 0) {
        file << "\n";
      }

      std::ostringstream ss;
      ss << *(parttab + i);
      file << ss.str();

      //file << std::string::to_string(*(parttab + i));
    }
  }
  file.close();
}





/* notes */
/*

1. initialize the strategy object
2. initialize the graph
3. populate/load the graph

4. load the architecture:

SCOTCH_archInit (&archdat);
if ((flagval & C_FLAGPART) != 0) {
  if ((flagval & C_FLAGCLUSTER) != 0)
    SCOTCH_archVcmplt (&archdat);
  else
    SCOTCH_archCmplt (&archdat, C_partNbr);
}
else {


5. create strategy parameters

if ((straval != 0) || ((flagval & C_FLAGKBALVAL) != 0)) {
  if (straptr != NULL)
    errorPrint ("main: options '-b' / '-c' and '-m' are exclusive");

  if ((flagval & C_FLAGPARTOVL) != 0)           // If overlap partitioning wanted
    SCOTCH_stratGraphPartOvlBuild (&stradat, straval, (SCOTCH_Num) C_partNbr, kbalval);
  else if ((flagval & C_FLAGCLUSTER) != 0)      // If clustering wanted
    SCOTCH_stratGraphClusterBuild (&stradat, straval, (SCOTCH_Num) C_partNbr, 1.0, kbalval);
  else
    SCOTCH_stratGraphMapBuild (&stradat, straval, (SCOTCH_Num) C_partNbr, kbalval);
}

6. call SCOTCH_graphSize



*/

/*#ifdef USE_OLD_CODE
  if(metisGraph) {

    // STEP 1: build the graph

    std::cout << "SCOTCH Graph Check = graph " << (ISCOTCH::checkGraph(scotchGraph) ? "valid" : "invalid") << std::endl;

    // STEP 2: build the strategy
    // TODO strategy graphmapbuild() C_partNbr
    // TODO usage:       SCOTCH_stratGraphMapBuild (&stradat, straval, (SCOTCH_Num) C_partNbr, kbalval);
    /// TODO if straptr != NULL , calls SCOTCH_stratGrarphMap
    SCOTCH_Strat *strategy = ISCOTCH::createSCOTCHStrategy(ISCOTCH::StrategyType_Default);

    // STEP 3: build the architecture
    SCOTCH_Arch *arch = ISCOTCH::createSCOTCHArch();

    // TODO what about SCOTCH_archCmplt() ? with cPartNbr

    if(ISCOTCH::buildSCOTCHArch(arch, scotchGraph, strategy) == false) {
      std::cout << "Error building SCOTCH Architecture." << std::endl;
    }

    // TODO   SCOTCH_graphSize (&grafdat, &vertnbr, NULL);
    // TODO     SCOTCH_graphMapInit (&grafdat, &mappdat, &archdat, parttab);
    // TODO         SCOTCH_graphMapCompute (&grafdat, &mappdat, &stradat);



    // STEP 4: partition the graph
    int * parttab = new int[metisGraph->numVertices()];
    if(ISCOTCH::graphMap(scotchGraph, arch, strategy, parttab)) {
      std::cout << "Successfully ran graphMap." << std::endl;
    }
    else {
      std::cout << "Failed to run graphMap." << std::endl;
    }
  }
#endif
*/
