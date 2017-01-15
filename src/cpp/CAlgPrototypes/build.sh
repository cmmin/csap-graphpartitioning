#!/bin/bash

# testing the input
if [[ $# -lt 1 ]]; then
  echo "Usage Instructions"
  echo "Required: one of -osx(-macOS) or -unix(-linux)"
  echo ""
  echo "-osx to build for macOS"
  echo "-unix to build for linux"
  echo ""
  echo "Options"
  echo "-run, -r to automatically run binary after building"
  echo "-clean, -c to remove built binary"
  echo "-help, -h to show this"
  exit 3
fi

# 0=none 1=macOS, 2=linux
build=0
clean=0
run=0

for var in "$@"
do
  if [[ "$var" == "-clean" ]] || [[ "$var" == "-c" ]]; then
    let clean=1
  fi
  if [[ "$var" == "-run" ]] || [[ "$var" == "-r" ]]; then
    let run=1
  fi
  if [[ "$var" == "-osx" ]] || [[ "$var" == "-macOS" ]]; then
    if [[ build -gt 0 ]]; then
      echo "Error: already specified a build type."
      exit 2
    fi
    let build=1
  fi
  if [[ "$var" == "-unix" ]] || [[ "$var" == "-linux" ]]; then
    if [[ build -gt 0 ]]; then
      echo "Error: already specified a build type."
      exit 2
    fi
    let build=2
  fi

  if [[ "$var" == "-help" ]] || [[ "$var" == "-h" ]]; then
    echo "Usage Instructions"
    echo "Required: one of -osx(-macOS) or -unix(-linux)"
    echo ""
    echo "-osx to build for macOS"
    echo "-unix to build for linux"
    echo ""
    echo "Options"
    echo "-run, -r to automatically run binary after building"
    echo "-clean, -c to remove built binary"
    echo "-help, -h to show this"
    exit 1
  fi
done

if [[ $build -lt 1 ]]; then
  echo "Error, please specify -osx or -unix"
  exit 2
fi

if [[ $clean -gt 0 ]]; then
  echo "Removing old binary"
  echo "rm scotch"
  echo ""
  rm scotch
fi

if [[ $build == 1 ]]; then
  echo "Building for macOS"
  echo "g++ -Wall main.cpp utils.cpp metis.cpp iscotch.cpp -L../../tools/scotch/lib/macOS/ -lscotch -o scotch"
  g++ -std=c++11 -Wall main.cpp utils.cpp metis.cpp iscotch.cpp -L../../../tools/scotch/lib/macOS/ -lscotch -o scotch
  echo ""
  echo "Build Done."
  echo ""
  echo "Updating executable to point to correct library."
  echo "install_name_tool -change libscotch.dylib ../../tools/scotch/lib/macOS/libscotch.dylib scotch"
  install_name_tool -change libscotch.dylib ../../../tools/scotch/lib/macOS/libscotch.dylib scotch
  echo ""
fi

if [[ $build == 2 ]]; then
  echo "Building for linux - NOT SUPPORTED UNTIL LIBSCOTCH.so is available."
  exit 2
  echo "g++ -Wall main.cpp utils.cpp metis.cpp iscotch.cpp -L../../tools/scotch/lib/macOS/ -lscotch -o scotch"
  g++ -Wall main.cpp utils.cpp metis.cpp iscotch.cpp -L../../../tools/scotch/lib/macOS/ -lscotch -o scotch
  echo ""
  echo "Build Done."
  echo ""
  echo "Updating executable to point to correct library."
  echo "install_name_tool -change libscotch.dylib ../../tools/scotch/lib/macOS/libscotch.dylib scotch"
  install_name_tool -change libscotch.dylib ../../../tools/scotch/lib/macOS/libscotch.dylib scotch
  echo ""
fi

if [[ $run == 1 ]]; then
  echo "Running program."
  echo "./scotch"
  echo ""
  ./scotch
fi


#g++ -Wall main.cpp utils.cpp metis.cpp iscotch.cpp -L../../tools/scotch/lib/macOS/ -lscotch -o scotch
#install_name_tool -change libscotch.dylib ../../tools/scotch/lib/macOS/libscotch.dylib scotch
#./scotch
