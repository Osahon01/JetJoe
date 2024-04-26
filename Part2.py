from Part1 import W_Turb
import numpy as np
from sympy import symbols, Eq, solve
f, T_t3, T_t4 = symbols('f, T_t3, T_t4')

# Step 1 (Analytical instead of numerical in the other .py file)
# Oshaon I just solved your system by hand since we'll need to show a mathematical expression in Deliv. A
print("\nStep 1")

# Known variables
a1 = np.deg2rad(35.26)
b1 = -np.deg2rad(19)
Omega = 160000 * (2*np.pi)/60 # Convert from RPM to rad/s
r1 = 0.02293760598
OmegaR1 = Omega*r1
w_T = OmegaR1**2 * 1/(1 - np.tan(b1)/np.tan(a1))
print(f'w_T = {w_T} [J/kg]')

# Step 2
print("\nStep 2")
print("We chose eta_C = eta_T = 0.6")

# Step 3
print("\nStep 3")

# Known Variables
T_t2 = 300
T_t5 = 953.15 # 680 + 273.15
c_pC = 1004.5
c_pT = 1243.67
# shaft_pow = W_Turb() #From Part 1
h_f = 42 * 10**6 # [J/kg]  (Internal enthalpy of Kerosine found online)
gamma_C = 1.4
gamma_T = 1.3

# Calculate fuel fraction, combustor inlet temp.
f = (-1*(c_pT*T_t5+h_f)+np.sqrt((c_pT*T_t5+h_f)**2 - 4*h_f*(T_t2*c_pC-c_pT*T_t5)))/(2*h_f)
T_t3 = (1+f)*(w_T/c_pC) + T_t2
print(f'f = {f}')
print(f'T_t3  = {T_t3} K')

# Calculating Compressor pressure ratio
eta_C = 0.6 # WE SET THIS
comp_ratio = (eta_C*(T_t3/T_t2 - 1) + 1)**(gamma_C/(gamma_C-1))
print(f'Compression Ratio =  {comp_ratio}  assuming eta_C = {eta_C}')

# Step 4
print("\nStep 4")

# Calculate Turbine Inlet temp.
T_t4 = (c_pC*(T_t3-T_t2))/((1+f)*c_pT) + T_t5
print(f'T_t4 Analytical = {T_t4} K')

# Step 5
print("\nStep 5")

# Knowns
R = 287
eta_T = 0.60 # WE SET THIS
P_0 = 101325 # [Pa] Atmospheric pressure at sea level
P_t0 = P_0 # c_0 = 0 (atmosphere is initially at rest wrt inlet)
P_t2 = P_t0 # Stagnation pressure conserved along streamline up to the compressor
P_t3 = comp_ratio * P_0 # Centrifugal Compression occurs
P_t4 = P_t3 # Stagnation pressure conserved across the combustor

# Pressure after turbine as a function of thermal efficiency
P_t5 = P_t4*((T_t5/T_t4 - 1)/eta_T + 1)**(gamma_T/(gamma_T-1))
T_6 = 300
P6 = 101325
T_t6 = T_t5
P_t6 = P_t5
M6 = ((2/(gamma_T - 1))*((P6/P_t6)**(-1*(gamma_T - 1) / gamma_T) -1))**0.5
c6 = M6*((gamma_T*R*T_t6)**0.5) 
# T_t5s = T_t5 + (c_pC/c_pT)*((T_t3 - T_t2) / (f+1))*(1 - (1 / (eta_C - (eta_T - eta_C))))
# c6 = (2*c_pT*T_t5*(1-(T_t4/T_t5s)*((P_0/P_t3)**((gamma_T - 1)/gamma_T))))**0.5
print(f'c6 = {c6} and M6 = {M6}')

# Solve for mass flow after the turbine (but its the same everywhere)
A_NGV = 0.000698744409 # m^2 measured
M_4 = 1 # for choked NGV
DM_4 = M_4/(1 + ((gamma_T-1)/2)*M_4**2)**(1/2 * (gamma_T+1)/(gamma_T-1)) # corrected mass flow per unit area
# DM_5 = DM_4 # conserved along the turbine (I believe)
m4 = (DM_4 * A_NGV * P_t4 * (gamma_T)**(1/2))/(R*T_t4)**(1/2)
print(f'NGV mass flow = {m4} [kg/s]')

# Step 6
print("\nStep 6")
KE = (0.5*m4*c6**2)
print(f'KE_dot = {KE} [W = J/s]')

# Step 7
print("\nStep 7")
cfact = (3600*4.4448*(1/0.4536)) # (kg/s)/N to (lbm/hr)/lbf
T0 = 300
TSFC = (f / (c6*(f+1)))
TSFC_imperial = TSFC*cfact
T_spec = (f+1)*(c6 / ((gamma_C*287*T0)**0.5) )
print(f'TSFC = {TSFC} ; Specific Thrust = {T_spec}')
print(f'TSFC Imperial = {TSFC_imperial}')

# Calculating Inlet Mass Flow
m1 = m4/(1 + f) # Mass flow after combustor scaled down by amount of fuel added
print(f'Mass flow at inlet = {m1} [kg/s]')

# SANITY CHECK
print("\nCheck if our model is reasonable")
T = m4*c6
print(f'Thrust = {T} [N], Thrust Imperial: {T / 4.44822} [lbf]')
cfact2 = (1/4.482) * (1/60) * 16 # (lbm/N) * (min/hr)^-1 * oz/lbm
fuel_cons = T * TSFC_imperial * cfact2
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