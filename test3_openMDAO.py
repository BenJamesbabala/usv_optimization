# test3_OpenMDAO.py - a first attempt at combining two components in an optimzation, based on http://openmdao.org/twodocs/versions/latest/basic_guide/sellar.html
# Still very much a work in progress, comments will be added throughout process.

from __future__ import division, print_function
import openmdao.api as om
import math
from Resistance import Resistance
from Weights import Weights

class Connect(om.Group):
# Grouping variables

    def setup(self):
        # constants
        rho = 1026.0 #kg/m^3
        g = 9.81 #m/s^2

        indeps = self.add_subsystem('indeps', om.IndepVarComp())
        indeps.add_output('Cb', 0.45) #unitless
        indeps.add_output('L', 30) #meters
        indeps.add_output('D', 4) #meters
        indeps.add_output('T', 2) #meters
        indeps.add_output('B', 6) #meters
        indeps.add_output('S', 400) #meters^2
        indeps.add_output('MCR', 500) #kilowatts
        # setting velocity to be constant, as the optimization can only occur at one speed
        #indeps.add_output('Vk', 16) #knots

        cycle = self.add_subsystem('cycle', om.Group())
        cycle.add_subsystem('resist', Resistance())
        cycle.add_subsystem('wts', Weights())
        cycle.connect('wts.Wt','resist.Delta')
        #cycle.nonlinear_solver = om.NonlinearBlockGS()

        # define the component whose output will be constrained
        self.add_subsystem('const', om.ExecComp('Fn = 8.23/((9.81*L)**(0.5))'))

        #connect components
        self.connect('indeps.Cb', ['cycle.resist.Cb', 'cycle.wts.Cb'])
        self.connect('indeps.L', ['cycle.resist.L', 'cycle.wts.L'])
        self.connect('indeps.D', 'cycle.wts.D')
        self.connect('indeps.T', 'cycle.wts.T')
        self.connect('indeps.B', 'cycle.wts.B')
        self.connect('indeps.S', 'cycle.resist.S')
        # not moving this
        #self.connect('indeps.Vk', 'resist.Vk')

# build the model
prob = om.Problem()
prob.model = Connect()

# setup the optimization
prob.driver = om.ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'COBYLA'
prob.driver.options['maxiter'] = 5000

prob.model.add_design_var('indeps.Cb', lower=.31, upper=.59)
prob.model.add_design_var('indeps.L', lower=15, upper=50)
prob.model.add_design_var('indeps.D', lower=4, upper=6)
prob.model.add_design_var('indeps.T', lower=2, upper=4)
prob.model.add_design_var('indeps.B', lower=3, upper=9)
prob.model.add_design_var('indeps.S', lower=300, upper=900)
#prob.model.add_design_var('indeps.Delta', lower=600, upper=1200)
#prob.model.add_design_var('indeps.Vk', lower=-50, upper=50)

prob.model.add_objective('cycle.resist.R')

# to add the constraint to the model
# this is a Froude number constraint to avoid falling out of bounds
prob.model.add_constraint('const.Fn', lower=.36, upper=1.04)
# this is a block coefficient constraint to avoid falling out of bounds
# prob.model.add_constraint('const.D', lower=1)
#prob.model.add_constraint('indeps.Vk', equals=16.)

prob.setup()
prob.run_driver()

# minimum value
print('R: ', prob['cycle.resist.R'], ' N')
print('Wt: ', prob['cycle.wts.Wt'], ' N')

# location of the minimum
print('Cb: ', prob['indeps.Cb'],' - ')
print('L: ', prob['indeps.L'],' meters ')
print('D: ', prob['indeps.D'],' meters ')
print('T: ', prob['indeps.T'],' meters ')
print('B: ', prob['indeps.B'],' meters ')
print('S: ', prob['indeps.S'],' meters^2 ')
#print(prob['indeps.Vk'])

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
