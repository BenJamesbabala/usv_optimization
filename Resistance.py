# Resistance.py - modified based on http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html
# Estimation of vessel resistance as a function of parameters

# package, function, and class imports
from __future__ import division, print_function
import openmdao.api as om
import math
from resistanceCurves import series64 #modify this if using a different resistance curve

# the definition of the Resistance component
class Resistance(om.ExplicitComponent):
    """
    Evaluates the hull resistance using Series 64 model test data
    """

    # setup input and output variables for the component
    def setup(self) :
        self.add_input('L', units='m')
        self.add_input('S', units='m*m')
        self.add_input('Displ', units='t')
        self.add_input('Cb')
        #self.add_input('Vk', units='kn') - Ignoring Vk because we do not intend for velocity to vary during an optimization

        self.add_output('R', units='N')

        # Finite difference all partials.
        self.declare_partials('*', '*', method='fd')


    def compute(self, inputs, outputs) :
        #inputs
        L = inputs['L']
        S = inputs['S']
        Displ = inputs['Displ']
        Cb = inputs['Cb']
        #Vk = inputs['Vk']

        # calls the series64 function - note that other resistance curves could be used
        outputs['R'] = series64(L, S, Displ, Cb, 16) # inputs in meters, meters^2,

# debugging code, verifies that inputs, outputs, and calculations are working properly within the component
if __name__ == "__main__":
    #define the model
    model = om.Group()
    #setup independent variables, will be chosen
    #units defined within OpenMDAO for completeness
    ivc = om.IndepVarComp()
    ivc.add_output('L', 30, units='m') #meters
    ivc.add_output('S', 400, units='m*m') #meters^2
    ivc.add_output('Displ', 650, units='t') #metric tonnes
    ivc.add_output('Cb', 0.45) #unitless
    # ivc.add_output('Vk', 16, units='kn') #knots

    # define subsystems to reference variables
    model.add_subsystem('des_vars', ivc)
    model.add_subsystem('resist_comp', Resistance()) # this is the component defined above

    #connect variables, note naming convention
    model.connect('des_vars.L', 'resist_comp.L')
    model.connect('des_vars.S', 'resist_comp.S')
    model.connect('des_vars.Displ', 'resist_comp.Displ')
    model.connect('des_vars.Cb', 'resist_comp.Cb')
    # model.connect('des_vars.Vk', 'resist_comp.Vk')

    #setup problem and run with initial definitions
    prob = om.Problem(model)
    prob.setup()
    prob.run_model()
    print(prob['resist_comp.R'])

    #change definitions and rerun
    prob['des_vars.L'] = 40
    prob['des_vars.S'] = 500
    prob['des_vars.Displ'] = 800
    prob['des_vars.Cb'] = .45
    # prob['des_vars.Vk'] = 16
    prob.run_model()
    print(prob['resist_comp.R'])
