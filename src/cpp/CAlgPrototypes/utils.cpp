#include "utils.h"

#include <sstream>
#include <cstdlib>

namespace Utils {
void split(const std::string &s, char delim, std::vector<std::string> &elems) {
    std::stringstream ss;
    ss.str(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        elems.push_back(item);
    }
}

std::vector<std::string> split(const std::string &s, char delim) {
    std::vector<std::string> elems;
    split(s, delim, elems);
    return elems;
}

int strToNum(std::string &s) {
  return atoi(s.c_str());
}

int charToNum(const char c) {
  std::string str(&c);
  return strToNum(str);
}

} // END namespace Utils
