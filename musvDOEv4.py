# musvDOEv4.py - modified based on http://openmdao.org/twodocs/versions/latest/features/building_blocks/drivers/doe_driver.html
# Third iteration Design of Experiment for US Navy MUSV
# Uses design estimates and regressions to create a vessel with modifications to include flywheel energy storage
# Using case reading example from http://openmdao.org/twodocs/versions/latest/basic_guide/basic_recording.html
# Creates a .csv file with designs generated to be further processed

# package, function, and class imports
from __future__ import division, print_function
from Weights import WeightsNoFuel
from Stability import Stability
from Fuel import Fuel
from Ratios import Ratios
import openmdao.api as om
import math
import csv

# build the model, defining units in the process`
prob = om.Problem()
indeps = prob.model.add_subsystem('indeps', om.IndepVarComp())
#define independent variables (to be explored)
indeps.add_output('Cb', 0.31) #unitless
indeps.add_output('LB', 0.31) #unitless
indeps.add_output('BT', 0.31) #unitless
indeps.add_output('TL', 0.31) #unitless
indeps.add_output('fwCap', 300, units='MJ') #megajoules

# add the fuel weight component from Fuel.py
prob.model.add_subsystem('fuel', Fuel())
# add the weights component from Weights.py
prob.model.add_subsystem('wts', WeightsNoFuel())
# add the stability component from Stability.py
prob.model.add_subsystem('stab', Stability())
# add the ratios component to solve for dimensions from Ratios.py
prob.model.add_subsystem('ratios', Ratios())
#ADD Reliability

# define component whose output will be constrained
# units defined, excess represents the 'excess' displacement of the design
prob.model.add_subsystem('const', om.ExecComp('Disp=1.026*Cb*T*L*B', Disp={'units': 't'}, T={'units': 'm'}, L={'units': 'm'}, B={'units': 'm'}))

#connect components
prob.model.connect('indeps.Cb', ['ratios.Cb','wts.Cb', 'stab.Cb', 'fuel.Cb', 'const.Cb'])
prob.model.connect('indeps.LB', 'ratios.LB')
prob.model.connect('indeps.BT', 'ratios.BT')
prob.model.connect('indeps.TL', 'ratios.TL')
prob.model.connect('ratios.T', ['wts.T', 'stab.T', 'fuel.T', 'const.T'])
prob.model.connect('ratios.L', ['wts.L', 'stab.L', 'fuel.L', 'const.L'])
prob.model.connect('ratios.B', ['wts.B', 'stab.B', 'fuel.B', 'const.B'])
prob.model.connect('fuel.MCR', 'wts.MCR')
prob.model.connect('fuel.fuelWt', 'wts.fuelWt')
prob.model.connect('indeps.fwCap', 'fuel.fwCap')
#ADD Reliability

# set the range for the independent variables that will be explored
prob.model.add_design_var('indeps.Cb', lower=0.31, upper=0.59)
prob.model.add_design_var('indeps.LB', lower=2, upper=7)
prob.model.add_design_var('indeps.BT', lower=0.5, upper=6)
prob.model.add_design_var('indeps.TL', lower=0.1, upper=0.2)
prob.model.add_design_var('indeps.fwCap', lower=0, upper=1000)

# add these variables to be calculated for each design
prob.model.add_design_var('ratios.T')
prob.model.add_design_var('ratios.L')
prob.model.add_design_var('ratios.B')

prob.model.add_design_var('wts.Wt')
prob.model.add_design_var('const.Disp')
prob.model.add_design_var('stab.GMT')
prob.model.add_design_var('fuel.fuelWt')
prob.model.add_design_var('fuel.MCR')
prob.model.add_design_var('fuel.etaRun')
prob.model.add_design_var('fuel.nStarts')

# set driver for design of experiment
#prob.driver = om.DOEDriver(om.UniformGenerator(num_samples=10000))
# latin hypercube is much better at determining edge behavior
prob.driver = om.DOEDriver(om.LatinHypercubeGenerator(samples=50))
prob.driver.add_recorder(om.SqliteRecorder("musvDOEv4cases.sql"))

# this is the meat of the OpenMDAO run
prob.setup()
prob.run_driver()
prob.cleanup()

# --- set up case reading
cr = om.CaseReader("musvDOEv4cases.sql")
cases = cr.list_cases('driver')

# # --- setup write to CSV with outputs
# with open('musvDOEv4cases.csv', mode='w') as csv_file:
#     #set up CSV file to use writer
#     fieldnames = ['Cb','L','B','T','FlywheelCapacity','GMT','Wt','Disp','Excess','MCR','fuelWt','etaRun','nStarts']
#     writer = csv.writer(csv_file,  quoting=csv.QUOTE_NONNUMERIC)
#     #write header
#     writer.writerow(fieldnames)
#
#     for case in cases:
#         #read outputs from data file
#         outputs = cr.get_case(case).outputs
#
#         # write data in a csv (human readable)
#         # add float conversions
#         writer.writerow([float(outputs['indeps.Cb']),float(outputs['ratios.L']),float(outputs['ratios.B']),float(outputs['ratios.T']),float(outputs['indeps.fwCap']),float(outputs['stab.GMT']),float(outputs['wts.Wt']),float(outputs['const.Disp']),float(outputs['const.Disp']-outputs['wts.Wt']),float(outputs['fuel.MCR']),float(outputs['fuel.fuelWt']),float(outputs['fuel.etaRun']),float(outputs['fuel.nStarts'])])

print(len(cases))

#printing related code
values = []
for case in cases:
    outputs = cr.get_case(case).outputs
    values.append((outputs['indeps.LB'], outputs['indeps.BT'], outputs['indeps.TL'], outputs['ratios.L'], outputs['indeps.Cb']))

print("\n".join(["L/B: %5.2f, B/T: %5.2f, T/L: %5.2f, L: %6.2f, Cb: %6.2f" % xyf for xyf in values]))
