
import numpy as np
from sympy import symbols, Eq, solve
f, T_t3, T_t4 = symbols('f, T_t3, T_t4')

#Known Variables#
T_t2 = 300
T_t5 = 953.15
c_pC = 1004.5
c_pT = 1244
shaft_pow = 848538.165060560 #From Part 1
h_f = 46.2 * 10**6 # Placeholder

# Equations
eq1 = Eq((1+f) * c_pT * (T_t4-T_t5), c_pC * (T_t3-T_t2))
eq2 = Eq((1+f) * c_pT * T_t4, f*h_f + c_pC*T_t3)
eq3 = Eq(shaft_pow/c_pT, T_t4-T_t5)

#Solve
solution = solve((eq1, eq2, eq3), (f, T_t3, T_t4))
print(solution)