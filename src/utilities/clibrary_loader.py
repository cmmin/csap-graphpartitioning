from ctypes import cdll

import utilities.exceptions as exceptions
from utilities.path_utils import checkFileExists, checkFileExtensionValid

class CLibrary:
    def __init__(self, libraryPath=''):
        self.libraryPath = libraryPath
        self.library = None

    def isLoaded(self):
        if self.library is None:
            return False
        return True

    def load(self):
        ''' Wrapper for loadLibrary(). Handles raised exceptions.'''
        try:
            self._loadLibrary()
        except exceptions.LibraryLoadException as error:
            print("Failed to load library: ", str(error))
        except Exception as e:
            print("Failed to load library:", str(e))

    def _loadLibrary(self):
        self.setLibraryPath(self.libraryPath)
        self.library = cdll.LoadLibrary(self.libraryPath)

    def setLibraryPath(self, newLibraryPath):
        try:
            self._checkLibraryPath(newLibraryPath)
            self.libraryPath = newLibraryPath
            return True

        except exceptions.LibraryLoadException as err:
            print("Could not set Library path:", str(err))
        except Exception as e:
            print("Unknown exception in CLibrary.setLibraryPath(),", str(e))

        return False

    def _checkLibraryPath(self, libraryPath):
        if(len(libraryPath) == 0):
            raise exceptions.LibraryLoadException("Library path is empty.")

        # check if path exists and is valid extension
        if(checkFileExists(libraryPath) == False):
            raise exceptions.LibraryLoadException("Could not locate library at " + libraryPath)

        if(checkFileExtensionValid(libraryPath, self._libExtensions()) == False):
            extParts = libraryPath.split(".")
            extension = extParts[len(extParts) - 1] # get the last index, which should be the extension if the filepath has .extension in it
            raise exceptions.LibraryLoadException("Library has unsopported extension " + extension)

        return True

    def _libExtensions(self):
        return [".dll", ".so", ".a"]
