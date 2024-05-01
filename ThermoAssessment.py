# THERMODYNAMIC ASSESSMENT BASED ON MEASUREMENTS
import numpy as np

# Constants
R = 287
gamma_C = 1.4
gamma_T = 1.3
cpC = 1004.5
cpT = 1243.67
rho_fuel = 6.843 # [lbm/gal] Density of fuel (known)

class ThermoAssessment:
    
    def __init__(self, P0, T0, Pt3, Tt3, Tt5, mf, m1, delta_eta):
    # Measured Parameters
        self.P0 = P0 # [Pa] Cell Static Pressure
        self.T0 = T0 # [K] Inlet Temperature
        self.Pt3 = Pt3 # [Pa] Compressor Discharge Pressure
        self.Tt3 = Tt3 # [K] Compressor Discharge Temperature
        self.Tt5 = Tt5 # [K] EGT (Exhaust Gas Temperature)
        # self.V = V # [gal/hour] Fuel Flow
        # self.F = F # [N] Thrust
        # self.A1 = A1
        self.mf = mf
        self.m1 = m1
        self.delta_eta = delta_eta

        # Calculate derived parameters from knowns
        # self.mf_imperial = rho_fuel*V # [lbm/hr]
        # self.F_imperial = F/4.4482 # [lbf]
        # self.mf = self.mf_imperial * 0.4536/3600 # [kg/s]

    def get_est_parameters(self):
        # Estimated Parameters
        self.f = self.mf/(self.mf + self.m1) # [-] Fuel flow fraction 
        self.eta_C = ((self.Pt3/self.P0)**((gamma_C-1)/gamma_C) - 1)/(self.Tt3/self.T0 - 1) # [-] Ad. Compressor Efficiency
        self.Tt4 = self.Tt5 + cpC/cpT * (self.Tt3-self.T0)/(self.f + 1) # [K] Turbine Inlet Temperature
        self.Tt5s = self.Tt5 + cpC/cpT * (self.Tt3-self.T0)/(self.f + 1) * (1 - 1/(self.eta_C + self.delta_eta)) # [K] Isentropic Turbine Exit Temp
        self.c6 = (2*cpT*self.Tt5*(1-self.Tt4/self.Tt5s*(self.P0/self.Pt3)**((gamma_T-1)/gamma_T)))**0.5 # [m/s] Jet Velocity
        self.spec_T = (self.f+1) * self.c6/(gamma_C*R*self.T0)**0.5 # [-] Specific Thrust
        self.TSFC = self.f/(self.c6*(self.f+1)) # [kg/s / N] TSFC
        self.TSFC_imperial = self.TSFC * 3600*4.4448*(1/0.4536) # [(lbm/hr)/lbf] Imperial Specific Thrust
        print(f'\nThermo Analysis Estimated Parameters \nFuel Flow Fraction = {self.f} [-] \nAd. Compressor Efficiency = {self.eta_C} [-] \nTurbine Inlet Temp = {self.Tt4} [K] \nIsentropic Turbine Exit Temp = {self.Tt5s} [K] \nJet Velocity = {self.c6} [m/s] \nSpecific Thrust = {self.spec_T} [-] \nTSFC = {self.TSFC_imperial} [(lbm/hr)/lbf]')
        return np.array([self.f, self.eta_C, self.Tt4, self.Tt5s, self.c6, self.spec_T, self.TSFC_imperial])
        