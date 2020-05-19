# package, function, and class imports
from __future__ import division, print_function
import openmdao.api as om
import math
from Weights import Weights
from Stability import Stability
from RatioWeights import RatioWeights

# the definition of the Ratios component
class Ratios(om.ExplicitComponent):
    """
    Evaluates Displacement = weight for reasonable L/B/T Ratios
    """

    # setup input and output variables for the component
    def setup(self) :
        self.add_input('LB') #unitless
        self.add_input('BT') #unitless
        self.add_input('TL') #unitless
        self.add_input('Cb')  #unitless

        self.add_output('L', units='m')
        self.add_output('B', units='m')
        self.add_output('T', units='m')

        # Finite difference all partials.
        self.declare_partials('*', '*', method='fd')


    def compute(self, inputs, outputs) :
        #inputs
        L_to_B = inputs['LB']
        B_to_T = inputs['BT']
        T_to_L = inputs['TL']
        Cb = inputs['Cb']

        # calls the RatioWeights function
        L,B,T,inBound = RatioWeights(L_to_B, B_to_T, T_to_L, Cb) # inputs are unitless,
        # primative error handling
        if inBound == 1:
            print("Success! Converged to: ")
            outputs['L'],outputs['B'],outputs['T'] = L,B,T
        else:
            print("Failed to converge!!!")
            outputs['L'],outputs['B'],outputs['T'] = 0,0,0


# debugging code, verifies that inputs, outputs, and calculations are working properly within the component
if __name__ == "__main__":
    #define the model
    model = om.Group()
    #setup independent variables, will be chosen
    #units defined within OpenMDAO for completeness
    ivc = om.IndepVarComp()
    ivc.add_output('LB', 4.0,) #unitless
    ivc.add_output('BT', 2.0, ) #unitless
    ivc.add_output('TL', 0.15,) #unitless
    ivc.add_output('Cb', 0.4) #unitless

    # define subsystems to reference variables
    model.add_subsystem('des_vars', ivc)
    model.add_subsystem('ratio_comp', Ratios()) # this is the component defined above

    #connect variables, note naming convention
    model.connect('des_vars.LB', 'ratio_comp.LB')
    model.connect('des_vars.BT', 'ratio_comp.BT')
    model.connect('des_vars.TL', 'ratio_comp.TL')
    model.connect('des_vars.Cb', 'ratio_comp.Cb')
    # model.connect('des_vars.Vk', 'ratio_comp.Vk')

    #setup problem and run with initial definitions
    prob = om.Problem(model)
    prob.setup()
    prob.run_model()
    print(prob['ratio_comp.L'])
    print(prob['ratio_comp.B'])
    print(prob['ratio_comp.T'])
    print(prob['ratio_comp.Cb'])


    #change definitions and rerun
    prob['des_vars.LB'] = 3
    prob['des_vars.BT'] = 2.5
    prob['des_vars.TL'] = 0.15
    prob['des_vars.Cb'] = .39
    prob.run_model()
    print(prob['ratio_comp.L'])
    print(prob['ratio_comp.B'])
    print(prob['ratio_comp.T'])
    print(prob['ratio_comp.Cb'])
