# estParam.py - functions to estimate hull parameters from principal characteristics
# based on Grubisic 2012

import math

# ---------
def displacement(Cb, T, L, B) : # inputs in unitless, meters, meters, meters
    # constants
    rho = 1026 #kg/m^3
    g = 9.81 #m/s^2

    # calculate displacement
    nabla = Cb*T*L*B # volume displacement from hull parameters
    Disp = nabla*rho*(1/1000) # metric tonnes

    # Estimation of wetted surface area


    return Disp

# ---------
def wettedSurf(Cb, T, L, B) : # inputs in unitless, meters, meters, meters
    # constants
    rho = 1026 #kg/m^3
    g = 9.81 #m/s^2

    # calculate displacement
    nabla = Cb*T*L*B # volume displacement from hull parameters

    # Estimation of wetted surface area
    C = 2.61 + (((B/T)*((B/T)-0.244))/81) # unitless
    S = C*math.sqrt(L*nabla) #m^2

    return S
