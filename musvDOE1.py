# musvDOE1.py - modified based on http://openmdao.org/twodocs/versions/latest/features/building_blocks/drivers/doe_driver.html
# First iteration Design of Experiment for US Navy MUSV

# package, function, and class imports
from __future__ import division, print_function
from Weights import WeightsNoFuel
from Stability import Stability
from Fuel import Fuel
import openmdao.api as om
import math

# build the model, defining units in the process`
prob = om.Problem()
indeps = prob.model.add_subsystem('indeps', om.IndepVarComp())
#define independent variables (to be explored)
indeps.add_output('Cb', 0.31) #unitless
indeps.add_output('T', 2, units='m') #meters
indeps.add_output('L', 20, units='m') #meters
indeps.add_output('B', 5, units='m') #meters

# add the fuel weight component from Fuel.py
prob.model.add_subsystem('fuel', Fuel())
# add the weights component from Weights.py
prob.model.add_subsystem('wts', WeightsNoFuel())
# add the stability component from Stability.py
prob.model.add_subsystem('stab',Stability())

# define component whose output will be constrained
# units defined, excess represents the 'excess' displacement of the design
prob.model.add_subsystem('const', om.ExecComp('Disp=Cb*T*L*B', Disp={'units': 't'}, T={'units': 'm'}, L={'units': 'm'}, B={'units': 'm'}))

#connect components
prob.model.connect('indeps.Cb', ['wts.Cb', 'stab.Cb', 'fuel.Cb', 'const.Cb'])
prob.model.connect('indeps.T', ['wts.T', 'stab.T', 'fuel.T', 'const.T'])
prob.model.connect('indeps.L', ['wts.L', 'stab.L', 'fuel.L', 'const.L'])
prob.model.connect('indeps.B', ['wts.B', 'stab.B', 'fuel.B', 'const.B'])
prob.model.connect('fuel.MCR', 'wts.MCR')
prob.model.connect('fuel.fuel', 'wts.fuel')

# set the range for the independent variables that will be explored
prob.model.add_design_var('indeps.Cb', lower=0.31, upper=0.59)
prob.model.add_design_var('indeps.T', lower=2, upper=5)
prob.model.add_design_var('indeps.L', lower=25, upper=50)
prob.model.add_design_var('indeps.B', lower=3, upper=12)
prob.model.add_design_var('wts.Wt')
prob.model.add_design_var('const.Disp')

# set objective to be minimizing weight
# prob.model.add_objective('wts.Wt')
# set objective to be minimizing excess displacement
# prob.model.add_objective('const.excess')

# add the constraint to the model
# this is a stability constraint to avoid nonfeasible solutions
prob.model.add_constraint('stab.GMT', lower=0)
# this is an attempt to get a wt/disp constraint
# prob.model.add_constraint('const.Disp', lower='wts.Wt')
prob.model.add_constraint('const.Disp', upper=500)

# set driver for design of experiment
#prob.driver = om.DOEDriver(om.UniformGenerator(num_samples=50))
prob.driver = om.DOEDriver(om.LatinHypercubeGenerator(samples=500))
prob.driver.add_recorder(om.SqliteRecorder("musvDOE1cases.sql"))

prob.setup()
prob.run_driver()
prob.cleanup()

# set up case reading
cr = om.CaseReader("musvDOE1cases.sql")
cases = cr.list_cases('driver')

print(len(cases))

# printing related code
values = []
for case in cases:
    outputs = cr.get_case(case).outputs
    values.append((outputs['indeps.Cb'], outputs['indeps.L'], outputs['stab.GMT'], outputs['wts.Wt'], outputs['const.Disp']))

print("\n".join(["Cb: %5.2f, L: %5.2f, GMT: %5.2f, Wt: %6.2f, Disp: %6.2f" % xyf for xyf in values]))
