# musvDOEv3.py - modified based on http://openmdao.org/twodocs/versions/latest/features/building_blocks/drivers/doe_driver.html
# First iteration Design of Experiment for US Navy MUSV
# Uses design estimates and regressions to create a vessel with modifications to include flywheel energy storage
# Using case reading example from http://openmdao.org/twodocs/versions/latest/basic_guide/basic_recording.html
# Creates a .csv file with designs generated to be further processed

# package, function, and class imports
from __future__ import division, print_function
from Weights import WeightsNoFuel
from Stability import Stability
from Fuel import Fuel
import openmdao.api as om
import math
import csv

# build the model, defining units in the process`
prob = om.Problem()
indeps = prob.model.add_subsystem('indeps', om.IndepVarComp())
#define independent variables (to be explored)
indeps.add_output('Cb', 0.31) #unitless
indeps.add_output('T', 2, units='m') #meters
indeps.add_output('L', 20, units='m') #meters
indeps.add_output('B', 5, units='m') #meters
indeps.add_output('fwCap', 300, units='MJ') #megajoules

# add the fuel weight component from Fuel.py
prob.model.add_subsystem('fuel', Fuel()) #, promotes=['Cb','T','L','B','fuelWt','MCR','etaRun','nStarts'])
# add the weights component from Weights.py
prob.model.add_subsystem('wts', WeightsNoFuel())
# add the stability component from Stability.py
prob.model.add_subsystem('stab',Stability())

# define component whose output will be constrained
# units defined, excess represents the 'excess' displacement of the design
prob.model.add_subsystem('const', om.ExecComp('Disp=1.026*Cb*T*L*B', Disp={'units': 't'}, T={'units': 'm'}, L={'units': 'm'}, B={'units': 'm'}))

#connect components
prob.model.connect('indeps.Cb', ['wts.Cb', 'stab.Cb', 'fuel.Cb', 'const.Cb'])
prob.model.connect('indeps.T', ['wts.T', 'stab.T', 'fuel.T', 'const.T'])
prob.model.connect('indeps.L', ['wts.L', 'stab.L', 'fuel.L', 'const.L'])
prob.model.connect('indeps.B', ['wts.B', 'stab.B', 'fuel.B', 'const.B'])
prob.model.connect('fuel.MCR', 'wts.MCR')
prob.model.connect('fuel.fuelWt', 'wts.fuelWt')
prob.model.connect('indeps.fwCap', 'fuel.fwCap')

# set the range for the independent variables that will be explored
prob.model.add_design_var('indeps.Cb', lower=0.31, upper=0.59)
prob.model.add_design_var('indeps.T', lower=2, upper=5)
prob.model.add_design_var('indeps.L', lower=25, upper=50)
prob.model.add_design_var('indeps.B', lower=3, upper=12)
prob.model.add_design_var('indeps.fwCap', lower=0, upper=1000)

# add these variables to be calculated for each design
prob.model.add_design_var('wts.Wt')
prob.model.add_design_var('const.Disp')
prob.model.add_design_var('stab.GMT')
prob.model.add_design_var('fuel.fuelWt')
prob.model.add_design_var('fuel.MCR')
prob.model.add_design_var('fuel.etaRun')
prob.model.add_design_var('fuel.nStarts')

# OBJECTIVES NOT USED WITH DOEDriver
# set objective to be minimizing weight
# prob.model.add_objective('wts.Wt')
# set objective to be minimizing excess displacement
# prob.model.add_objective('const.excess')

# set driver for design of experiment
#prob.driver = om.DOEDriver(om.UniformGenerator(num_samples=10000))
# latin hypercube is much better at determining edge behavior
prob.driver = om.DOEDriver(om.LatinHypercubeGenerator(samples=15000))
prob.driver.add_recorder(om.SqliteRecorder("musvDOEv3cases.sql"))

# this is the meat of the OpenMDAO run
prob.setup()
prob.run_driver()
prob.cleanup()

# set up case reading
cr = om.CaseReader("musvDOEv3cases.sql")
cases = cr.list_cases('driver')

# setup write to CSV with outputs
with open('musvDOEv3cases.csv', mode='w') as csv_file:
    #set up CSV file to use writer
    fieldnames = ['Cb','L','B','T','FlywheelCapacity','GMT','Wt','Disp','Excess','MCR','fuelWt','etaRun','nStarts']
    writer = csv.writer(csv_file,  quoting=csv.QUOTE_NONNUMERIC)
    #write header
    writer.writerow(fieldnames)

    for case in cases:
        #read outputs from data file
        outputs = cr.get_case(case).outputs

        # write data in a csv (human readable)
        # add float conversions
        writer.writerow([float(outputs['indeps.Cb']),float(outputs['indeps.L']),float(outputs['indeps.B']),float(outputs['indeps.T']),float(outputs['indeps.fwCap']),float(outputs['stab.GMT']),float(outputs['wts.Wt']),float(outputs['const.Disp']),float(outputs['const.Disp']-outputs['wts.Wt']),float(outputs['fuel.MCR']),float(outputs['fuel.fuelWt']),float(outputs['fuel.etaRun']),float(outputs['fuel.nStarts'])])

# print(len(cases))
#
# printing related code
# values = []
# for case in cases:
#     outputs = cr.get_case(case).outputs
#     values.append((outputs['fuel.fuelWt'], outputs['indeps.L'], outputs['stab.GMT'], outputs['wts.Wt'], outputs['fuel.nStarts']))
#
# print("\n".join(["Fuel Wt: %5.2f, L: %5.2f, GMT: %5.2f, Wt: %6.2f, Num Starts: %6.2f" % xyf for xyf in values]))
