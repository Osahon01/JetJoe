from Part1 import W_Turb
import numpy as np
from sympy import symbols, Eq, solve
f, T_t3, T_t4 = symbols('f, T_t3, T_t4')

#Known Variables#
T_t2 = 300
T_t5 = 953.15 # 680 + 273.15
c_pC = 1004.5
c_pT = 1243.67
shaft_pow = W_Turb() #From Part 1
h_f = 42 * 10**6 # [J/kg] Placeholder (Kerosine)
gamma_C = 1.4
gamma_T = 1.3

# Equations
eq1 = Eq((1+f) * c_pT * (T_t4-T_t5), c_pC * (T_t3-T_t2))
eq2 = Eq((1+f) * c_pT * T_t4, f*h_f + c_pC*T_t3)
eq3 = Eq(shaft_pow/c_pT, T_t4-T_t5)
# Proposed different eq3 using compressor should yield same result
eq3_prime = Eq(shaft_pow/c_pC, T_t3-T_t2)

#Solve
solution = solve((eq1, eq2, eq3), (f, T_t3, T_t4))
print(solution)
f = solution[0][0]
T_t3 = solution[0][1]
T_t4 = solution[0][2]
# Solution for eq3 prime using compressor specific work instead
solution_prime = solve((eq1, eq2, eq3_prime), (f, T_t3, T_t4))
print("\n\n Alternatively\n")
print(solution_prime)
print("\n\n Analytical solution")
# Why is it slightly different?

# Analytical Solution for step 3 (solved by hand)
f = (-1*(c_pT*T_t5+h_f)+np.sqrt((c_pT*T_t5+h_f)**2 - 4*h_f*(T_t2*c_pC-c_pT*T_t5)))/(2*h_f)
T_t3 = (1+f)*(shaft_pow/c_pC) + T_t2
print("f Analytical = ", f)
print("T_t3 Analytical = ", T_t3)

# Solving for Compressor pressure ratio
eta_C = 0.7 # WE SET THIS (burner value for now)
comp_ratio = (eta_C*(T_t3/T_t2 - 1) + 1)**(gamma_C/(gamma_C-1))
print("Compression Ratio = ", comp_ratio, " assuming eta_C = ", eta_C)

# Analytical Solution for step 4
T_t4 = (c_pC*(T_t3-T_t2))/((1+f)*c_pT) + T_t5
print("T_t4 Analytical = ", T_t4)