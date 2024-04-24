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

print("\n\n Analytical solution")
# Analytical Solution for step 3 (solved by hand)
f = (-1*(c_pT*T_t5+h_f)+np.sqrt((c_pT*T_t5+h_f)**2 - 4*h_f*(T_t2*c_pC-c_pT*T_t5)))/(2*h_f)
T_t3 = (1+f)*(shaft_pow/c_pC) + T_t2
print("f Analytical = ", f)
print("T_t3 Analytical = ", T_t3, " K")

# Solving for Compressor pressure ratio
eta_C = 0.6 # WE SET THIS (burner value for now)
comp_ratio = (eta_C*(T_t3/T_t2 - 1) + 1)**(gamma_C/(gamma_C-1))
print("Compression Ratio = ", comp_ratio, " assuming eta_C = ", eta_C)

# Analytical Solution for step 4
T_t4 = (c_pC*(T_t3-T_t2))/((1+f)*c_pT) + T_t5
print("T_t4 Analytical = ", T_t4, " K")

# STEP 5

# Knowns
R = 287
eta_T = 0.60 # WE SET THIS
P_0 = 101325 # [Pa] in atmosphere
P_t0 = P_0
P_t2 = P_t0
P_t3 = comp_ratio * P_0
P_t4 = P_t3 # assuming deltaKE is negligible in combustor

# Pressure after turbine as a function of thermal efficiency
P_t5 = P_t4*((T_t5/T_t4 - 1)/eta_T + 1)**(gamma_T/(gamma_T-1))
T_6 = 300
P6 = 101325
T_t6 = T_t5
P_t6 = P_t5
M6 = ((2/(gamma_T - 1))*((P6/P_t6)**(-1*(gamma_T - 1) / gamma_T) -1))**0.5
c6 = (2*c_pT*T_t5*(1-(T_t4/T_t5)*((P_0/P_t3)**((gamma_T - 1)/gamma_T))))**0.5

print("c6 = ", c6, " and M6 = ", M6)

# Solve for mass flow after the turbine (but its the same everywhere)
A_NGV = 0.000698744409 # m^2
M_4 = 1 # for choked NGV
DM_4 = M_4/(1 + ((gamma_T-1)/2)*M_4**2)**(1/2 * (gamma_T+1)/(gamma_T-1)) # corrected mass flow per unit area
# DM_5 = DM_4 # conserved along the turbine (I believe)
m4 = (DM_4 * A_NGV * P_t4 * (gamma_T)**(1/2))/(R*T_t4)**(1/2)
KE = (0.5*m4*c6**2) #STEP 6 --> verify on piazza
print(f'NGV mass flow = {m4} [kg/s] ; KE_dot = {KE} [W = J/s]')

# STEP 7
cfact = (3600*4.4448*(1/0.4536)) # (kg/s)/N to (lbm/hr)/lbf
T0 = 300
TSFC = (f / (c6*(f+1)))
TSFC_new = TSFC*cfact
T_spec = (f+1)*(c6 / ((gamma_C*287*T0)**0.5) )
print(f'TSFC = {TSFC} ; Specific Thrust = {T_spec}')
print(f'TSFC Imperial = {TSFC_new}')
# Calculating Inlet Mass Flow
m1 = m4/(1 + f)
print(f'Mass flow at inlet = {m1} [kg/s]')

# SANITY CHECK
T = m4*c6
print(f'Thrust = {T} [N], Thrust Imperial: {T / 4.44822}')
cfact2 = (1/4.482) * (1/60) * 16 # (lbm/N) * (min/hr)^-1 * oz/lbm
fuel_cons = T * TSFC_new * cfact2
print(f'Fuel consumption = {fuel_cons} [oz/min]')

# DIRECT ASSESSMENT BASED ON MEASUREMENTS
# Values we measure
A_1 = 0 # Inlet Area [m^2]
T_0 = 0 # [K]
P_0 = 0 # [Pa] Cell Pressure
P_dynamic = 0 
P_1 = P_0 - P_dynamic
# Values we calculate
#M_1 = (2/(gamma_C-1)*(STUFF))
#m1 = A_1*P_0/(T_0)**0.5 * (gamma_C/R)**0.5 * M_1/((1 + (gamma_C-1)/2 * M_1**2)**((gamma_C+1)/2*(gamma_C-1)))