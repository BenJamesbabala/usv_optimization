# Reliability.py - modified based on http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html
# Combine several metrics of a design to produce a reliability score, a probability of failure (a fraction of 1)

# package, function, and class imports
from __future__ import division, print_function
import openmdao.api as om
import math

# the definition of the Reliability component
class Reliability(om.ExplicitComponent):
    """
    Evaluates the probability of failure for a mission using empirical estimates
    """

    # setup input and output variables for the component
    def setup(self) :
        self.add_input('MCR', units='kW') #kilowatts
        self.add_input('etaRun')
        self.add_input('nStarts')
        self.add_input('tMission', units='h') #hours
        self.add_input('fwCap', units='MJ') #megajoules

        self.add_output('failProb')

        # Finite difference all partials.
        self.declare_partials('*', '*', method='fd')


    def compute(self, inputs, outputs) :
        #inputs
        MCR = inputs['MCR']
        etaRun = inputs['etaRun']
        nStarts = inputs['nStarts']
        tMission = inputs['tMission']

        # engine running failure probability
        tRun = etaRun*tMission # hours
        engineMTBF = 10000 # hours
        runProb = (1/engineMTBF)*tRun

        # engine starting failure probability
        failPerStart = (1/10000)
        startProb = failPerStart*nStarts

        # FESD failure probability
        tFESD = (1-etaRun)*tMission # hours
        fesdMTBF = 10000 # hours
        fesdProb = (1/fesdMTBF)*tFESD

        # combine probabilities
        outputs['failProb'] = runProb + startProb + fesdProb;

# debugging code, verifies that inputs, outputs, and calculations are working properly within the component
if __name__ == "__main__":
    #define the model
    model = om.Group()
    #setup independent variables, will be chosen
    #units defined within OpenMDAO for completeness
    ivc = om.IndepVarComp()
    ivc.add_output('MCR', 45.14, units='kW') #kilowatts
    ivc.add_output('etaRun', 4.234) #unitless
    ivc.add_output('nStarts', 3.105) #unitless
    ivc.add_output('tMission', 0.354, units='h') #hours
    ivc.add_output('fwCap', 0.354, units='MJ') #megajoules


    #define subsystems to reference variables
    model.add_subsystem('des_vars', ivc)
    model.add_subsystem('rel_comp', Reliability())

    #connect variables
    model.connect('des_vars.MCR', 'rel_comp.MCR')
    model.connect('des_vars.etaRun', 'rel_comp.etaRun')
    model.connect('des_vars.nStarts', 'rel_comp.nStarts')
    model.connect('des_vars.tMission', 'rel_comp.tMission')
    model.connect('des_vars.fwCap', 'rel_comp.fwCap')


    #setup problem and run with initial definitions
    prob = om.Problem(model)
    prob.setup()
    prob.run_model()
    # print("Fuel Weight: " + str(prob['rel_comp.fuelWt']))
    # print("Max MCR: " + str(prob['rel_comp.MCR']))
    # print("Runtime Frac: " + str(prob['rel_comp.etaRun']))
    # print("Number of Starts: " + str(prob['rel_comp.nStarts']))

    # #change definitions and rerun
    # prob['des_vars.tMission'] = 0.5
    # prob['des_vars.nStarts'] = 2.5
    # prob['des_vars.MCR'] = 45
    # prob['des_vars.etaRun'] = 70
    # prob.run_model()
    # print(prob['wts_comp.Wt'])
