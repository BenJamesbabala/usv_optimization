# musvDOEv3casePlotter.py - from
# Reads musvDOEv3cases.csv and plots

import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from poweringEstimate import poweringEstimate
from estParam import wettedSurf

# setup write to CSV with outputs
with open('musvDOEv3cases.csv', newline='') as csv_file:
    # read csv file
    reader = csv.reader(csv_file, quoting=csv.QUOTE_NONNUMERIC)

    # skip header row
    next(reader)

    # set up lists for data
    Cb = [] # index = 0
    L = [] # index = 1
    B = [] # index = 2
    T = [] # index = 3
    fwCap = [] # index = 4
    GMT = [] # index = 5
    Wt = [] # index = 6
    Disp = [] # index = 7
    Excess = [] # index = 8
    MCR = [] # index = 9
    fuelWt = [] # index = 10
    etaRun = [] # index = 11
    nStarts = [] # index = 12
    percentFuel = []
    PBcru = []
    PBspr = []
    PBratio = []

    # iterate through all designs
    for row in reader:
        # require positive GMT
        if row[5] > 0:
            # require weight/displacement within 10%
            if abs(row[8]) < (0.1*row[6]):
                # require sprint power within twice cruise power
                PBcruise = poweringEstimate(row[1], wettedSurf(row[0], row[3], row[1], row[2]), row[7], row[0], 16) #kW
                PBsprint = poweringEstimate(row[1], wettedSurf(row[0], row[3], row[1], row[2]), row[7], row[0], 27) #kW
                if (PBsprint/PBcruise) < 2:
                    #read data into lists
                    Cb.append(row[0])
                    L.append(row[1])
                    B.append(row[2])
                    T.append(row[3])
                    fwCap.append(row[4])
                    GMT.append(row[5])
                    Wt.append(row[6])
                    Disp.append(row[7])
                    Excess.append(row[8])
                    MCR.append(row[9])
                    fuelWt.append(row[10])
                    etaRun.append((row[11]*100)) #convert to percentage
                    nStarts.append(row[12])
                    percentFuel.append(row[10]/row[5])
                    PBcru.append(PBcruise)
                    PBspr.append(PBspr)
                    PBratio.append(PBsprint/PBcruise)

#---- SOME PLOTS
# test of 3D plotting
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(L, MCR, fwCap)
#
# ax.set_xlabel('Length [m]')
# ax.set_ylabel('MCR [kW]')
# ax.set_zlabel('Flywheel Size [MJ]')
#
# plt.show()

# # Save and close figure
# plt.savefig('Wt_Disp.png')
# plt.clf()


#-----
# # plot MCR and engine runtime
# plt.plot(MCR, etaRun, color='blue', marker='o', linewidth=0, markersize=2, label='Designs')
# plt.axhline(y=0.5, color='green', linewidth=1, linestyle='dashed', label='0.5%')
# plt.axhline(y=1, color='orange', linewidth=1, linestyle='dashed', label='1%')
# plt.axhline(y=2, color='red', linewidth=1, linestyle='dashed', label='2%')
#
# # Create legend, labels
# plt.legend(loc='upper left')
# #plt.xscale("log")
# plt.xlim(0, 10000)
# plt.ylim(0, 3)
# plt.xlabel('MCR [kW]')
# plt.ylabel('Loitering Engine Runtime [%]')
#
# # Save and close figure
# plt.show()
# # plt.savefig('Wt_Disp.png')
# # plt.clf()

#-----
# plot MCR and engine starts
plt.plot(MCR, nStarts, color='blue', marker='o', linewidth=0, markersize=2, label='Designs')
#plt.axhline(y=0.5, color='green', linewidth=1, linestyle='dashed', label='0.5%')
#plt.axhline(y=1, color='orange', linewidth=1, linestyle='dashed', label='1%')
#plt.axhline(y=2, color='red', linewidth=1, linestyle='dashed', label='2%')

