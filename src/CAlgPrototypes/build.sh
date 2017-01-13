g++ -Wall main.cpp utils.cpp metis.cpp iscotch.cpp -L../../tools/scotch/lib/macOS/ -lscotch -o scotch
install_name_tool -change libscotch.dylib ../../tools/scotch/lib/macOS/libscotch.dylib scotch
./scotch
