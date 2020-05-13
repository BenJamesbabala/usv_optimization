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
        self.add_input('L', val=0.0, units='m')
        self.add_input('B', val=0.0, units='m')
        self.add_input('T', val=0.0, units='m')
        self.add_input('Cb', val=0.0)
        self.add_input('fwCap', val=0.001, units='MJ') #unit is megajoules, val set to 0.001 to avoid divide by zero

        self.add_output('fuel', val=0.0, units='t')
        self.add_output('MCR', val=0.0, units='kW')
        self.add_output('etaRun', val=0.0)
        self.add_output('nStarts', val=0.0)

        # Finite difference all partials.
        self.declare_partials('*', '*', method='fd')


    def compute(self, inputs, outputs) :
        #inputs
        L = inputs['L']
        B = inputs['B']
        T = inputs['T']
        Cb = inputs['Cb']
        fwCap = inputs['fwCap']

        # calls paramter estimation functions
        Displ = displacement(L,B,T,Cb)
        S = wettedSurf(L,B,T,Cb)
        # calls the missionFuel1 function - note that other missions could be used
        outputs['fuel'], outputs['MCR'], outputs['etaRun'], outputs['nStarts'] = missionFuel1FW(L, S, Displ, Cb, fwCap) # inputs in meters, meters^2, metric tonnes, unitless, megajoules
