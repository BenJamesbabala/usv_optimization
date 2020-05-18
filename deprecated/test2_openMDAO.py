# test2_openMDAO.py - based on http://openmdao.org/twodocs/versions/latest/basic_guide/first_optimization.html
# Rough optimization of vessel resistance as a function of parameters with given ranges

# package, function, and class imports
from __future__ import division, print_function
import openmdao.api as om
import math
from Resistance import Resistance

# build the model, defining units in the process`
prob = om.Problem()
indeps = prob.model.add_subsystem('indeps', om.IndepVarComp())
indeps.add_output('L', 30, units='m') #meters
indeps.add_output('S', 400, units='m*m') #meters^2
indeps.add_output('Displ', 650, units='t') #metric tonnes
indeps.add_output('Cb', 0.45) #unitless
# setting velocity to be constant, as the optimization can only occur at one speed
#indeps.add_output('Vk', 16, units='kn') #knots

# add the resistance component previously defined in Resistance.py
prob.model.add_subsystem('resist', Resistance())

# define the component whose output will be constrained
# units defined for L
prob.model.add_subsystem('const', om.ExecComp('Fn = 8.23/((9.81*L)**(0.5))', L={'units': 'm'}))

#connect components
prob.model.connect('indeps.L', ['resist.L', 'const.L'])
prob.model.connect('indeps.S', 'resist.S')
prob.model.connect('indeps.Displ', 'resist.Displ')
prob.model.connect('indeps.Cb', 'resist.Cb')
#prob.model.connect('indeps.Vk', 'resist.Vk')

# setup the optimization
prob.driver = om.ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'COBYLA'
prob.driver.options['maxiter'] = 500

# set the range for the independent variables that will be explored
prob.model.add_design_var('indeps.L', lower=15, upper=50)
prob.model.add_design_var('indeps.S', lower=300, upper=900)
prob.model.add_design_var('indeps.Displ', lower=600, upper=1200)
prob.model.add_design_var('indeps.Cb', lower=.31, upper=.59)
#prob.model.add_design_var('indeps.Vk', lower=-50, upper=50)

# set objective to be minimizing resistance
prob.model.add_objective('resist.R')

# to add the constraint to the model
# this is a Froude number constraint to avoid falling out of bounds
prob.model.add_constraint('const.Fn', lower=.36, upper=1.04)
#prob.model.add_constraint('indeps.Vk', equals=16.)

# setup and run the optimization
prob.setup()
prob.run_driver()

# minimum value
print(prob['resist.R'])

# location of the minimum
print(prob['indeps.L'])
print(prob['indeps.S'])
print(prob['indeps.Displ'])
print(prob['indeps.Cb'])
# print(prob['indeps.Vk'])

# case recording function currently disabled
# # create a case recorder
# recorder = om.SqliteRecorder('cases.sql')
#
# # add the recorder to the driver so driver iterations will be recorded
# prob.driver.add_recorder(recorder)
#
# # add the recorder to the problem so we can manually save a case
# prob.add_recorder(recorder)
#
# # perform setup and run the problem
# prob.setup()
# prob.set_solver_print(0)
# prob.run_driver()
#
# # record the final state of the problem
# prob.record_iteration('final')
#
# # clean up and shut down
# prob.cleanup()
