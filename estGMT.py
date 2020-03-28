# estGMT.py - function to perform a rudimentary check up upright stability.  Returns transverse metacentric height
# relies on a series of coefficient calculations

import math

# ---------
# Based on Parsons' NA470 Coursepack
def estGMT(Cb, T, L, B) : # inputs in unitless, meters, meters, meters
    # constants/conversions
    Disp = Cb*T*L*B # displacement from hull parameters

    # Estimation of KB
    # - Based on Grubisic and Begovic 2012, originally based on Begovic 1998?
    Cp = 0.384 + (0.565*Cb) #unitless
    Cwp = 0.467 + (0.47*Cp) #unitless

    KB = (0.961)*T*(1.048-(Cb/(Cb + Cwp))) # modified Papmel's formula

    # Estimation of BM
    # - Based on definition of BM and estimation of waterplane moment of inertia
    CI = (1.04*Cwp*Cwp)/12 # Based on McCloghrie’s formula assuming a roughly triangular waterplane

    IT = CI*L*B*B*B # estimation of waterplane moment of inertia

    BM = IT/Disp # exact calculation of metacentric radius

    # Estimation of KG
    # NEED A SOURCE FOR THIS ESTIMATE
    a = 0.8
    KG = a*T # VERY rough estimation

    GM = KB + BM - KG

    return GM
