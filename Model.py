from Part1 import W_Turb
import numpy as np

# OUR MODEL 

# Constants
R = 287
cpC = 1004.5
cpT = 1243.67
hf = 42 * 10**6 # [J/kg]  (Internal enthalpy of Kerosine found online)
gamma_C = 1.4
gamma_T = 1.3
T0 = 300 # [K] Ambient Temperature
P0 = 101325 #101325 # [Pa] Atmospheric pressure at sea level
Pt0 = P0 # c_0 = 0 (atmosphere is initially at rest wrt inlet)
Tt2 = T0
Pt2 = Pt0 # Stagnation pressure conserved along streamline up to the compressor
Tt5 = 953.15 # 680 + 273.15

# Measured Parameters
a1 = 35.26 # [deg] Rotor angle 1
b1 = 19 # [deg] Rotor angle 2
A_NGV = 0.000698744409 # [m^2] measured

class Model:

    def __init__(self, RPM, a1, b1, A_NGV):
        self.RPM = RPM
        self.a1 = a1
        self.b1 = b1
        self.A_NGV = A_NGV

        # Step 1 - Calculate Specific Shaft Work
        print("\nStep 1")

        # Known variables
        self.a1 = np.deg2rad(self.a1)
        self.b1 = -np.deg2rad(self.b1)
        self.omega = self.RPM * (2*np.pi)/60 # Convert from RPM to rad/s
        self.r1 = 0.02293760598 # [m]
        self.w_T = (self.omega* self.r1)**2 * 1/(1 - np.tan(self.b1)/np.tan(self.a1))
        print(f'w_T = {self.w_T} [J/kg]')

        # Step 2
        print("\nStep 2")
        eta_C = 0.63 # WE SET THIS
        eta_T = 0.70 # WE SET THIS
        print("We chose eta_C = 0.63, eta_T = 0.7")

        # Step 3
        print("\nStep 3")

        # Calculate fuel fraction, combustor inlet temp.
        self.f = (-1*(cpT*Tt5+hf)+np.sqrt((cpT*Tt5+hf)**2 - 4*hf*(Tt2*cpC-cpT*Tt5)))/(2*hf)
        self.Tt3 = (1+self.f)*(self.w_T/cpC) + Tt2
        print(f'f = {self.f}')
        print(f'Tt3  = {self.Tt3} K')

        # Calculating Compressor pressure ratio
        self.comp_ratio = (eta_C*(self.Tt3/Tt2 - 1) + 1)**(gamma_C/(gamma_C-1))
        print(f'Compression Ratio =  {self.comp_ratio}  assuming eta_C = {eta_C}')

        # Step 4
        print("\nStep 4")

        # Calculate Turbine Inlet temp.
        self.Tt4 = (cpC*(self.Tt3-Tt2))/((1+self.f)*cpT) + Tt5
        print(f'Tt4 Analytical = {self.Tt4} K')

        # Step 5
        print("\nStep 5")

        self.Pt3 = self.comp_ratio * P0 # Centrifugal Compression occurs
        self.Pt4 = self.Pt3 # Stagnation pressure conserved across the combustor

        # Pressure after turbine as a function of thermal efficiency
        self.Pt5 = self.Pt4*((Tt5/self.Tt4 - 1)/eta_T + 1)**(gamma_T/(gamma_T-1))
        # self.Pt5 = self.Pt4*((Tt5/self.Tt4))**(gamma_T/(gamma_T-1)) # If eta_T = 1
        self.P6 = 101325
        self.Tt6 = Tt5
        self.Pt6 = self.Pt5
        self.M6 = ((2/(gamma_T - 1))*((self.Pt6/self.P6)**((gamma_T - 1) / gamma_T) -1))**0.5
        self.T_exit = self.Tt6/(1+(gamma_T-1)/2 * self.M6**2)
        print(f'self.T_exit = {self.T_exit} K')
        self.a6 = (gamma_T * R * self.T_exit)**0.5
        self.c6 = self.M6*self.a6
        # Tt5_s = Tt5 + (cpC*(self.Tt3-T0))/(cpT*(f+1))*(1-1/eta_T)
        # self.c6 = (2*cpT*Tt5*(1-(self.Tt4/Tt5_s)*((P0/self.Pt3)**((gamma_T - 1)/gamma_T))))**0.5
        print(f'c6 = {self.c6} and M6 = {self.M6} and a6 = {self.a6}')

        # Solve for mass flow after the turbine (but its the same everywhere)
        self.M4 = 1 # for choked NGV
        self.DM4 = self.M4/(1 + ((gamma_T-1)/2)*self.M4**2)**(1/2 * (gamma_T+1)/(gamma_T-1)) # corrected mass flow per unit area
        self.m4 = (self.DM4 * A_NGV * self.Pt4 * (gamma_T)**(1/2))/(R*self.Tt4)**(1/2)
        print(f'NGV mass flow = {self.m4} [kg/s]')

        # Step 6
        print("\nStep 6")
        self.KE = (0.5*self.m4*self.c6**2)
        print(f'KE_dot = {self.KE} [W = J/s]')

        # Step 7
        print("\nStep 7")
        cfact = (3600*4.4448*(1/0.4536)) # (kg/s)/N to (lbm/hr)/lbf
        self.TSFC = (self.f / (self.c6*(self.f+1)))
        self.TSFC_imperial = self.TSFC*cfact
        self.T_spec = (self.f+1)*(self.c6 / ((gamma_C*287*T0)**0.5))
        print(f'TSFC = {self.TSFC} ; Specific Thrust = {self.T_spec}')
        print(f'TSFC Imperial = {self.TSFC_imperial}')

        # Calculating Inlet Mass Flow
        self.m1 = self.m4/(1 + self.f) # Mass flow after combustor scaled down by amount of fuel added
        print(f'Mass flow at inlet = {self.m1} [kg/s]')

        # SANITY CHECK
        print("\nCheck if our model is reasonable")
        self.T = self.m4*self.c6
        print(f'Thrust = {self.T} [N], Thrust Imperial: {self.T / 4.4482} [lbf]')
        cfact2 = (1/4.4482) * (1/60) * 16 # (lbf/N) * (min/hr)^-1 * oz/lbm
        self.fuel_cons = self.T * self.TSFC_imperial * cfact2
        print(f'Fuel consumption = {self.fuel_cons} [oz/min]')

    def performance_bid(self):
        return np.array([self.comp_ratio, self.m1, self.Tt4, self.T_spec, self.TSFC_imperial])

