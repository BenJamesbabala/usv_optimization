# Fuel.py - modified based on http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html
# Estimation of vessel's fuel weight as a function of parameters

# package, function, and class imports
from __future__ import division, print_function
import openmdao.api as om
import math
from fuelEstimate import missionFuel1, missionFuel1FW
from estParam import wettedSurf, displacement

# the definition of the Fuel component
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
