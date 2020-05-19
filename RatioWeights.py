import math
import numpy as np
from Weights import Weights
from weightCurves import parsonsWts, grubisicWts, grubisicWtsNoFuel #modify this if using a different weight estimation

#Cb = 0.4
#T_to_L = .15
#L_to_B = 4
#B_to_T = 2


def RatioWeights(L_to_B, B_to_T, T_to_L, Cb) : #inputs in meters, meters^2, metric tonnes, unitless, knots
    #constants
    rho = 1.0260 #kg/m^3
    MCR = 500
    Vk = 16
    lower_length = 19
    upper_length = 51

    # create a binary value to handle errors
    inBound = 0

    #g = 9.81 #m/s^2

    #Iterate through all Lengths, solves for displacement and weight
    for L in np.arange(lower_length,upper_length,0.1): #use np.arange to give decimal range steps
        T = T_to_L*L
        B = B_to_T*T
        Wt = grubisicWts(Cb, T, L, B, MCR, Vk)
        Displ = (L*B*T*Cb*rho)
        if (Wt*0.9 < Displ and Displ < Wt*1.1):
            # debugging text --
            # print("--Matched!!--")
            # print("Wt: ",Wt)
            # print("Displ: ",Displ)
            # end debugging --
            inBound = 1
            break
        else:
            # debugging text --
            # print("--Failed! At L = ",L," m --")
            # print("Wt: ",Wt)
            # print("Displ: ",Displ)
            # end debugging --
            #not strictly needed, but helps track the flow of code
            inBound = 0

    return L,B,T,inBound # "can only concatenate str (not "tuple") to str" error when running Ratios.py

# debugging text --
# print("~Design 1~")
# (L,B,T,Cb) = RatioWeights(4, 2, 0.15,0.4)
# print("--Final Dimensions--")
# print("L: ", L)
# print("B: ", B)
# print("T: ", T)
# print("Cb: ", Cb)
#
# print("~Design 2~")
# (L,B,T,Cb) = RatioWeights(4.2, 2.1, 0.153,0.4)
# print("--Final Dimensions--")
# print("L: ", L)
# print("B: ", B)
# print("T: ", T)
# print("Cb: ", Cb)
