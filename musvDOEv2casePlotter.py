# musvDOE1casePlotter.py - from
# Reads WeightsDOE.csv and plots

import csv
import matplotlib.pyplot as plt

# setup write to CSV with outputs
with open('WeightsDOE.csv', newline='') as csv_file:
    # read csv file
    reader = csv.reader(csv_file, quoting=csv.QUOTE_NONNUMERIC)

    # skip header row
    next(reader)

    # set up lists for data
    Cb = [] # index = 0
    L = [] # index = 1
    B = [] # index = 2
    T = [] # index = 3
    GMT = [] # index = 4
    Wt = [] # index = 5
    Disp = [] # index = 6
    Excess = [] # index = 7
    MCR = [] # index = 8
    fuelWt = [] # index = 9
    percentFuel = []

    # iterate through all designs
    for row in reader:
        # require positive GMT
        #if row[4] > 0:
            # require weight/displacement within 10%
            #if abs(row[7]) < (0.1*row[5]):
                #read data into lists
                Cb.append(row[0])
                L.append(row[1])
                B.append(row[2])
                T.append(row[3])
                GMT.append(row[4])
                Wt.append(row[5])
                Disp.append(row[6])
                Excess.append(row[7])
                MCR.append(row[8])
                fuelWt.append(row[9])
                percentFuel.append(row[9]/row[5])


#---- SOME PLOTS
# plot weight and displacement
plt.plot(Wt, Disp, color='blue', marker='o', linewidth=0, markersize=2, label='Designs')
plt.plot(Wt, Wt, label='Equal', color='red', linewidth=2)

# Create legend, labels
plt.legend(loc='upper left')
plt.xlim(100, 600)
plt.ylim(100, 600)
plt.xlabel('Weight [MT]')
plt.ylabel('Displacement [MT]')

# Save and close figure
plt.savefig('Wt_Disp.png')
plt.clf()

#-----
# plot length and "excess" displacement
plt.plot(L, Excess, color='blue', marker='o', linewidth=0, markersize=2, label='Designs')
plt.axhline(y=0, color='red', linewidth=2)
plt.axhline(y=-50, color='red', linewidth=1, linestyle='dashed')
plt.axhline(y=50, color='red', linewidth=1, linestyle='dashed')


# Create legend, labels
plt.legend(loc='upper left')
plt.xlim(20, 55)
plt.ylim(-100, 300)
plt.xlabel('Length [m]')
plt.ylabel('Excess Displacement [MT]')

# Save and close figure
plt.savefig('L_Excess.png')
plt.clf()

#-----
# plot displacement and stability
plt.plot(Disp, GMT, color='blue', marker='o', linewidth=0, markersize=2, label='Designs')
plt.axhline(y=0, color='red', linewidth=2)
plt.axhline(y=.50, color='red', linewidth=1, linestyle='dashed')


# Create legend, labels
plt.legend(loc='upper left')
plt.xlim(0, 600)
plt.ylim(-1, 3)
plt.xlabel('Displacement [MT]')
plt.ylabel('GMT [m]')

# Save and close figure
plt.savefig('disp_gmt.png')
plt.clf()

#----
# plot fuel weight and MCR
plt.plot(MCR, percentFuel, color='blue', marker='o', linewidth=0, markersize=2, label='Designs')
plt.axhline(y=.1, color='green', linewidth=1, linestyle='dashed', label='10%')
plt.axhline(y=.3, color='orange', linewidth=1, linestyle='dashed', label='30%')
plt.axhline(y=.5, color='red', linewidth=1, linestyle='dashed', label='50%')


# Create legend, labels
plt.legend(loc='upper left')
plt.xlim(0, 2000)
plt.ylim(0, 0.8)
plt.xlabel('MCR [kW]')
plt.ylabel('Percent of Weight that is Fuel [-]')

# Save and close figure
plt.savefig('fuel_mcr.png')
plt.clf()
