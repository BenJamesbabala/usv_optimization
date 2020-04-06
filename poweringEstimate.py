# poweringEstimate.py - function to estimate brake powering required based on series64 resistance

import math
from resistanceCurves import series64

# Series 64 resistance taken from Ship Resistance and Propulsion by Molland
# Powering estimate based on Parsons' NA470 Coursepack
def poweringEstimate(L, S, Disp, Cb, Vk) : #inputs in meters, meters^2, metric tonnes, unitless, knots
    # constants
    rho = 1026.0 #kg/m^3
    g = 9.81 #m/s^2

    # conversions
    v = Vk/(1.944) #m/s

    # resistance
    R = series64(L, S, Disp, Cb, Vk) #N

    # effective power
    PE = (R*v)/1000 #kW

    # delivered power
    eta_H = 1.2 #hull efficiency
    eta_RR = 0.97 #propeller rotative efficiency
    eta_O = 0.55 #propeller open water efficiency
    PD = PE/(eta_H*eta_RR*eta_O)

    # brake power
    eta_SBG = 0.98 #stern tube, bearing, gear efficiency - taken assuming machinery aft
    PB = (PD/eta_SBG)*(0.85) #kW, brake power assuming 85% MCR

    return PB

# P1 = poweringEstimate(40,400,250,.45,16)
# print(P1)
#
# P2 = poweringEstimate(40,400,250,.45,27)
# print(P2)
