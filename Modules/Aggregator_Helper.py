import numpy as np
from scipy.interpolate import lagrange

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