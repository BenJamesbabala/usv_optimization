# Fuel.py - modified based on http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html
# Estimation of vessel's fuel weight as a function of parameters

# package, function, and class imports
from __future__ import division, print_function
import openmdao.api as om
import math
from fuelEstimate import missionFuel1, missionFuel1FW
from estParam import wettedSurf, displacement

# the definition of the Resistance component
class Fuel(om.ExplicitComponent):
    """
    Evaluates the fuel weight for a mission using resistance and powering estimates
    """

    # setup input and output variables for the component
    def setup(self) :
        self.add_input('L', units='m')
        self.add_input('B', units='m')
        self.add_input('T', units='m')
        self.add_input('Cb')
        self.add_input('fwCap', units='MJ')

        self.add_output('fuelWt', units='t')
        self.add_output('MCR', units='kW')
        self.add_output('etaRun')
        self.add_output('nStarts')

        # Finite difference all partials.
        self.declare_partials('*', '*', method='fd')


    def compute(self, inputs, outputs) :
        #inputs
        L = inputs['L']
        B = inputs['B']
        T = inputs['T']
        Cb = inputs['Cb']
        fwCap = inputs['fwCap']

        # calls parameter estimation functions
        Displ = displacement(L,B,T,Cb)
        S = wettedSurf(L,B,T,Cb)
        # calls the missionFuel1 function - note that other missions could be used
        outputs['fuelWt'], outputs['MCR'], outputs['etaRun'], outputs['nStarts'] = missionFuel1FW(L, S, Displ, Cb, fwCap) # inputs in meters, meters^2, metric tonnes, unitless, megajoules

# debugging code, verifies that inputs, outputs, and calculations are working properly within the component
if __name__ == "__main__":
    #define the model
    model = om.Group()
    #setup independent variables, will be chosen
    #units defined within OpenMDAO for completeness
    ivc = om.IndepVarComp()
    ivc.add_output('L', 35.8, units='m') #meters
    ivc.add_output('B', 6.08, units='m') #meters
    ivc.add_output('T', 2.85, units='m') #meters
    ivc.add_output('Cb', 0.42) #unitless
    ivc.add_output('fwCap', 782, units='MJ') #megajoules

    #define subsystems to reference variables
    model.add_subsystem('des_vars', ivc)
    model.add_subsystem('fuel_comp', Fuel())

    #connect variables
    model.connect('des_vars.L', 'fuel_comp.L')
    model.connect('des_vars.B', 'fuel_comp.B')
    model.connect('des_vars.T', 'fuel_comp.T')
    model.connect('des_vars.Cb', 'fuel_comp.Cb')
    model.connect('des_vars.fwCap', 'fuel_comp.fwCap')


    #setup problem and run with initial definitions
    prob = om.Problem(model)
    prob.setup()
    prob.run_model()
    print("Fuel Weight: " + str(prob['fuel_comp.fuelWt']))
    print("Max MCR: " + str(prob['fuel_comp.MCR']))
    print("Runtime Frac: " + str(prob['fuel_comp.etaRun']))
    print("Number of Starts: " + str(prob['fuel_comp.nStarts']))

    # #change definitions and rerun
    # prob['des_vars.Cb'] = 0.5
    # prob['des_vars.T'] = 2.5
    # prob['des_vars.L'] = 45
    # prob['des_vars.B'] = 70
    # prob.run_model()
    # print(prob['wts_comp.Wt'])
