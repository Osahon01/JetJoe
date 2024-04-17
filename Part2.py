from Part1 import W_Turb
# from Part_1 import TurbineWork_glob()
import math
import numpy as np
from sympy import symbols, Eq, solve
#from sympy.abc import *
f, Tt3 = symbols('f, Tt3')

# Equations
Tt2 = 300
Tt4 = ?
Tt5 = 680 + 273
hf = ?
cp = ?
ws_dot = W_Turb()
eq1 = Eq((1+f)*cp_T*(Tt4-Tt5), cp_C*(Tt3-Tt2))
eq2 = Eq((1+f)*cp_T*(Tt4), f*hf + cp_C*Tt3)
eq3 = Eq(cp*(Tt4 - Tt5), ws_dot)
# W_t = W_Turb()