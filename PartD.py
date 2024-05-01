from ThermoAssessment import ThermoAssessment
from DirectAssessment import DirectAssessment
from Model import Model
import numpy as np
import matplotlib.pyplot as plt
import math

# DIRECT AND THERMODYNAMIC ASSESSMENTS


### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!! ALL VALUES ARE AS ENTERED FROM THE SENSORS
# FROM THE VIDEO, NEED TO CONVERT !!!###
# Any value with none is not entered yet
### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Found an "idle" state (least RPM before cooling)
# RPM, timestamp 
idle = [43500,5.40]


# RPM's where I could find decent pausing times
# for measurements. Corresponding timestamp in
# video 2 (should be same in 1)
RPM = [107000, 130000, 148000,160000] 
timestamps = [3.24, 3.50, 4.13, 4.59]
## These correspond to the trials below


# Direct Assessment Inputs from our Trials (Measured Parameters)
# (Values we measure; make sure to convert to specified units from run table)
# A vector for each parameter whose entries correspond with each trial in the run table at a specific RPM
# [Trial 1 , Trial 2, Trial 3, Trial 4 (Max RPM)] 

P0 = [None, None, None, 14.81] # [Pa] Cell Static Pressure
T0 = [None, None, None, 23.1] # [K] Inlet Temperature
F = [None, None, None, 14.6] # [N] Thrust
A1 = np.pi * 0.0229**2 # Inlet Area [m^2]
P1_dynamic = [None, None, None, 23.96] # [Pa] Inlet Duct Wall Dynamic Pressure
V = [None, None, None, None] # [gal/hour] Fuel Flow

# Thermodynamic Assessment Inputs from our Trials (Measured Paramaters)

P0 = P0 # [Pa] Cell Static Pressure
T0 = T0 # [K] Inlet Temperature
Pt3 = [None, None, None, 37] # [Pa] Compressor Discharge Pressure
Tt3 = [None, None, None, 148.3] # [K] Compressor Discharge Temperature
Tt5 = [None, None, None, 756] # [K] Exhaust Gas Temperature
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

bar_label = ["Model", "Direct \nAssessment", "Thermodynamic \nAssessment"]
TSFCs = [model_assessment[3][4], direct_assessment[3][3], thermo_assessment[3][6]]
spec_Ts = [model_assessment[3][3], direct_assessment[3][2], thermo_assessment[3][5]]

# Creating the figure and subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))  # 1 row, 2 columns

# First bar graph on the first axis
ax1.bar(bar_label, TSFCs, color='b', label='TSFC')
ax1.set_title(f'TSFC Comparison at Max RPM of {RPM[-1]}')
ax1.set_xlabel('Model Comparison')
ax1.set_ylabel(f'TSFC [lbm/hr / kg]')
ax1.legend()

# Second bar graph on the second axis
ax2.bar(bar_label, spec_Ts, color='r', label='$F\'/ma$')
ax2.set_title(f'Specific Thrust Comparison at Max RPM of {RPM[-1]}')
ax2.set_xlabel('Model Comparison')
ax2.set_ylabel(f'Specific Thrust $F\'/ma$ [-]')
ax2.legend()

# Adjust layout to prevent overlap
fig.tight_layout()

plt.show()