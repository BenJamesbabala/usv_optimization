# musvOPTv1Plotter.py - from
# Reads output from NSGA2 optimization and plots

import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

outpath = './results/OPTv1/'

# setup read of output file
with open('nsga2_best_pop.out', newline='') as csv_file:
    # skip header rows
    next(csv_file)
    next(csv_file)

    # read csv file
    reader = csv.reader(csv_file, delimiter='	', quoting=csv.QUOTE_NONNUMERIC)

    # -- set up lists for data
    # objectives
    Disp = [] # index = 0
    nStarts = [] # index = 1

    # constraints
    Wt = [] # index = 3
    GMT = [] # index = 5
    MCR = [] # index = 7
    fuelWt = [] # index = 9
    Excess = [] # index = 11
    etaRun = [] # index = 13
    PBratio = [] # index = 15

    # design variables
    Cb = [] # index = 16
    T = [] # index = 17
    L = [] # index = 18
    B = [] # index = 19
    fwCap = [] # index = 20

    # calculated values
    percentFuel = []
    LB = []
    BT = []
    TL = []

    # iterate through all designs
    for row in reader:
        #read data into lists
        Disp.append(row[0])
        nStarts.append(row[1])

        Wt.append(row[3])
        GMT.append(row[5])
        MCR.append(row[7])
        fuelWt.append(row[9])
        Excess.append(row[11])
        etaRun.append((row[13]*100)) #convert to percentage
        PBratio.append(row[15])

        Cb.append(row[16])
        T.append(row[17])
        L.append(row[18])
        B.append(row[19])
        fwCap.append(row[20])

        percentFuel.append((row[9]/row[3])*100)  #convert to percentage

        LB.append(row[18]/row[19])
        BT.append(row[19]/row[17])
        TL.append(row[17]/row[18])
        print("L: ",row[18]," B: ",row[19]," T: ",row[17]," Cb: ",row[16])

    numFeasible = len(Disp)


#---- SOME PLOTS ---

# # test of 3D plotting
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# # # --- dimension ratios
# # ax.scatter(LB, BT, TL)
# #
# # ax.set_xlabel('L/B [-]')
# # ax.set_ylabel('B/T [-]')
# # ax.set_zlabel('T/L [-]')
# # # --- MCR, etaRun, nStarts
# # ax.scatter(PBcru, etaRun, nStarts)
# #
# # ax.set_xlabel('Cruise MCR [kW]')
# # ax.set_ylabel('Runtime [%]')
# # ax.set_zlabel('Num. Starts [-]')
#
# plt.show()
#
# # # Save and close figure
# # plt.savefig(outpath+'Wt_Disp.png')
# # plt.clf()

#-----
# plot flywheel capacity and engine starts
plt.plot(fwCap, nStarts, color='green', marker='o', linewidth=0, markersize=2, label=(str(numFeasible) + ' Feasible Designs'))
plt.axhline(y=0, color='black', linewidth=1)
plt.axhline(y=50, color='red', linewidth=1, linestyle='dashed', label='50 Starts')

# Create legend, labels
plt.legend(loc='upper right')
#plt.xscale("log")
#plt.xlim(0, 1100)
#plt.ylim(17200, 18000)
plt.xlabel('FESD Capacity [MJ]')
plt.ylabel('Loitering Engine Starts [-]')

# Save and close figure
plt.savefig(outpath+'fwCap_nStarts.png')
plt.clf()

#-----
# plot flywheel capacity and engine runtime
plt.plot(fwCap, etaRun, color='green', marker='o', linewidth=0, markersize=2, label=(str(numFeasible) + ' Feasible Designs'))
plt.axhline(y=0.1, color='green', linewidth=1, linestyle='dashed', label='0.1%')
plt.axhline(y=0.5, color='orange', linewidth=1, linestyle='dashed', label='0.5%')
plt.axhline(y=1, color='red', linewidth=1, linestyle='dashed', label='1.0%')

# Create legend, labels
plt.legend(loc='upper left')
#plt.xscale("log")
#plt.xlim(0, 1100)
plt.ylim(0, 2)
plt.xlabel('FESD Capacity [MJ]')
plt.ylabel('Loitering Engine Runtime [%]')

# Save and close figure
plt.savefig(outpath+'fwCap_etaRun.png')
plt.clf()

#-----
# plot MCR and engine starts and runtime
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

ax1.plot(MCR, nStarts, color='green', marker='o', linewidth=0, markersize=2, label='Starts')
ax2.plot(MCR, etaRun, color='red', marker='o', linewidth=0, markersize=2, label='Runtime')

