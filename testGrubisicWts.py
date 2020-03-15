# testGrubisicWeights.py - a testing script to develop a weight estimation program based on Grubisic and Begovic, 2009
# NOTES:
# - Approximating L_p = L_wl = L_oa

import math

def grubisicWts(Disp, D, T, L, B, MCR, Vk) : # inputs in metric tonnes, meters, meters, meters, meters, kilowatts, knots
    rho = 1026.0 #kg/m^3
    g = 9.81 #m/s^2

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
    CTD = 1.144*math.pow((T/D),0.244)

    # structural numeral
    Es = fdis*CTD*SR # meters^2

    # service type and weight constant
    Gf = 1.20 #for patrol craft
    Sf = 1.25 #for unrestricted service
    K = 0.002 + (0.0064*Gf*Sf) # weight constant for aluminium hull

    # structural weights
    W100 = K*math.pow(Es,1.33) # metric tonnes
    print("W100: ",round(W100,3)," MT ")

    # machinery weights
    W250 = MCR/286 # metric tonnes, propulsion engine weight
    Wmach = math.pow(L*B*D,0.94)/45.66 # metric tonnes, remaining machinery`
    Wspp = math.pow(MCR,1.271)/8375 # metric tonnes, approximate weight of controllable pitch propeller
    W200 = Wmach+W250+Wspp # metric tonnes
    print("W200: ",round(W200,3)," MT ")

    # fuel weights
    SFC = 0.000196 # t/KWhr
    endur = 4500 # nautical miles
    Wfuel = SFC*MCR*(endur/Vk)*1.05 # tonnes, NA470 Coursepack Page 143
    print("Wfuel: ",round(Wfuel)," MT ")

    # electrical, auxilary machinery, outfit weights
    # NOTE - THESE ARE THE MOST VARIABLE
    W300 = math.pow(L*B*D,1.24)/592 # metric tonnes, electrical machinery weights
    print("W300: ",round(W300,3)," MT ")
    W400 = math.pow(L,2.254)/1887 # metric tonnes, electronic equipment weights
    print("W400: ",round(W400,3)," MT ")
    W500 = math.pow(L*B,1.784)/1295 # metric tonnes, auxilary machinery weights
    print("W500: ",round(W500,3)," MT ")
    W600 = math.pow(L,2.132)/102.5 # metric tonnes, outfit weights
    print("W600: ",round(W600,3)," MT ")

    # special systems weights
    W700 = math.pow(L*B*D,1.422)/3000 # metric tonnes, special systems weights
    print("W700: ",round(W700,3)," MT ")

    # cargo weights
    massContainer = 30000 # kg, from Wikipedia for shipping containers
    massCargo = 2*massContainer # must carry two containers
    Wcargo = massCargo/1000 # metric tonnes
    print("Wcargo: ",round(Wcargo,3)," MT ")

    #calulate and return R
    W = W100 + W200 + Wfuel + W300 + W400 + W500 + W600 + W700 + Wcargo # metric tonnes
    W = W*1.05 # metric tonnes, 5% margin
    print("W: ",round(W,3)," MT ")
    #print("W: ",round(((W/1000)*0.10036),3)," long ton ")
    return W

Wt = grubisicWts(.4,3,1.5,40,6,500,16) # inputs in unitless, meters, meters, meters, meters, kilowatts, knots
