import numpy as np
from math import gcd

def inverseMod26(matrix):
    det = np.linalg.det(matrix)
    if det == 0: raise np.linalg.LinAlgError("Singular Matrix")
    if len(matrix[0]) == 2:
        adjugate = np.array([[matrix[1][1],-matrix[0][1]%26],
                             [-matrix[1][0]%26,matrix[0][0]]]
        )
    else: raise NotImplementedError("Matrix size not implemented")
    return np.dot(inversemodp(int(round(det%26)),26),adjugate)%26

def generalizedEuclidianAlgorithm(a, b):
    if b > a:
        #print a, b
        return generalizedEuclidianAlgorithm(b,a);
    elif b == 0:
        return (1, 0);
    else:
        #print a,b
        (x, y) = generalizedEuclidianAlgorithm(b, a % b);
        return (y, x - (a // b) * y)

def inversemodp(a, p):
    a = a % p
    if gcd(a,p) > 1: raise ValueError("a and p are not coprime")
    (x,y) = generalizedEuclidianAlgorithm(p, a % p);
    return y % p
