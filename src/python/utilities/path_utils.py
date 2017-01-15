import os
import os.path

def checkFileExists(path):
    ''' Checks if path points to a valid existing file on the system '''
    if(os.path.exists(path)):
        if(os.path.isfile(path)):
            return True
    return False

def checkFileExtensionValid(path, validExtensionsList):
    ''' Checks if the path string ends with the right extension'''
    for extension in validExtensionsList:
        if(path.endswith(extension)):
            return True
    return False
