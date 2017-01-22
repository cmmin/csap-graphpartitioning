# SCOTCH Partitioning Algorithms

- Author: 	Carlo Mattia Minciacchi
- Email:		carlo.minciacchi@cantab.net

This document contains a brief guide to the repository and code within. It will be updated as the project progresses.

Some basic documentation is presented here. More detailed documentation can be found within the source files in the repository.

Project Aims

- Implement fennel graph partitioning algorithms with SCOTCH or PaToH.

Objectives

- [x] Implement SCOTCH_graphMap() algorithm in C++
- [x] Implement SCOTCH_graphMapFixed() algorithm in C++
- [x] Port the algorithms to Python
- [] Fully working alternative to fennel algorithm
- [] Integrate algorithms with the larger partitioning algorithm

# Structure of Repository

### ```data``` Folder

Contains all the input and output files that are required to test the code to read/generate graphs or publish the outputs of graphs.

### ```docs``` Folder

Contains project documentation and third-party library documentation.

### ```src``` Folder

Contains ```cpp``` and ```python``` subfolders.

The ```cpp``` folder contains the graph partitioning algorithms implemented using C++ and SCOTCH shared object.

The ```python``` folder contains utilities to visualize graphs and the code for running SCOTCH algorithms from python.

### ```test``` Folder

Currently contains basic unit tests for the Python implementation of the SCOTCH wrapper.


### ```tools``` Folder

Contains the binaries of the shared libraries for various operating systems, to avoid having to re-build them for each machine.

Currently holds ```libscotch.dylib``` for ```macOS 64bit scotch v6.0.4``` and for ```linux 64 bit scotch v5.1 (incorrectly linked)```.


# C++ Graph Partitioner using SCOTCH

The implementation of a graph partitioning algorithm using SCOTCH is first written in C++ to ensure that the right calls and datastructures are implemented. The algorithm will be ported into python subsequently.

The source for the graph partitioner is in ```src/cpp/CAlgPrototypes```.

The current implementation is in the method ```gpart()``` in ```src/CAlgPrototypes/main.cpp```.

Default partitioning parameters were chosen.

Building the source creates a program called ```scotch``` that takes an input METIS graph file and runs graphMap to obtain the partitions for the vertices in the graph.

## Building on Linux

This requires ```libscotch-5.1.so``` to be installed on the system. For later versions, amend the ```build.sh``` script found in the folder, to point to the other version of libscotch.

```$ sudo apt-get install scotch```

Building the graph partitioner:

```
$ ./build.sh -linux
```

Build options: ```-r``` runs the program after building. ```-c``` removes the program before re-building.

## Building on macOS

This requires ```libscotch.dylib``` found in ```tools``` folder.


Building the graph partitioner:

```
$ ./build.sh -osx
```

Build options: ```-r``` runs the program after building. ```-c``` removes the program before re-building.

## Running the Graph Partitioner

The build script creates a program called scotch in the same folder. The program is currently hard-coded to read the METIS graph ```data/oneshot_fennel_weights.txt``` and upon successful partitioning, generates ```data/oneshot_fennel_partitions.txt```

```
$ cd src/cpp/CAlgPrototypes
$ ./scotch
```

## Visualising the Partions

To visualise the partitions and graph, there is a d3js html visualisation found at ```data/socialNetwork.html```.

Requires ```graphviz``` package.

```
$ pip3 install graphviz
```

To update the visualisation to the latest data in ```data/oneshot_fennel_partitions.txt```:

```
$ cd src/python
$ python3 run_metis_graph.py
... generates .json file read
by socialNetwork.html ...
```

# Basic Python Interface to SCOTCH

The basic code to interface Python with SCOTCH has been implemented, including some unit tests in ```src/python```.

The python modules include some code to read METIS graphs and populate the arrays required by SCOTCH.

This code will be updated once the C++ implementaiton of the partitioning algorithms is completed.