# Create legend, labels
plt.legend(loc='upper left')
#plt.yscale("log")
plt.xlim(0, 10000)
#plt.ylim(0, 3)
plt.xlabel('MCR [kW]')
plt.ylabel('Loitering Engine Starts [-]')

# Save and close figure
plt.show()
# plt.savefig('Wt_Disp.png')
# plt.clf()

#-----
# # plot weight and displacement
# plt.plot(Wt, Disp, color='blue', marker='o', linewidth=0, markersize=2, label='Designs')
# plt.plot(Wt, Wt, label='Equal', color='red', linewidth=2)
#
# # Create legend, labels
# plt.legend(loc='upper left')
# plt.xlim(100, 600)
# plt.ylim(100, 600)
# plt.xlabel('Weight [MT]')
# plt.ylabel('Displacement [MT]')
#
# # Save and close figure
# plt.savefig('Wt_Disp.png')
# plt.clf()
#
# #-----
# # plot length and "excess" displacement
# plt.plot(L, Excess, color='blue', marker='o', linewidth=0, markersize=2, label='Designs')
# plt.axhline(y=0, color='red', linewidth=2)
# plt.axhline(y=-50, color='red', linewidth=1, linestyle='dashed')
# plt.axhline(y=50, color='red', linewidth=1, linestyle='dashed')
#
#
# # Create legend, labels
# plt.legend(loc='upper left')
# plt.xlim(20, 55)
# plt.ylim(-100, 300)
# plt.xlabel('Length [m]')
# plt.ylabel('Excess Displacement [MT]')
#
# # Save and close figure
# plt.savefig('L_Excess.png')
# plt.clf()
#
# #-----
# # plot displacement and stability
# plt.plot(Disp, GMT, color='blue', marker='o', linewidth=0, markersize=2, label='Designs')
# plt.axhline(y=0, color='red', linewidth=2)
# plt.axhline(y=.50, color='red', linewidth=1, linestyle='dashed')
#
#
# # Create legend, labels
# plt.legend(loc='upper left')
# plt.xlim(0, 600)
# plt.ylim(-1, 3)
# plt.xlabel('Displacement [MT]')
# plt.ylabel('GMT [m]')
#
# # Save and close figure
# plt.savefig('disp_gmt.png')
# plt.clf()
#
# #----
# # plot fuel weight and MCR
# plt.plot(MCR, percentFuel, color='blue', marker='o', linewidth=0, markersize=2, label='Designs')
# plt.axhline(y=.1, color='green', linewidth=1, linestyle='dashed', label='10%')
# plt.axhline(y=.3, color='orange', linewidth=1, linestyle='dashed', label='30%')
# plt.axhline(y=.5, color='red', linewidth=1, linestyle='dashed', label='50%')
#
#
# # Create legend, labels
# plt.legend(loc='upper left')
# plt.xlim(0, 2000)
# plt.ylim(0, 0.8)
# plt.xlabel('MCR [kW]')
# plt.ylabel('Percent of Weight that is Fuel [-]')
#
# # Save and close figure
# plt.savefig('fuel_mcr.png')
# plt.clf()
#
# #----
# # plot displacement and power ratio
# plt.plot(Disp, PBratio, color='blue', marker='o', linewidth=0, markersize=2, label='Designs')
# plt.axhline(y=1, color='green', linewidth=1, linestyle='dashed', label='10%')
# plt.axhline(y=3, color='orange', linewidth=1, linestyle='dashed', label='30%')
# plt.axhline(y=5, color='red', linewidth=1, linestyle='dashed', label='50%')
#
#
# # Create legend, labels
# plt.legend(loc='upper left')
# plt.xlim(0, 1000)
# plt.ylim(0, 10)
# plt.xlabel('MCR [kW]')
# plt.ylabel('Percent of Weight that is Fuel [-]')
#
# # Save and close figure
# plt.savefig('disp_powratio.png')
# plt.clf()
