import rsa
import numpy as np
from scipy.interpolate import lagrange
from numpy.polynomial.polynomial import Polynomial
import matplotlib.pyplot as plt
from tqdm import tqdm
from typing import List, Tuple


def rsaGenKey(numbit = 4096):
  """
  Gen key follow RSA
  -------
  Input:
    - numbit: specify the number of bits of key
  output:
    - (e,m): public key
    - (d,m): private key
  """
  _, allkey = rsa.newkeys(numbit)
  m = allkey['n']
  e = allkey['e']
  d = allkey['d']
  return (e,m), (d,m) 

def genSecret(exp = 10):
  """
  Gen pair secret and self secret for client
  -------
  Input:
    - exp: specify the large of secret by exponent 
  Output:
    - ps: pair secret
    - ss: self secret
  """
  ps = np.random.randint(0,2**exp)
  ss = np.random.randint(0,2**exp)
  return ps, ss

def genPointofCurve(order: int, coeff_limit: int, point_num = -1):
  """
  Gen Points in Curve
  -------
  Input:
    - order: order of the function. e.g. x^2 + x + 1 has order of 2
    - coeff_limit: range to limit the large of coeff
    - point_num: number of points in curve to generate
  Output:
    - coeffs: coeffs of curve
    - X,Y: Points in curve
  """
  point_num = order+1 if point_num<=order else point_num

  # Create coeffs
  coeffs = np.random.randint(-coeff_limit, coeff_limit, order+1)
  if coeffs[0] == 0:
    coeffs[0] = 1

  # Get points
  X = np.random.choice(range(-point_num//2-1, point_num//2+1), point_num, False)
  Y = [np.sum(coeffs*([x]**np.array(range(order, -1, -1)))) for x in X]
  
  return (coeffs, X, Y)

def regenCurve(X: list[int], Y: list[int]):
  """
  Regenerate Curve using list of Points
  -------
  Input: 
    - X: list of Points in axis x
    - Y: list of Points in axis y
  Output:
    - regen poly curve
  """
  lagrange_poly = np.poly1d(lagrange(X, Y).coefficients.round().astype(np.int64))
  return lagrange_poly

def exponent_mod(b: int, e: int, m: int):
  """
  Fast exponent modulo function
  -------
  Input:
    - b: base
    - e: exponent
    - m: modulo
  Output:
    - result: b^e modulo m
  """
  result = 1
  while e > 0:
    if e % 2:
      b, e, result = (b * b) % m, e // 2, (b * result) % m
    else:
      b, e, result = (b * b) % m, e // 2, result
  return result


def checkXY(poly: np.poly1d, X: np.ndarray, Y: np.ndarray):
  """
  Check regen poly by Points
  -------
  Input:
    - poly: regen polynomial function
    - X: Points in axis x
    - Y: True axis y of points x
  Output:
    True if regen poly is correct
  """
  Y_from_poly = poly(X)
  return all(Y_from_poly==Y)

def checkCoeffs(poly: np.poly1d, coeffs: np.ndarray):
  """
  Check regen poly by Coeffs
  ------
  Input:
    - poly: regen polynomial function
    - coeffs: coeffs of true poly
  OutputL
    True if regen poly is correct
  """
  return all(poly.coefficients==coeffs)

def maskModel(wlm: int, neighbors: List[Tuple[int, int]], ps: int, ss: int, self_id: int, g: int, q: int):
    """
    Mask Local model by sharing secret
    -------
    Input:
      - wlm: weights local model in integer
      - neigbors: id and public of each neighbor
      - ps: pair secret of this local
      - ss: self secret of this local
      - self_id: id of this local
      - g: parameter of diffie-helman
      - q: parameter of diffie-helman
    Output:
      - masked local model
    """
    self_public = pow(g, ps, q)

    for neighbor_id, neighbor_public in neighbors:
        sign = -1 if self_id > neighbor_id else 1
        wlm = (wlm + sign * self_public * neighbor_public) % q

    return (wlm + ss) % q  

#Test
# (e,m), (d,m) = rsaGenKey()
# print(e)
# print(m)
# print(d)

# ps,ss = genSecret()
# print(ps)
# print(ss)

# for testcase_ID in tqdm(range(10000)):
#   #print(f"Testcase #{testcase_ID}", end=" ")

#   coeffs, X, Y = genPointofCurve(order = 15, coeff_limit = 3, point_num = 16)
#   lagrange_poly = np.poly1d(lagrange(X, Y).coefficients.round().astype(np.int64))

#   if not checkXY(lagrange_poly, X, Y):
#     print(f"TESTCASE #{testcase_ID} FAILED CHECK XY!")
#     print(coeffs)
#     print(lagrange_poly.coefficients)
#     print(X)
#     print(Y)
#     quit()
#   elif not checkCoeffs(lagrange_poly, coeffs):
#     print(f"TESTCASE #{testcase_ID} FAILED CHECK COEFFS!")
#     print(coeffs)
#     print(lagrange_poly.coefficients)
#     print(X)
#     print(Y)
#     quit()
  
#print("SUCCESS!")

# print(exponent_mod(2,10000000000000000000000 ,19472468722417397862558857150087778833563567447828596137285949137713554888004771279233477394582204013249209520541369050915998789018565616266327796914086325427778753887468211249285574734294151829310027214581775193890142939838132633371974477813502883331360744022497806724741968550141407644231522327645042702362263231672364430967906551566700028939158562682842922050404300793021053108400897416440694342611660893657584496011521574815551724188606262074259571796638737602576098759418276877681850654914056243425729800720713560064186603082272673535566186497264161034856105408817239711481740341605347326896143605436974992107063))
