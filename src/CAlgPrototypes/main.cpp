#include <iostream>

// Include Scotch.h
#include "includes/scotch.h"

namespace SCOTCH {
  void version() {
    int major, minor, patch;
    SCOTCH_version(&major, &minor, &patch);
    std::cout << "SCOTCH Version: " << major << "." << minor << "." << patch;
  }
}


int main(int argc, char*argv[]) {
  SCOTCH::version();
}
