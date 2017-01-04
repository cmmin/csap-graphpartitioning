# SCOTCH Setup Instructions

Download: https://www.labri.fr/perso/pelegrin/scotch/#resources

Compile the library on your system using the ```INSTALL.txt``` instructions in the SCOTCH folder:

1. make a symbolic link to the correct makefile for your system from from Make.inc folder in ```libscotch/src/``` (i.e. for macOS: ```Makefile.inc.i686_mac_darwin10.icc```)

```
$ cd to/libscotch/src
$ ln -s Make.inc/Makefile.inc.xxxxxx Makefile.inc
$ make
```