# Create legend, labels
fig.legend(loc='upper left')
#plt.xlim(0, 2000)
#plt.ylim(0, 3)
ax1.set_xlabel('Max MCR [kW]')
ax1.set_ylabel('Loitering Engine Starts [-]')
ax2.set_ylabel('Loitering Engine Runtime [%]')


# Save and close figure
plt.savefig(outpath+'nStarts_etaRun_1.png')
plt.clf()

#-----
# plot number of starts and runtime percentage
plt.plot(nStarts, etaRun, color='green', marker='o', linewidth=0, markersize=2, label=(str(numFeasible) + ' Feasible Designs'))

# Create legend, labels
plt.legend(loc='upper left')
#plt.xlim(0, 200)
#plt.ylim(0, 2)
plt.xlabel('Number of Starts [-]')
plt.ylabel('Runtime [%]')

# Save and close figure
plt.savefig(outpath+'nStarts_etaRun_2.png')
plt.clf()

#-----
# plot displacement and number of starts
plt.plot(Disp, nStarts, color='green', marker='o', linewidth=0, markersize=2, label=(str(numFeasible) + ' Feasible Designs'))

# Create legend, labels
plt.legend(loc='upper right')
plt.xlim(0, 1000)
plt.ylim(0, 400)
plt.xlabel('Displacement [MT]')
plt.ylabel('Number of Starts [-]')

# Save and close figure
plt.savefig(outpath+'disp_nStarts.png')
plt.clf()

#-----
# plot displacement and number of starts
plt.plot(Disp, fwCap, color='green', marker='o', linewidth=0, markersize=2, label=(str(numFeasible) + ' Feasible Designs'))

# Create legend, labels
plt.legend(loc='upper right')
plt.xlim(0, 500)
plt.ylim(0, 1100)
plt.xlabel('Displacement [MT]')
plt.ylabel('Flywheel Capacity [MJ]')

# Save and close figure
plt.savefig(outpath+'disp_fwCap.png')
plt.clf()

#-----
# plot weight and displacement
plt.plot(Wt, Disp, color='green', marker='o', linewidth=0, markersize=2, label=(str(numFeasible) + ' Feasible Designs'))
plt.plot(Wt, Wt, label='Equal', color='red', linewidth=2)

# Create legend, labels
plt.legend(loc='upper left')
plt.xlim(100, 400)
plt.ylim(100, 400)
plt.xlabel('Weight [MT]')
plt.ylabel('Displacement [MT]')

# Save and close figure
plt.savefig(outpath+'Wt_Disp.png')
plt.clf()

#-----
# plot displacement and stability
plt.plot(Disp, GMT, color='green', marker='o', linewidth=0, markersize=2, label=(str(numFeasible) + ' Feasible Designs'))
plt.axhline(y=0, color='red', linewidth=2)
plt.axhline(y=.50, color='red', linewidth=1, linestyle='dashed')

# Create legend, labels
plt.legend(loc='upper left')
plt.xlim(100, 300)
plt.ylim(-.25, 1.25)
plt.xlabel('Displacement [MT]')
plt.ylabel('GMT [m]')

# Save and close figure
plt.savefig(outpath+'disp_gmt.png')
plt.clf()

#----
# plot fuel weight and MCR
plt.plot(MCR, percentFuel, color='green', marker='o', linewidth=0, markersize=2, label=(str(numFeasible) + ' Feasible Designs'))
plt.axhline(y=10, color='green', linewidth=1, linestyle='dashed', label='10%')
plt.axhline(y=30, color='orange', linewidth=1, linestyle='dashed', label='30%')
plt.axhline(y=50, color='red', linewidth=1, linestyle='dashed', label='50%')

# Create legend, labels
plt.legend(loc='upper left')
#plt.xlim(0, 2000)
plt.ylim(0, 80)
plt.xlabel('Max MCR [kW]')
plt.ylabel('Percent of Weight that is Fuel [-]')

# Save and close figure
plt.savefig(outpath+'fuel_mcr.png')
plt.clf()

#----
# plot displacement and power ratio
plt.plot(MCR, PBratio, color='green', marker='o', linewidth=0, markersize=2, label=(str(numFeasible) + ' Feasible Designs'))
plt.axhline(y=1, color='green', linewidth=1, linestyle='dashed', label='Equal')
plt.axhline(y=1.5, color='orange', linewidth=1, linestyle='dashed', label='1.5 times')
plt.axhline(y=2, color='red', linewidth=1, linestyle='dashed', label='2 times')

# Create legend, labels
plt.legend(loc='lower left')
#plt.xlim(0, 2000)
plt.ylim(0, 5)
plt.xlabel('Max MCR [kW]')
plt.ylabel('Sprint to Cruise Power Ratio [-]')

# Save and close figure
plt.savefig(outpath+'mcr_powratio.png')
plt.clf()
