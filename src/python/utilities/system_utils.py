import platform

class OS(Enum):
    linux   = 1
    macOS   = 2
    windows = 3

def isMacOS():
    if 'Darwin' in platform.system():
        return True
    return False

def isLinux():
    if 'Linux' in platform.system():
        return True
    return False

def getOS():
    operatingSystem = platform.system()
    if 'Darwin' in operatingSystem:
        return OS.macOS
    elif 'Linux' in operatingSystem:
        return OS.linux
    else:
        print('Error, unhandled case: windows')

    return OS.windows
