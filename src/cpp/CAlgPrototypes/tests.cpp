#include <iostream>

#include "utils.h"
#include "metis.h"


bool testMetis() {
  using namespace METIS;

  MetisGraph *g = new MetisGraph(10, 10, "101");
  if(g) {
    if((g->format | GraphFormat_VertexWeights) == 0) {
      std::cout << "ERROR: expecting VertexWeights Flag = 1; found 0";
      return false;
    }
    if((g->format | GraphFormat_EdgeWeights) == 1) {
      std::cout << "ERROR: expecting EdgeWeights Flag = 0; found 1";
      return false;
    }
    if((g->format | GraphFormat_VertexLabels) == 0) {
      std::cout << "ERROR: expecting VertexLabels Flag = 1; found 0";
      return false;
    }
  }

  return true;
}



int main(int argc, char * argv []) {
  bool metisTestsPassed = testMetis();

  if(metisTestsPassed) {
    std::cout << "Ran METIS tests. All passed." << std::endl;
  }
  else {
    std::cout << "METIS tests failed." << std::endl;
  }
}
