#ifndef _METIS_H
#define _METIS_H

#include <string>
#include <map>
#include <vector>

/*

# Description

Contains structures and code to load a METIS graph from a txt file, representing it and manipulating it into a SCOTCH graph data.

# Contents

enum GraphFormats;

struct MetisEdge;
struct MetisVertex;
struct MetisGraph;

metods to load a metis graph.


# METIS FILE format

'%' as first character = comment line
n = number of nodes/vertices
n + 1 = number of lines in file (excluding comment lines)
baseval = 1 if node/vertex indeces start at 1 or 0 otherwise

Line Structure
[0]: header line = n, m, [fmt, ncon]  [optional]
  n = see above
  m = number of unique edges (arcs)
  fmt = format of each node (flags, xxx) i.e. 001
  ncon = number of vertex weights

[1:1 + n]: node/vertex line = s w_1 w_2 ... w_ncon v1 e1 v2 e2 ... vk ek
  s = size of vertex
  w_1...w_ncon = weights of vertex
  vi = edge vertex id
  ei = edge weight

*/



namespace METIS {

  /// @brief Represents the different types of METIS graph format flags
  enum GraphFormats {
    GraphFormat_DEFAULT         = 0b0000,
    GraphFormat_EdgeWeights     = 0b0001,
    GraphFormat_VertexWeights   = 0b0010,
    GraphFormat_VertexSize      = 0b0100
  };

  /// @brief Checks that the format string of METIS format is valid.
  /// checks that format string consists of 0,1s and adds 0 if length < 3.
  /// @returns false if string is not 0,1s and > 3. Sets format to 000 if string is empty.
  bool graphFormatStringValid(std::string &format);



  /// @brief Represents an ARC in the Metis format
  /// An edge (u,v) is between node u and node v. Node u has smaller ID than node v in this implementation.
  ///
  /// \code{.cpp}
  ///
  /// MetisEdge e1(100, 120, 2); // u = 100, v = 120; weight = 2
  /// MetisEdge e2(120, 100, 2); // u = 100, v = 120; weight = 2; u,v swapped
  ///
  /// e2.getOtherVertex(100); // returns 120
  /// e2.getOtherVertex(101); // returns -1
  ///
  /// \endcode
  struct MetisEdge {
    int u;
    int v;
    int weight;

    /// @brief Constructs an Edge/Arc u,v where u is set to be less than v.
    MetisEdge(int u, int v, int weight = 1);

    /// @brief Returns the std::pair (u, v)
    std::pair<int, int> getPair();

    /// @brief Returns the u or v, given one of u or v.
    int getOtherVertex(int vertID) {
      if(vertID == this->u) {
        return this->v;
      }
      else if(vertID == this->v) {
        return this->u;
      }
      else {
        return -1;
      }
    }

  };


  /// @brief Represents a graph Vertex
  struct MetisVertex {
    int vertexID;
    int vertexSize;

    /// The different weights associated to this vertex. Set to 1 if by default.
    std::vector<int> vertexWeights;

    /// Stores the indexed edges that this vertex is connected to
    std::map <std::pair<int, int>, MetisEdge *> edges;

    /// @brief Constructs a Vertex
    MetisVertex(int id, int vertexSize = 1, std::vector<int> weights = std::vector<int>());

    /// @brief Adds a valid MetisEdge to this Vertex, if not added already
    bool addEdge(MetisEdge *edge);

    /// @brief Checks whether an edge is already associated with this vertex
    bool hasEdge(std::pair<int, int> uvPair);

    /// @brief Returns the current number of edges
    int numEdges();

  };


  /// @brief Represents a METIS Graph
  struct MetisGraph {
    /// The number of nodes/vertices in the graph
    int numNodes;

    int numUniqueEdges;

    /// The format string xxx as specified by the METIS format description (paramter fmt on pg.9 of user manual)
    std::string formatStr;

    /// Internal format flag: stores which GraphFormats flags are enabled for this graph
    int format;
    int vertexWeightsSize; // number of vertex parameters


    /// Array pointer that stores the weights for each vertex in the graph (computed by computeArrays())
    int *nodeWeights;
    /// Array pointer (SCOTCH FORMAT) that stores the vertices in the graph (computed by computeArrays())
    int *verttab;
    /// Array pointer (SCOTCH FORMAT) that stores the edges in the graph (computed by computeArrays())
    int *edgetab;
    /// Array pointer (SCOTCH FORMAT) that stores the edge weights in the graph (computed by computeArrays())
    int *edlotab;
    /// Array pointer (SCOTCH FORMAT) that stores the vertex weights in the graph (computed by computeArrays())
    int *velotab;


    /// Indexes all the unique edges in this graph
    std::vector< std::pair<int, int> > uniqueEdges;

    /// Index of each vertex in the graph
    std::map<int, MetisVertex *> vertices;


    /// @brief Constructs a MetisGraph
    MetisGraph(int numNodes, int numUniqueEdges, std::string formatStr = "", int vertexWeightsSize = 1);

    /// @brief Sets the graph's input file format string xxx
    void setGraphFormat(std::string formatStr);
    /// @brief Parses the format string xxx to extract the valid GraphFormats flags
    void parseFormat();
    /// @brief Returns true if the flag graphFormatFlag (GraphFormats) is set for this graph
    bool isGraphFormatFlagSet(int graphFormatFlag);
    /// @brief Prints some basic stats for this graph, for debug purposes
    void print();

    /// @brief Method to add a vertex to this graph (called by a load routine)
    bool addVertex(MetisVertex *vertex);

    /// @brief Tests wehter the edge is unique or already present in the graph
    bool isEdgeUnique(MetisEdge *edge);

    int numVertices();
    int numEdges();

    /// @brief computes the arrays that are used by SCOTCH
    void computeArrays();

  };

  /// @brief Loads a graph from a metis .txt file pointed at by path
  /// @return The MetisGraph object if successful, or nullptr
  MetisGraph  *loadGraphFromFile(std::string path);

  /// @brief Scans the header line of a METIS file.
  /// @return The MetisGraph object if valid header line found, or nullptr
  MetisGraph  *parseMETISHeader(std::string &header);

  /// @brief Parses a METIS node line given a valid header and graph
  void parseMETISNodeLine(std::string line, int nodeID, MetisGraph *graph);

  /// @brief Tests whether the line in the METIS file is a comment: starting with '%'
  bool lineIsComment(std::string &line);

  /// @brief Strips \n and \r characters from line.
  void cleanLine(std::string &line);

} // end namespace METIS


#endif
