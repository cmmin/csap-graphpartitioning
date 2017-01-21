
class Cl:
    def argFunc(self, arg1, arg2 = 1):
        if(arg2 == None):
            arg2 = 1
        if(arg1 == True):
            print('Appending', arg2)
            arg2 += 1
        print(arg1, arg2)

if __name__ == '__main__':
    c = Cl()
    c.argFunc(True)
    c.argFunc(True, 6)
    c.argFunc(True)
    c.argFunc(True, 8)
    c.argFunc(False)
    c.argFunc(False, 10)
    c.argFunc(False)
