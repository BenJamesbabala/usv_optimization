# Weights.py - modified based on http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html
# Estimation of vessel weight as a function of parameters

# package, function, and class imports
from __future__ import division, print_function
from weightCurves import parsonsWts, grubisicWts #modify this if using a different weight estimation
import openmdao.api as om
import math

# the definition of the Weights component
class Weights(om.ExplicitComponent):
    """
    Evaluates the weights based on regressions
    """
    # setup input and output variables for the component
    def setup(self) :
        #setup inputs or variables needed for function
        self.add_input('Cb', val=0.0)
        #self.add_input('D', val=0.0, units='m') - Depth implicitly calculated in grubisicWeights
        self.add_input('T', val=0.0, units='m')
        self.add_input('L', val=0.0, units='m')
        self.add_input('B', val=0.0, units='m')
        #self.add_input('MCR', val=0.0, units='kW') - Fixing power as it is an objective in RFP
        #self.add_input('Vk', val=0.0, units='kn') - Ignoring Vk because we do not intend for velocity to vary during an optimization


        self.add_output('Wt', val=0.0, units='t')

        # Finite difference all partials.
        self.declare_partials('*', '*', method='fd')

    def compute(self, inputs, outputs) :
        # inputs
        Cb = inputs['Cb']
        #D = inputs['D']
        T = inputs['T']
        L = inputs['L']
        B = inputs['B']
        #MCR = inputs['MCR']
        #Vk = inputs['Vk']

        # calls the parsonsWts function - note that other estimations could be used
        #outputs['Wt'] = parsonsWts(Cb, D, T, L, B, MCR, 16) # inputs in unitless, meters, meters, meters, meters, kilowatts, knots
        outputs['Wt'] = grubisicWts(Cb, T, L, B, 500, 16) # inputs in unitless, meters, meters, meters, meters, kilowatts, knots

# debugging code, verifies that inputs, outputs, and calculations are working properly within the component
if __name__ == "__main__":
    #define the model
    model = om.Group()
    #setup independent variables, will be chosen
    #units defined within OpenMDAO for completeness
    ivc = om.IndepVarComp()
    ivc.add_output('Cb', 0.45) #unitless
    #ivc.add_output('D', 4, units='m') #meters
    ivc.add_output('T', 2, units='m') #meters
    ivc.add_output('L', 40, units='m') #meters
    ivc.add_output('B', 6, units='m') #meters
    #ivc.add_output('MCR', 500, units='kW') #kilowatts
    #ivc.add_output('Vk', 16, units='kn') #knots
    #define subsystems to reference variables
    model.add_subsystem('des_vars', ivc)
    model.add_subsystem('wts_comp', Weights())

    #connect variables
    model.connect('des_vars.Cb', 'wts_comp.Cb')
    #model.connect('des_vars.D', 'wts_comp.D')
    model.connect('des_vars.T', 'wts_comp.T')
    model.connect('des_vars.L', 'wts_comp.L')
    model.connect('des_vars.B', 'wts_comp.B')
    #model.connect('des_vars.MCR', 'wts_comp.MCR')
    #model.connect('des_vars.Vk', 'wts_comp.Vk')


    #setup problem and run with initial definitions
    prob = om.Problem(model)
    prob.setup()
    prob.run_model()
    print(prob['wts_comp.Wt'])

    #change definitions and rerun
    prob['des_vars.Cb'] = 0.5
    prob['des_vars.T'] = 2.5
    prob['des_vars.L'] = 45
    prob['des_vars.B'] = 70
    prob.run_model()
    print(prob['wts_comp.Wt'])
