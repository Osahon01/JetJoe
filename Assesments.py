# DIRECT ASSESSMENT BASED ON MEASUREMENTS

# Constants
R = 287
gamma_C = 1.4
rho_fuel = 6.843 # [lbm/gal] Density of fuel (known)
A_duct = 0.00225806 # [m^2] (3.5in^2 converted to m^2)

# Measured Parameters (Values we measure; make sure to convert to specified units from run table)
P0 = 1 # [Pa] Cell Static Pressure
T0 = 1 # [K] Inlet Temperature
F = 1 # [N] # Thrust
A1 = 1 # Inlet Area [m^2]
P1_dynamic = 2 # [Pa] Inlet Duct Wall Dynamic Pressure
V = 1 # [gal/hour] Fuel Flow

# Calculate derived parameters from knowns
P1 = P0 - P1_dynamic # [Pa] Inlet Static Pressure
mf_imperial = rho_fuel*V # [lbm/hr]
F_imperial = F/4.4482 # [lbf]
mf = mf_imperial * 0.4536/3600 # [kg/s]

# Estimated Parameters (Values we calculate)
M1 = (2/(gamma_C-1)*((P0/P1)**((gamma_C-1)/gamma_C)-1))**0.5
m1 = A1*P0/(T0)**0.5 * (gamma_C/R)**0.5 * M1/((1 + (gamma_C-1)/2 * M1**2)**((gamma_C+1)/2*(gamma_C-1)))
spec_T = F/(m1*(gamma_C*R*T0)**0.5)
TSFC_imperial = mf_imperial/F_imperial
print(f'Estimated Parameters \nInlet Mach No. = {M1} [-] \nInlet Mass Flow = {m1} [kg/s] \nSpecific Thrust = {spec_T} [-] \nTSFC = {TSFC_imperial} [(lbm/hr)/lbf]')

# THERMODYNAMIC ASSESSMENT

# Additional Constants
gamma_T = 1.3
cpC = 1004.5
cpT = 1243.67

# Measured Parameters
Pt3 = 3 # [Pa] Compressor Discharge Pressure
Tt3 = 3 # [K] Compressor Discharge Temperature
Tt5 = 5 # [K] EGT (Exhaust Gas Temperature)
