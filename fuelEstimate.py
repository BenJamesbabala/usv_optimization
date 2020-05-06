# poweringEstimate.py - function to estimate brake powering required based on series64 resistance

import math
from poweringEstimate import poweringEstimate

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
def missionFuel1FW(L, S, Disp, Cb) : #inputs in meters, meters^2, metric tonnes, unitless
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

    return fuelTot, PMax, PBCruise, PBSprint

# fuel, MCR, cru, spr = missionFuel1FW(26.32,189.727,198.55,.342)
# print(fuel)
# print(MCR)
# print(cru)
# print(spr)
