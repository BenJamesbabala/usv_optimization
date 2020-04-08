# weightCurves.py - file to contain various weight estimations defined for use as functions

import math

# ---------
# Based on Parsons' NA470 Coursepack
def parsonsWts(Cb, D, T, L, B, MCR, Vk) : # inputs in unitless, meters, meters, meters, meters, kilowatts, knots
    rho = 1026.0 #kg/m^3
    g = 9.81 #m/s^2
    K = 0.044 # from NA470 Coursepack for Tugs
    E = 400 # from NA470 Coursepack for Tugs

    # structural weights
    CbPrime = Cb + ((1-Cb)*(((0.8*D) - T)/(3*T))) # unitless, NA470 Coursepack Page 141
    Ws = K*math.pow(E,1.36)*(1+(0.5*(CbPrime-0.7))) # tonnes, NA470 Coursepack Page 141
    #Ws = Ws/2.9 # tonnes, conversion to Aluminium construction
    Ws = Ws*g*1000 # newtons, conversion to newtons

    # machinery weights
    Wm = 0.72*math.pow(MCR,0.78) # tonnes, NA470 Coursepack Page 143
    Wm = Wm*g*1000 # newtons, conversion to newtons

    # fuel weights
    SFC = 0.000196 # t/KWhr
    endur = 4500 # nautical miles
    Wfuel = SFC*MCR*(endur/Vk)*1.05 # tonnes, NA470 Coursepack Page 143
    Wfuel = Wfuel*g*1000 # newtons, conversion to newtons

    # outfit weights
    Co = 0.4 # unitless, from Figure in NA470 Coursepack Page 144
    Wo = Co*L*B # tonnes, NA470 Coursepack Page 144
    Wo = Wo*g*1000 # newtons, conversion to newtons

    # cargo weights
    massContainer = 30000 # kg, from Wikipedia for shipping containers
    massCargo = 2*massContainer # must carry two containers
    Wcargo = g*massCargo # newtons

    #calulate and return R
    W = Ws + Wm + Wfuel + Wo + Wcargo # newtons
    W = W*1.05 # newtons, 5% margin
    W = W/(g*1000) # convert back to tonnes for standardization
    return W

# ---------
# Based on Grubisic and Begovic, 2009
# NOTES: Approximating L_p = L_wl = L_oa, ELIMINATING depth input, will approximate based on draft,
def grubisicWts(Cb, T, L, B, MCR, Vk) : # inputs in unitless, meters, meters, meters, kilowatts, knots
    rho = 1026.0 #kg/m^3
    g = 9.81 #m/s^2

    # Approximate displacment, per definition of block coefficient
    Disp = (rho/1000)*Cb*L*B*T #metric tonnes

    # Approximate depth based on draft, eqn from Grubisic 2012
    D = (2.493)*math.pow(T,0.582)

    # estimate surface areas
    S1 = 2.825*math.sqrt((Disp/rho)*L) #bottom
    S2 = 1.09*(2*(L+B))*(D-T) #sides
    S3 = 0.823*L*B #deck
    Nwtb = L/5 #Approximating number of watertight bulkheads
    S4 = 0.6*Nwtb*B*D #Bulkheads

    SR = S1 + (0.73*S2) + (0.69*S3) + (0.65*S4) #total reduced surface area

    # correction factors
    DispLR = 0.125*((L*L)-15.8) #tonnes
    nabla = (DispLR + Disp)/rho
    fdis = 0.7 + (2.4*(nabla/((L*L)-15.8)))
    CTD = 1.144*math.pow((T/(D+0.0001)),0.244) #modified to prevent a divide by zero

    # structural numeral
    Es = fdis*CTD*SR # meters^2

    # service type and weight constant
    Gf = 1.20 #for patrol craft
    Sf = 1.25 #for unrestricted service
    K = 0.002 + (0.0064*Gf*Sf) # weight constant for aluminium hull

    # structural weights
    W100 = K*math.pow(Es,1.33) # metric tonnes

    # machinery weights
    W250 = MCR/286 # metric tonnes, propulsion engine weight
    Wmach = math.pow(L*B*D,0.94)/45.66 # metric tonnes, remaining machinery`
    Wspp = math.pow(MCR,1.271)/8375 # metric tonnes, approximate weight of controllable pitch propeller
    W200 = Wmach+W250+Wspp # metric tonnes

    # fuel weights
    SFC = 0.000196 # t/KWhr
    endur = 4500 # nautical miles
    Wfuel = SFC*MCR*(endur/Vk)*1.05 # tonnes, NA470 Coursepack Page 143

    # electrical, auxilary machinery, outfit weights
    # NOTE - THESE ARE THE MOST VARIABLE
    W300 = math.pow(L*B*D,1.24)/592 # metric tonnes, electrical machinery weights
    W400 = math.pow(L,2.254)/1887 # metric tonnes, electronic equipment weights
    W500 = math.pow(L*B,1.784)/1295 # metric tonnes, auxilary machinery weights
    W600 = math.pow(L,2.132)/102.5 # metric tonnes, outfit weights

    # special systems weights
    W700 = math.pow(L*B*D,1.422)/3000 # metric tonnes, special systems weights

    # cargo weights
    massContainer = 30000 # kg, from Wikipedia for shipping containers
    massCargo = 2*massContainer # must carry two containers
    Wcargo = massCargo/1000 # metric tonnes

    #calulate and return R
    W = W100 + W200 + Wfuel + W300 + W400 + W500 + W600 + W700 + Wcargo # metric tonnes
    W = W*1.05 # metric tonnes, 5% margin
    return W

