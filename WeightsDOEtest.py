# WeightsDOEtest.py - modified based on http://openmdao.org/twodocs/versions/latest/features/building_blocks/drivers/doe_driver.html
# Design of Experiment for weight estimation of vessel weight as a function of parameters

# package, function, and class imports
from __future__ import division, print_function
from Weights import Weights
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

# add the weights component previously defined in Weights.py
prob.model.add_subsystem('wts', Weights())

# define component whose output will be constrained
# units defined, excess represents the 'excess' displacement of the design
prob.model.add_subsystem('const', om.ExecComp('excess = (Cb*L*T*B) - Wt', excess={'units': 't'}, Wt={'units': 't'}, T={'units': 'm'}, L={'units': 'm'}, B={'units': 'm'}))

#connect components
prob.model.connect('indeps.Cb', ['wts.Cb', 'const.Cb'])
prob.model.connect('indeps.T', ['wts.T', 'const.T'])
prob.model.connect('indeps.L', ['wts.L', 'const.L'])
prob.model.connect('indeps.B', ['wts.B', 'const.B'])
prob.model.connect('wts.Wt', 'const.Wt')

# set the range for the independent variables that will be explored
prob.model.add_design_var('indeps.Cb', lower=0.31, upper=0.59)
prob.model.add_design_var('indeps.T', lower=2, upper=7)
prob.model.add_design_var('indeps.L', lower=20, upper=50)
prob.model.add_design_var('indeps.B', lower=5, upper=15)

# set objective to be minimizing weight
prob.model.add_objective('wts.Wt')
# set objective to be minimizing excess displacement
prob.model.add_objective('const.excess')

# add the constraint to the model
# this is a displacement constraint to avoid nonfeasible solutions
# NOTE: Constraints do not seem affect the range of solutions tested in design of experiments
#prob.model.add_constraint('const.excess', lower=0, upper=100)


# set driver for design of experiment
prob.driver = om.DOEDriver(om.UniformGenerator(num_samples=50))
#prob.driver = om.DOEDriver(om.LatinHypercubeGenerator(samples=10))
prob.driver.add_recorder(om.SqliteRecorder("cases.sql"))

prob.setup()
prob.run_driver()
prob.cleanup()

# set up case recording
cr = om.CaseReader("cases.sql")
cases = cr.list_cases('driver')

print(len(cases))

# printing related code
values = []
for case in cases:
    outputs = cr.get_case(case).outputs
    values.append((outputs['indeps.Cb'], outputs['indeps.L'], outputs['indeps.B'], outputs['indeps.T'], outputs['wts.Wt'], outputs['const.excess']))
    #values.append((outputs['indeps.Cb'], outputs['indeps.L'], outputs['wts.Wt']))

print("\n".join(["Cb: %5.2f, L: %5.2f, B: %5.2f, T: %5.2f, Wt: %6.2f, Excess Displacement: %6.2f" % xyf for xyf in values]))
