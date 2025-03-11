import pandas as pd
import random
from sympy import isprime, primitive_root

def gen_DHparam(index:int):
  """
  Generate q and g for diffie-helman
  -------
  Input:
    - index: used for loop statement to prevent pick the same params in file
  Output:
    - (q, g): diffie-helman params
  """
  dhparams = pd.read_csv("dfparam.csv")
  qs = dhparams['q']
  gs = dhparams['g']
  return (int(qs[index]), int(gs[index]))
  

def genPedersenParameter():
  """
  Generate arguments for Pedersen Commitment
  -------
  Input:
    None
  Output:
    - p,h,k to gen commitment: (h^global_model k^r) mod p
  """
  p = gen_large_prime()
  h = find_primitive_root(p)
  k = random.randint(1,2**10)
  return p,h,k

def genID(listID: list[int], nlistID: list[int]):
  """
  Generate ID for client when client sends regist
  -------
  Input:
    - listID: list of ID generated for all the clients before
    - nlistID: new list of ID for all clients in this round
  Output:
    None
  """
  id = random.randint(0,2**10)
  while id in listID or id in nlistID:
    id = random.randint(0,2**10)
  nlistID.append(id)
  return

################################## SUPPORT FUNCTION ####################################
def gen_prime_candidate(length: int):
    """ 
    Generate an odd integer randomly 
    -------
    Input:
      - length: bit length of random number p
    Output:
      - p: random number with bit length "length"
    """
    p = random.getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p

def gen_large_prime(length=10):
    """
    Generate a prime number of specified bit length
    -------
    Input:
      - length: bit length of random number p
    Output:
      - p: prime number with bit length "length"
    """
    p = 4
    # keep generating while the number is not prime
    while not isprime(p):
        p = gen_prime_candidate(length)
    return p

def find_primitive_root(p: int):
    """
    Find a primitive root for prime p
    -------
    Input:
      - p: prime number
    Ouput:
      - primitive root of p 
    """
    return primitive_root(p)
##################################### END ###########################################



# Test
# for i in range(100):
#   q, g = gen_DHparam(i)
#   print(q)
#   print(g)

