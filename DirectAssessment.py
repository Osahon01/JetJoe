# DIRECT ASSESSMENT BASED ON MEASUREMENTS
import numpy as np

# Constants
R = 287
gamma_C = 1.4
rho_fuel = 6.843 # [lbm/gal] Density of fuel (known)
A_duct = 0.00225806 # [m^2] (3.5in^2 converted to m^2)

class DirectAssessment:

    def __init__(self, P0, T0, F, A1, P1_dynamic, V):
        # Measured Parameters
        self.P0 = P0 # [Pa] Cell Static Pressure
        self.T0 = T0 # [K] Inlet Temperature
        self.F = F # [N] Thrust
        self.A1 = A1 # Inlet Area [m^2]
        self.P1_dynamic = P1_dynamic # [Pa] Inlet Duct Wall Dynamic Pressure
        self.V = V # [gal/hour] Fuel Flow

        # Calculate derived parameters from knowns
        self.P1 = self.P0 - self.P1_dynamic # [Pa] Inlet Static Pressure
        self.mf_imperial = rho_fuel*V # [lbm/hr]
        self.F_imperial = F/4.4482 # [lbf]
        self.mf = self.mf_imperial * 0.4536/3600 # [kg/s]

    def get_est_parameters(self):
        # Estimated Parameters (Values we calculate)
        self.M1 = (2/(gamma_C-1)*((self.P0/self.P1)**((gamma_C-1)/gamma_C)-1))**0.5
        self.m1 = self.A1*self.P0/(self.T0)**0.5 * (gamma_C/R)**0.5 * self.M1/((1 + (gamma_C-1)/2 * self.M1**2)**((gamma_C+1)/2*(gamma_C-1)))
        self.spec_T = self.F/(self.m1*(gamma_C*R*self.T0)**0.5)
        self.TSFC_imperial = self.mf_imperial/self.F_imperial
        print(f'\nDirect Assessment Estimated Parameters \nInlet Mach No. = {self.M1} [-] \nInlet Mass Flow = {self.m1} [kg/s] \nSpecific Thrust = {self.spec_T} [-] \nTSFC = {self.TSFC_imperial} [(lbm/hr)/lbf]')
        return np.array([self.M1, self.m1, self.spec_T, self.TSFC_imperial])

    def get_mf(self):
        return self.mf
    
    def get_m1(self):
        return self.m1
