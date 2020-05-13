# poweringEstimate.py - function to estimate brake powering required based on series64 resistance

import math
from poweringEstimate import poweringEstimate
from flywheelWeight import convertToE, fwWgt

# fuel estimation based on hypothetical mission profile
# define alternative missions with new functions

# Initial Mission Analysis
def missionFuel1(L, S, Disp, Cb) : #inputs in meters, meters^2, metric tonnes, unitless
    # constants
    rho = 1026.0 #kg/m^3
    g = 9.81 #m/s^2

    # define characteristics
    range = 4500 #naut. mile
    days = 60
    vCruise = 16 #knots
    vSprint = 27 #knots
    hoursTot = (days*24)
    hoursSprint = days
    hoursComm = (days*2)
    hoursCruise = (range/vCruise)
    hoursLoiter = hoursTot - (hoursSprint+hoursComm+hoursCruise)
    powSleep = 50 #kW
    powNorm = 300 #kW
    powMax = 500 #kW
    SFC = 0.000196 #t/kWhr

    # Calculate propulsion powering
    PBCruise = poweringEstimate(L, S, Disp, Cb, vCruise) #kW
    PBSprint = poweringEstimate(L, S, Disp, Cb, vSprint) #kW

    # calculate total powers
    PSprint = PBSprint + powNorm #kW
    PComm = PBCruise + powMax #kW
    PCruise = PBCruise + powNorm #kW
    PLoiter = powSleep #kW

    PMax = max(PSprint, PComm, PCruise, PLoiter) #kW

    # calculate fuel consumption
    fuelSprint = SFC*PSprint*hoursSprint #t
    fuelComm = SFC*PComm*hoursComm #t
    fuelCruise = SFC*PCruise*hoursCruise #t
    fuelLoiter = SFC*PLoiter*hoursLoiter #t

    fuelTot = fuelSprint + fuelComm + fuelCruise + fuelLoiter

    return fuelTot, PMax

# Initial Mission Analysis WITH FLYWHEELS
def missionFuel1FW(L, S, Disp, Cb, fwCap) : #inputs in meters, meters^2, metric tonnes, unitless, megajoules
    # constants
    rho = 1026.0 #kg/m^3
    g = 9.81 #m/s^2

    # define characteristics
    range = 4500 #naut. mile
    days = 60
    vCruise = 16 #knots
    vSprint = 27 #knots
    hoursTot = (days*24)
    hoursSprint = days
    hoursComm = (days*2)
    hoursCruise = (range/vCruise)
    hoursLoiter = hoursTot - (hoursSprint+hoursComm+hoursCruise)
    powSleep = 50 #kW
    powNorm = 300 #kW
    powMax = 500 #kW
    SFC = 0.000196 #t/kWhr

    # Calculate propulsion powering
    PBCruise = poweringEstimate(L, S, Disp, Cb, vCruise) #kW
    PBSprint = poweringEstimate(L, S, Disp, Cb, vSprint) #kW

    # calculate total powers
    PSprint = PBSprint + powNorm #kW
    PComm = PBCruise + powMax #kW
    PCruise = PBCruise + powNorm #kW
    PLoiter = powSleep #kW

    PMax = max(PSprint, PComm, PCruise, PLoiter) #kW

    # calculate flywheel charge/discharge times
    tChg = (fwCap*1000000)/((PCruise - PLoiter)*1000) #seconds
    tDischg = (fwCap*1000000)/(PLoiter*1000) #seconds
    etaRun = tChg/(tChg + tDischg) #unitless

    # calculate flywheel starts
    nStarts = (hoursLoiter*60*60)/(tChg + tDischg) # unitless

    # calculate fuel consumption
    fuelSprint = SFC*PSprint*hoursSprint #t
    fuelComm = SFC*PComm*hoursComm #t
    fuelCruise = SFC*PCruise*hoursCruise #t
    fuelLoiter = SFC*PLoiter*(hoursLoiter*etaRun) #t

    fuelTot = fuelSprint + fuelComm + fuelCruise + fuelLoiter + fwWgt(fwCap)

    return fuelTot, PMax, etaRun, nStarts
    #return fuelTot, PMax, PBCruise, PBSprint, etaRun, nStarts

# fuel, MCR, cru, spr, run, starts = missionFuel1FW(26.32,189.727,198.55,.342,300)
# print("Fuel Wt: ", round(fuel,4), " MT")
# print("Max MCR: ", round(MCR,4), " kW")
# print("Cruise MCR: ", round(cru,4), " kW")
# print("Sprint MCR: ", round(spr,4), " kW")
# print("Runtime: ", round(run*100,4), " %")
# print("Starts: ", round(starts,2), " -")
