from Part1 import TurbineWork_glob
# from Part_1 import TurbineWork_glob()
import math
import numpy as np
from sympy import symbols, Eq, solve
#from sympy.abc import *
f, Tt3 = symbols('f, Tt3')

# Equations
a1 = np.deg2rad(35.26)
b1 = np.deg2rad(19)
Omega = 4398.2316
r1 = 0.0393760598
TurbineWork_glob()
# W_t = W_Turb()