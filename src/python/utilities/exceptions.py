class LibraryLoadException(Exception):
    ''' An exception caused by a problem with loading external libraries '''

class MetisGraphFormatException(Exception):
    ''' An Exception caused by a format string error in a metis graph file '''


def noExceptPropagate(func):
    try:
        ret = func()
        return ret
    except Exception as err:
        print(err)
        return None
