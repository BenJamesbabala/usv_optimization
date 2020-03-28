# Stability.py - modified based on http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html
# Estimation of vessel upright stability

# package, function, and class imports
from __future__ import division, print_function
from estGMT import estGMT
import openmdao.api as om
import math

# the definition of the Weights component
class Stability(om.ExplicitComponent):
    """
    Evaluates the metacentric height based on rudimentary equations
    """
    # setup input and output variables for the component
    def setup(self) :
        #setup inputs or variables needed for function
        self.add_input('Cb', val=0.0)
        self.add_input('T', val=0.0, units='m')
        self.add_input('L', val=0.0, units='m')
        self.add_input('B', val=0.0, units='m')

        self.add_output('GMT', val=0.0, units='m')

        # Finite difference all partials.
        self.declare_partials('*', '*', method='fd')

    def compute(self, inputs, outputs) :
        # inputs
        Cb = inputs['Cb']
        T = inputs['T']
        L = inputs['L']
        B = inputs['B']

        # calls the estGMT function - note that other estimations could be used
        outputs['GMT'] = estGMT(Cb, T, L, B) # inputs in unitless, meters, meters, meters

# debugging code, verifies that inputs, outputs, and calculations are working properly within the component
if __name__ == "__main__":
    #define the model
    model = om.Group()
    #setup independent variables, will be chosen
    #units defined within OpenMDAO for completeness
    ivc = om.IndepVarComp()
    ivc.add_output('Cb', 0.45) #unitless
    ivc.add_output('T', 2, units='m') #meters
    ivc.add_output('L', 40, units='m') #meters
    ivc.add_output('B', 6, units='m') #meters

    #define subsystems to reference variables
    model.add_subsystem('des_vars', ivc)
    model.add_subsystem('stab_comp', Stability())

    #connect variables
    model.connect('des_vars.Cb', 'stab_comp.Cb')
    model.connect('des_vars.T', 'stab_comp.T')
    model.connect('des_vars.L', 'stab_comp.L')
    model.connect('des_vars.B', 'stab_comp.B')

    #setup problem and run with initial definitions
    prob = om.Problem(model)
    prob.setup()
    prob.run_model()
    print(prob['stab_comp.GMT'])

    #change definitions and rerun
    prob['des_vars.Cb'] = 0.5
    prob['des_vars.T'] = 2.5
    prob['des_vars.L'] = 45
    prob['des_vars.B'] = 7
    prob.run_model()
    print(prob['stab_comp.GMT'])
