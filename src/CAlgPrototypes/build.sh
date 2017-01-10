g++ -Wall main.cpp -L../../tools/scotch/lib/macOS/ -lscotch -o scotch
install_name_tool -change libscotch.dylib ../../tools/scotch/lib/macOS/libscotch.dylib scotch
./scotch
