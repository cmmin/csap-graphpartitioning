
def checkArgType(arg, typeClass):
    if isinstance(arg, typeClass):
        return True
    else:
        return False

def checkArgtypeConvert(arg, typeClass, tryConvert):
    if(checkArgType(arg, typeClass)) == True:
        return True
    else:
        if tryConvert == False:
            return False

        try:
            convertedVal = typeClass(arg)
            return True
        except ValueError as err:
            return False

def isInt(arg, tryConvert = False):
    ''' Checks if argument is of integer type '''
    return checkArgtypeConvert(arg, int, tryConvert)

def isFloat(arg, tryConvert = False):
    ''' Checks if argument is of float type '''
    return checkArgtypeConvert(arg, float, tryConvert)

'''
def isInt(arg, tryConverting = True):
    if isinstance(arg, int):
        return True
    else:
        if(tryConverting):
            try:
                iArg = int(arg)
                return True
            except ValueError as err:
                return False
    return False
'''

def isStr(arg):
    ''' Checks if argument is of type string '''
    return checkArgtypeConvert(arg, str, tryConvert = False)
