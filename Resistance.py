from __future__ import division, print_function
import openmdao.api as om
import math
from resistanceCurves import series64

class Resistance(om.ExplicitComponent):
    """
    Evaluates the hull resistance using Series 64 model test data
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

        outputs['R'] = series64(L, S, Delta, Cb, 16)

if __name__ == "__main__":
    #define the model
    model = om.Group()
    #setup independent variables, will be chosen
    ivc = om.IndepVarComp()
    ivc.add_output('L', 30) #meters
    ivc.add_output('S', 400) #meters^2
    ivc.add_output('Delta', 650) #metric tonnes
    ivc.add_output('Cb', 0.45) #unitless
    # ivc.add_output('Vk', 16) #knots
    #define subsystems to reference variables
    model.add_subsystem('des_vars', ivc)
    model.add_subsystem('resist_comp', Resistance())

    #connect variables
    model.connect('des_vars.L', 'resist_comp.L')
    model.connect('des_vars.S', 'resist_comp.S')
    model.connect('des_vars.Delta', 'resist_comp.Delta')
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
    prob['des_vars.Delta'] = 800
    prob['des_vars.Cb'] = .45
    # prob['des_vars.Vk'] = 16
    prob.run_model()
    print(prob['resist_comp.R'])
