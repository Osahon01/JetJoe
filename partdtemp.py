from ThermoAssessment import ThermoAssessment
from DirectAssessment import DirectAssessment
from Model import Model
import numpy as np
import matplotlib.pyplot as plt
import math

# DIRECT AND THERMODYNAMIC ASSESSMENTS
idle = [45200]

RPM = [45200, 82900, 108100, 160000] 

# Direct Assessment Inputs from our Trials (Measured Parameters)
# (Values we measure; make sure to convert to specified units from run table)
# A vector for each parameter whose entries correspond with each trial in the run table at a specific RPM
# [Trial 1 , Trial 2, Trial 3, Trial 4 (Max RPM)] 

P0 = [101973.5004, 101973.5004,	101973.5004, 101973.5004] # [Pa] Cell Static Pressure
T0 = [295.05, 294.85, 296.55, 295.45] # [K] Inlet Temperature
F = [0.0001, 3.113755131, 64.94403558, 0.8896443231] # [N] Thrust
A1 = 0.004870958 # Inlet Area [m^2]
P1_dynamic = [0.0001, 33.34456, 593.23456, 0.0001] # [Pa] Inlet Duct Wall Dynamic Pressure
V = [0.0001, 0.15, 4.12, 0.0001] # [gal/hour] Fuel Flow

# Thermodynamic Assessment Inputs from our Trials (Measured Paramaters)

P0 = P0 # [Pa] Cell Static Pressure
T0 = T0 # [K] Inlet Temperature
Pt3 = [100663.496, 109626.684, 255106.12, 100663.496] # [Pa] Compressor Discharge Pressure
Tt3 = [314.65, 311.55, 424.45, 315.45] # [K] Compressor Discharge Temperature HIGH TEMPS FIX ISSUE
Tt5 = [293.15, 827.15, 1033.15, 349.15] # [K] Exhaust Gas Temperature
V = V # [gal/hour] Fuel Flow 
F = F # [N] Thrust
A1 = A1 # Inlet Area [m^2] 
delta_eta = 0.07 # WE DECIDE THIS -Joe (for simplicity to avoid the 6x6)

# Calculate Direct and Thermodyanmic Assessment outputs for each trial

direct_assessment = np.zeros((4, 4)) # 4 trials and 4 estimated outputs
thermo_assessment = np.zeros((4, 7)) # 4 trials and 7 estimated outputs
for i in range(len(direct_assessment[0])):
    # Direct Analysis for a given RPM
    direct_anal_trial = DirectAssessment(P0[i], T0[i], F[i], A1, P1_dynamic[i], V[i])
    direct_assessment[i] = direct_anal_trial.get_est_parameters()
    # Thermodynamic Analysis for a given RPM
    mf = direct_anal_trial.get_mf()
    m1 = direct_anal_trial.get_m1()
    thermo_anal_trial = ThermoAssessment(P0[i], T0[i], Pt3[i], Tt3[i], Tt5[i], mf, m1, delta_eta)
    thermo_assessment[i] = thermo_anal_trial.get_est_parameters()

print('\nDirect Assessment Output Table')
print(f'{np.array2string(direct_assessment, precision=4, floatmode="fixed")}')
print('\nThermodynamic Assessment Output Table')
print(f'{np.array2string(thermo_assessment, precision=4, floatmode="fixed")}')

# MODEL PREDICTIONS for each RPM

# Measured Parameters
a1 = 35.26 # [deg] Rotor angle 1
b1 = 19 # [deg] Rotor angle 2
A_NGV = 0.000698744409 # [m^2] measured

model_assessment = np.zeros((4, 5)) # 4 trials and 5 analytical outputs
for i in range(len(model_assessment)):
    # Direct Analysis for a given RPM
    model_anal_trial = Model(RPM[i], a1, b1, A_NGV)
    model_assessment[i] = model_anal_trial.performance_bid()

print('\nModel Prediction Output Table')
print(f'{np.array2string(model_assessment, precision=4, floatmode="fixed")}')

# PLOT/TABULATE, COMPARE, AND INTERPRET

# # Max RPM TSFC
# 
# ax1 = plt.figure()
# plt.bar(x=[1,2,3], height=TSFCs, label=bar_label)
# plt.title(f'')
# plt.ylabel(f'TSFC ')
# plt.show(block=True)

TSFCs = [model_assessment[3][4], direct_assessment[3][3]] #, thermo_assessment[3][6]]
spec_Ts = [model_assessment[3][3], direct_assessment[3][2], thermo_assessment[3][5]]

# Creating the figure and subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))  # 1 row, 2 columns

# First bar graph on the first axis
bar_label1 = ["Model", "Direct \nAssessment"] #, "Thermodynamic \nAssessment"]
ax1.bar(bar_label1, TSFCs, color='b', label='TSFC')
ax1.set_title(f'TSFC Comparison at Max RPM of {RPM[-1]}')
ax1.set_xlabel('Model Comparison')
ax1.set_ylabel(f'TSFC [lbm/hr / kg]')
ax1.legend()

# Second bar graph on the second axis
bar_label2 = ["Model", "Direct \nAssessment", "Thermodynamic \nAssessment"]
ax2.bar(bar_label2, spec_Ts, color='r', label='$F\'/ma$')
ax2.set_title(f'Specific Thrust Comparison at Max RPM of {RPM[-1]}')
ax2.set_xlabel('Model Comparison')
ax2.set_ylabel(f'Specific Thrust $F\'/ma$ [-]')
ax2.legend()

# Adjust layout to prevent overlap
fig.tight_layout()

plt.show()