g++ -Wall tests.cpp utils.cpp metis.cpp -L../../tools/scotch/lib/macOS/ -lscotch -o test
install_name_tool -change libscotch.dylib ../../tools/scotch/lib/macOS/libscotch.dylib test
./test
