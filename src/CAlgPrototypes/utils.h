#ifndef _UTILS_SCOTCH_
#define _UTILS_SCOTCH_

#include <string>
#include <vector>

namespace Utils {
  void split(const std::string &s, char delim, std::vector<std::string> &elems);
  std::vector<std::string> split(const std::string &s, char delim);
  int strToNum(std::string &s);
  int charToNum(const char *c);
}

#endif
