#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:56:22 2024

@author: osahon
"""

import math
import numpy as np
from sympy import symbols, Eq, solve
#from sympy.abc import *
W1, C1, C_theta1, C_theta2, Ws_turb = symbols('W1 C1 C_theta1 C_theta2 Ws_turb')

# Equations
a1 = np.deg2rad(35.26)
b1 = np.deg2rad(19)
Omega = 160000 * (2*np.pi)/60 # Convert from RPM to rad/s
print(Omega)
r1 = 0.0393760598
OmegaR1 = Omega*r1
eq1 = Eq(W1*np.sin(b1) + OmegaR1, C1*np.sin(a1))
eq2 = Eq(W1*np.cos(b1), C1*np.cos(a1))
eq3 = Eq(C_theta1, C1*np.sin(a1))
eq4 = Eq(C_theta2, 0)
eq5 = Eq(Ws_turb, OmegaR1*C1*np.sin(a1))

solution = solve((eq1, eq2, eq3, eq4, eq5), (W1, C1, C_theta1, C_theta2, Ws_turb))

def W_Turb(): 
    return solution[Ws_turb]

# Print the solution
print(solution)
