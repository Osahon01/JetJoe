# DIRECT ASSESSMENT BASED ON MEASUREMENTS

# Constants
R = 287
gamma_C = 1.3

# Measured Parameters (Values we measure; make sure to convert to specified units from run table)
A1 = 0.00225806 # Inlet Area [m^2] (3.5in^2 converted to m^2)
T0 = 1 # [K]
P0 = 1 # [Pa] Cell Static Pressure
P_dynamic = 2 # [Pa] Inlet Duct Wall Dynamic Pressure
P1 = P0 - P_dynamic # [Pa] Inlet Static Pressure
F = 1 # [N] # Thrust
V = 1 # [gal/hour] Fuel Flow
rho_fuel = 6.843 # [lbm/gal] Density of fuel (known)
mf = rho_fuel*V # [lbm/hr]

# Estimated Parameters (Values we calculate)
M1 = (2/(gamma_C-1)*((P0/P1)**((gamma_C-1)/gamma_C)-1))**0.5
m1 = A1*P0/(T0)**0.5 * (gamma_C/R)**0.5 * M1/((1 + (gamma_C-1)/2 * M1**2)**((gamma_C+1)/2*(gamma_C-1)))
spec_T = F/(m1*(gamma_C*R*T0)**0.5)
TSFC = mf/F
print(f'Estimated Parameters \nInlet Mach No. = {M1} [-] \nInlet Mass Flow = {m1} [kg/s] \nSpecific Thrust = {spec_T} [-] \nTSFC = {TSFC} [(lbm/hr)/lbf]')
