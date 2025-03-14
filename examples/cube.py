import sys

from pysnark.runtime import snark

@snark
def cube(x,y):
    return x**y

print("The cube of", sys.argv[1], "is", cube(int(sys.argv[1]), int(sys.argv[2])))