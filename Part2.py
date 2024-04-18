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
h_f = 42 * 10**6 # [J/kg]  (Kerosine)
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
# solution_prime = solve((eq1, eq2, eq3_prime), (f, T_t3, T_t4))
# print("\n\n Alternatively\n")
# print(solution_prime)
# Why is it slightly different?

print("\n\n Analytical solution")
# Analytical Solution for step 3 (solved by hand)
f = (-1*(c_pT*T_t5+h_f)+np.sqrt((c_pT*T_t5+h_f)**2 - 4*h_f*(T_t2*c_pC-c_pT*T_t5)))/(2*h_f)
T_t3 = (1+f)*(shaft_pow/c_pC) + T_t2
print("f Analytical = ", f)
print("T_t3 Analytical = ", T_t3, " K")

# Solving for Compressor pressure ratio
eta_C = 0.1 # WE SET THIS (burner value for now)
comp_ratio = (eta_C*(T_t3/T_t2 - 1) + 1)**(gamma_C/(gamma_C-1))
print("Compression Ratio = ", comp_ratio, " assuming eta_C = ", eta_C)

# Analytical Solution for step 4
T_t4 = (c_pC*(T_t3-T_t2))/((1+f)*c_pT) + T_t5
print("T_t4 Analytical = ", T_t4, " K")

# STEP 5

# Knowns
R = 287
eta_T = 0.8 # WE SET THIS
A_T = 0.00258064 # [m^2] (measured) (DUMMY VALUE 4 in^2)
P_0 = 101325 # [Pa] in atmosphere
P_t0 = P_0
P_t2 = P_t0
P_t3 = comp_ratio * P_0
P_t4 = P_t3 # assuming constant pressure combustion

# Pressure after turbine as a function of thermal efficiency
P_t5 = P_t4*((T_t5/T_t4 - 1)/eta_T + 1)**(gamma_T/(gamma_T-1))
P6 = 101325
T_t6 = T_t5
P_t6 = P_t5
M6 = ((2/(gamma_T - 1))*((P6/Pt6)**((gamma_T - 1) / gamma_T) -1))**0.5
c6 = M6*(gamma_T*287*T_t6)

# Solve for mass flow after the turbine (but its the same everywhere)
M_4 = 1 # for choked NGV
DM_4 = M_4/(1 + ((gamma_T-1)/2)*M_4**2)**(1/2 * (gamma_T+1)/(gamma_T-1)) # corrected mass flow per unit area
DM_5 = DM_4 # conserved along the turbine (I believe)
m = (DM_5 * A_T * P_t5 * (gamma_T)**(1/2))/(R*T_t5)**(1/2)
print("Mass flow = ", m, " kg/s")

# # STEP 6
# A_6 = 0.0013283844 # [m^2] measured; converted from 2.059 in^2
# A_4 = 0.001 # [m^2] measured (DUMMY VALUE TIL WE CALCULATE)
# # Solve for Mach number at nozzle exit
# M_6 = symbols('M_6')
# f_M = Eq(A_6/A_4, 1/M_6*(2/(gamma_T+1)*(1 + (gamma_T-1)/2 * M_6**2))**(1/2 * (gamma_T-1)/(gamma_T+1)))
# solution = solve((f_M), (M_6))
# print(solution)
# print("TEst")
