# test1_openMDAO.py - a first attempt at optimization based on http://openmdao.org/twodocs/versions/latest/basic_guide/first_optimization.html
# comments are limited as this is not recommended for further use

from __future__ import division, print_function
import openmdao.api as om
import math

class Resistance(om.ExplicitComponent):
    """
    Evaluates the hull resistance using Series 64 model test data
    NOTE: THIS IS A PRELIMINARY RESISTANCE COMPONENT.  SEE Resistance.py FOR THE UPDATED COMPONENT.
    """

    def setup(self) :
        self.add_input('L', val=0.0)
        self.add_input('S', val=0.0)
        self.add_input('Delta', val=0.0)
        self.add_input('Cb', val=0.0)
        #self.add_input('Vk', val=0.0)

        self.add_output('R', val=0.0)

        # Finite difference all partials.
        self.declare_partials('*', '*', method='fd')

    def compute(self, inputs, outputs) :
        #inputs
        L = inputs['L']
        S = inputs['S']
        Delta = inputs['Delta']
        Cb = inputs['Cb']
        #Vk = inputs['Vk']
        Vk = 16

        #constants
        rho = 1026.0 #kg/m^3
        g = 9.81 #m/s^2

        #conversion
        V = Vk/1.944 #m/s
        Fn = V/math.sqrt(g*L) #unitless
        D3 = math.pow(Delta,(1/3)) #meters

        #set up equation for C_R
        if Cb < 0.3:
            #print("Block too low")
            a, n = 0, 0
        elif Cb < 0.4 and Cb >= 0.3 :
            if Fn < 0.35:
                a, n = 0, 0
                #print("invalid Froude Number")
            elif Fn < 0.45 and Fn >= 0.35 :
                a, n = 288, -2.33
            elif Fn < 0.55 and Fn >= 0.45 :
                a, n = 751, -2.76
            elif Fn < 0.65 and Fn >= 0.55 :
                a, n = 758, -2.81
            elif Fn < 0.75 and Fn >= 0.65 :
                a, n = 279, -2.42
            elif Fn < 0.85 and Fn >= 0.75 :
                a, n = 106, -2.06
            elif Fn < 0.95 and Fn >= 0.85 :
                a, n = 47, -1.74
            elif Fn < 1.05 and Fn >= 0.95 :
                a, n = 25, -1.50
            else:
                a,n = 0,0
                #print("invalid Froude Number")
        elif Cb < 0.5 and Cb >= 0.4 :
            if Fn < 0.35:
                a, n = 0, 0
                #print("invalid Froude Number")
            elif Fn < 0.45 and Fn >= 0.35 :
                a, n = 36726, -4.41
            elif Fn < 0.55 and Fn >= 0.45 :
                a, n = 55159, -4.61
            elif Fn < 0.65 and Fn >= 0.55 :
                a, n = 42184, -4.56
            elif Fn < 0.75 and Fn >= 0.65 :
                a, n = 29257, -4.47
            elif Fn < 0.85 and Fn >= 0.75 :
                a, n = 27130, -4.51
            elif Fn < 0.95 and Fn >= 0.85 :
                a, n = 20657, -4.46
            elif Fn < 1.05 and Fn >= 0.95 :
                a, n = 11644, -4.24
            else:
                a,n = 0,0
                #print("invalid Froude Number")
        elif Cb < 0.6 and Cb >= 0.5 :
            if Fn < 0.35:
                a, n = 0, 0
                #print("invalid Froude Number")
            elif Fn < 0.45 and Fn >= 0.35 :
                a, n = 926, -2.74
            elif Fn < 0.55 and Fn >= 0.45 :
                a, n = 1775, -3.05
            elif Fn < 0.65 and Fn >= 0.55 :
                a, n = 1642, -3.08
            elif Fn < 0.75 and Fn >= 0.65 :
                a, n = 1106, -2.98
            elif Fn < 0.85 and Fn >= 0.75 :
                a, n = 783, -2.90
            elif Fn < 0.95 and Fn >= 0.85 :
                a, n = 458, -2.73
            elif Fn < 1.05 and Fn >= 0.95 :
                a, n = 199, -2.38
            else:
                a,n = 0,0
                #print("invalid Froude Number")
        else:
            #print("Block too high")
            a, n = 0, 0

        #estimate C_R
        C = (a*(math.pow((L/D3),n)))/1000 #unitless

        #checks
        #print("C_R: ", round(C,5), " - ")
        #print("S: ",round(S,2), " m^2 ")
        #print("V: ",round(V,3), " m/s ")
        #print("Fn: ",round(Fn,4), " - ")

        #calulate and return R
        outputs['R'] = C*(0.5)*rho*S*V*V #newtons

# build the model
prob = om.Problem()
indeps = prob.model.add_subsystem('indeps', om.IndepVarComp())
indeps.add_output('L', 30) #meters
indeps.add_output('S', 400) #meters^2
indeps.add_output('Delta', 650) #metric tonnes
indeps.add_output('Cb', 0.45) #unitless
# setting velocity to be constant, as the optimization can only occur at one speed
#indeps.add_output('Vk', 16) #knots

prob.model.add_subsystem('resist', Resistance())

# define the component whose output will be constrained
prob.model.add_subsystem('const', om.ExecComp('Fn = 8.23/((9.81*L)**(0.5))'))

#connect components
prob.model.connect('indeps.L', ['resist.L', 'const.L'])
prob.model.connect('indeps.S', 'resist.S')
prob.model.connect('indeps.Delta', 'resist.Delta')
prob.model.connect('indeps.Cb', 'resist.Cb')
#prob.model.connect('indeps.Vk', 'resist.Vk')

# setup the optimization
prob.driver = om.ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'COBYLA'
prob.driver.options['maxiter'] = 500

prob.model.add_design_var('indeps.L', lower=15, upper=50)
prob.model.add_design_var('indeps.S', lower=300, upper=900)
prob.model.add_design_var('indeps.Delta', lower=600, upper=1200)
prob.model.add_design_var('indeps.Cb', lower=.31, upper=.59)
#prob.model.add_design_var('indeps.Vk', lower=-50, upper=50)

prob.model.add_objective('resist.R')

# to add the constraint to the model
# this is a Froude number constraint to avoid falling out of bounds
prob.model.add_constraint('const.Fn', lower=.36, upper=1.04)
#prob.model.add_constraint('indeps.Vk', equals=16.)

# prob.setup()
# prob.run_driver()
#
# # minimum value
# print(prob['resist.R'])
#
# # location of the minimum
# print(prob['indeps.L'])
# print(prob['indeps.S'])
# print(prob['indeps.Delta'])
# print(prob['indeps.Cb'])
# #print(prob['indeps.Vk'])

# create a case recorder
recorder = om.SqliteRecorder('cases.sql')

# add the recorder to the driver so driver iterations will be recorded
prob.driver.add_recorder(recorder)

# add the recorder to the problem so we can manually save a case
prob.add_recorder(recorder)

# perform setup and run the problem
prob.setup()
prob.set_solver_print(0)
prob.run_driver()

# record the final state of the problem
prob.record_iteration('final')

# clean up and shut down
prob.cleanup()
