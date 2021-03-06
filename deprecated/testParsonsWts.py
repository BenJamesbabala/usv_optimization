# testParsonsWts.py - a testing script to develop a weight estimation program

import math

def parsonsWts(Cb, D, T, L, B, MCR, Vk) : # inputs in unitless, meters, meters, meters, meters, kilowatts, knots
    rho = 1026.0 #kg/m^3
    g = 9.81 #m/s^2
    K = 0.044 # from NA470 Coursepack for Tugs
    E = 400 # from NA470 Coursepack for Tugs

    # structural weights
    CbPrime = Cb + ((1-Cb)*(((0.8*D) - T)/(3*T))) # unitless, NA470 Coursepack Page 141
    print("Cb': ",round(CbPrime,4)," - ")
    Ws = K*math.pow(E,1.36)*(1+(0.5*(CbPrime-0.7))) # tonnes, NA470 Coursepack Page 141
    #Ws = Ws/2.9 # tonnes, conversion to Aluminium construction
    Ws = Ws*g*1000 # newtons, conversion to newtons
    print("Ws: ",round((Ws/1000),3)," kN ")

    # machinery weights
    Wm = 0.72*math.pow(MCR,0.78) # tonnes, NA470 Coursepack Page 143
    Wm = Wm*g*1000 # newtons, conversion to newtons
    print("Wm: ",round((Wm/1000),3)," kN ")

    # fuel weights
    SFC = 0.000196 # t/KWhr
    endur = 4500 # nautical miles
    Wfuel = SFC*MCR*(endur/Vk)*1.05 # tonnes, NA470 Coursepack Page 143
    Wfuel = Wfuel*g*1000 # newtons, conversion to newtons
    print("Wfuel: ",round((Wfuel/1000),3)," kN ")

    # outfit weights
    Co = 0.4 # unitless, from Figure in NA470 Coursepack Page 144
    Wo = Co*L*B # tonnes, NA470 Coursepack Page 144
    Wo = Wo*g*1000 # newtons, conversion to newtons
    print("Wo: ",round((Wo/1000),3)," kN ")

    # cargo weights
    massContainer = 30000 # kg, from Wikipedia for shipping containers
    massCargo = 2*massContainer # must carry two containers
    Wcargo = g*massCargo # newtons
    print("Wcargo: ",round((Wcargo/1000),3)," kN ")

    #calulate and return R
    W = Ws + Wm + Wfuel + Wo + Wcargo # newtons
    W = W*1.05 # newtons, 5% margin
    print("W: ",round((W/1000),3)," kN ")
    print("W: ",round(((W/1000)*0.10036),3)," long ton ")
    return W

Wt = parsonsWts(.4,3,1.5,40,6,500,16) # inputs in unitless, meters, meters, meters, meters, kilowatts, knots