# ---------
# Based on Grubisic and Begovic, 2009
# assumes no fuel weight
# NOTES: Approximating L_p = L_wl = L_oa, ELIMINATING depth input, will approximate based on draft,
def grubisicWtsNoFuel(Cb, T, L, B, MCR, fuel) : # inputs in unitless, meters, meters, meters, kilowatts, metric tonnes
    rho = 1026.0 #kg/m^3
    g = 9.81 #m/s^2

    # Approximate displacment, per definition of block coefficient
    Disp = (rho/1000)*Cb*L*B*T #metric tonnes

    # Approximate depth based on draft, eqn from Grubisic 2012
    D = (2.493)*math.pow(T,0.582)

    # estimate surface areas
    S1 = 2.825*math.sqrt((Disp/rho)*L) #bottom
    S2 = 1.09*(2*(L+B))*(D-T) #sides
    S3 = 0.823*L*B #deck
    Nwtb = L/5 #Approximating number of watertight bulkheads
    S4 = 0.6*Nwtb*B*D #Bulkheads

    SR = S1 + (0.73*S2) + (0.69*S3) + (0.65*S4) #total reduced surface area

    # correction factors
    DispLR = 0.125*((L*L)-15.8) #tonnes
    nabla = (DispLR + Disp)/rho
    fdis = 0.7 + (2.4*(nabla/((L*L)-15.8)))
    CTD = 1.144*math.pow((T/(D+0.0001)),0.244) #modified to prevent a divide by zero

    # structural numeral
    Es = fdis*CTD*SR # meters^2

    # service type and weight constant
    Gf = 1.20 #for patrol craft
    Sf = 1.25 #for unrestricted service
    K = 0.002 + (0.0064*Gf*Sf) # weight constant for aluminium hull

    # structural weights
    W100 = K*math.pow(Es,1.33) # metric tonnes

    # machinery weights
    W250 = MCR/286 # metric tonnes, propulsion engine weight
    Wmach = math.pow(L*B*D,0.94)/45.66 # metric tonnes, remaining machinery`
    Wspp = math.pow(MCR,1.271)/8375 # metric tonnes, approximate weight of controllable pitch propeller
    W200 = Wmach+W250+Wspp # metric tonnes
    Wfuel = fuel # FUEL WEIGHT IS AN INPUT

    # electrical, auxilary machinery, outfit weights
    # NOTE - THESE ARE THE MOST VARIABLE
    W300 = math.pow(L*B*D,1.24)/592 # metric tonnes, electrical machinery weights
    W400 = math.pow(L,2.254)/1887 # metric tonnes, electronic equipment weights
    W500 = math.pow(L*B,1.784)/1295 # metric tonnes, auxilary machinery weights
    W600 = math.pow(L,2.132)/102.5 # metric tonnes, outfit weights

    # special systems weights
    W700 = math.pow(L*B*D,1.422)/3000 # metric tonnes, special systems weights

    # cargo weights
    massContainer = 30000 # kg, from Wikipedia for shipping containers
    massCargo = 2*massContainer # must carry two containers
    Wcargo = massCargo/1000 # metric tonnes

    #calulate and return R
    W = W100 + W200 + Wfuel + W300 + W400 + W500 + W600 + W700 + Wcargo # metric tonnes
    W = W*1.05 # metric tonnes, 5% margin
    return W
