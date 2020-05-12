# flywheelWeight.py - file to contain various flywheel energy storage device weight estimations defined for use as functions

import math
import statistics

# ---------
# helper funciton to turn power and time to megajoules
def convertToE(P,t) : # inputs in kilowatts, hours
    P_watts = P*1000 # power in watts
    t_sec = t*60*60 # time in seconds
    E_joules = P_watts*t_sec # energy in joules
    E = E_joules/(1000000) #energy in megajoules

    return E

# ---------
# average from industrially available FESDs
def fwWgt(E) : # inputs in megajoules
    # Amber kinetics, 115.2 MJ, 4536 kg
    m1 = (115.2/4536) #MJ/kg

    # Active Power, 66 MJ, 5103 kg
    m2 = (66/5103) #MJ/kg

    # UT-Austin ALPS, 360 MJ, 8600 kg
    m3 = (360/8600) #MJ/kg

    m = statistics.mean([m1,m2,m3])
    W = (E/m)/1000 # metric tonnes

    return W

# print("100 kW, 2 hours: ", round(convertToE(100,2),3), " MJ")
# print("1500 kW, 0.1 hours: ", round(convertToE(1500,0.1),3), " MJ")
#
#
# print("100 MJ: ", round(fwWgt(100),3), " MT")
# print("360 MJ: ", round(fwWgt(360),3), " MT")
# print("1000 MJ: ", round(fwWgt(1000),3), " MT")
