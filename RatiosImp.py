# package, function, and class imports
from __future__ import division, print_function
import openmdao.api as om
import math
from RatioWeights import RatioWeights
from weightCurves import grubisicWts #modify this if using a different weight estimation


# the definition of the Ratios IMPLICIT component, based on residuals

class RatiosImp(om.ImplicitComponent):
    """Computes dimensions of roughly balanced vessel based on dimensionless ratios."""

    def setup(self):
        self.add_input('LB') #unitless
        self.add_input('BT') #unitless
        self.add_input('TL') #unitless
        self.add_input('Cb')  #unitless

        self.add_output('L', units='m', lower=19, upper=51)
        self.add_output('B', units='m', lower=2, upper=12)
        self.add_output('T', units='m', lower=1, upper=5)
        self.add_output('Excess', units='t')
        self.add_output('err1')
        self.add_output('err2')
        self.add_output('err3')

        self.declare_partials(of='*', wrt='*')

    def apply_nonlinear(self, inputs, outputs, residuals):
        LB = inputs['LB']
        BT = inputs['BT']
        TL = inputs['TL']
        Cb = inputs['Cb']

        L = outputs['L']
        B = outputs['B']
        T = outputs['T']

        rho = 1.026 # t/m^3
        Wt = grubisicWts(Cb, T, L, B, 1000, 16)
        Displ = (L*B*T*Cb*rho)

        residuals['Excess'] = (Wt-Displ)
        # residuals['err1'] = ((L/B)-LB)
        # residuals['err2'] = ((B/T)-BT)
        # residuals['err3'] = ((T/L)-TL)
        # residuals['Excess'] = grubisicWts(Cb, T, L, B, 1000, 16) - (L*B*T*Cb*rho)
        #residuals['Excess'] = (Cb*rho*(L*B*T)*(LB*BT*TL)) - grubisicWts(Cb, T, L, B, 1000, 16)

    def solve_nonlinear(self, inputs, outputs):
        LB = inputs['LB']
        BT = inputs['BT']
        TL = inputs['TL']
        Cb = inputs['Cb']

        L = outputs['L']
        B = outputs['B']
        T = outputs['T']

        rho = 1.026 # t/m^3
        Wt = grubisicWts(Cb, T, L, B, 1000, 16)
        Displ = (L*B*T*Cb*rho)

        outputs['Excess'] = (Cb*rho*(L*B*T)*(LB*BT*TL)) - grubisicWts(Cb, T, L, B, 1000, 16)



prob = om.Problem()
model = prob.model

model.add_subsystem('ratio_comp', RatiosImp())

newton = model.nonlinear_solver = om.NewtonSolver(solve_subsystems=False)
newton.options['maxiter'] = 50
model.linear_solver = om.ScipyKrylov()

#setup problem and run with initial definitions
prob.setup()
prob['ratio_comp.LB'] = 4.0
prob['ratio_comp.BT'] = 2.0
prob['ratio_comp.TL'] = 0.15
prob['ratio_comp.Cb'] = .40
prob.run_model()
print("-- L/B = 4.0, B/T = 2.0, T/L =0.15, Cb = 0.40 --")
print("Excess = ", prob['ratio_comp.Excess'])
print("err1 = ", prob['ratio_comp.err1'])
print("L = ", prob['ratio_comp.L'])
print("B = ", prob['ratio_comp.B'])
print("T = ", prob['ratio_comp.T'])
print("Cb = ", prob['ratio_comp.Cb'])


#change definitions and rerun
prob['ratio_comp.LB'] = 3
prob['ratio_comp.BT'] = 2.5
prob['ratio_comp.TL'] = 0.15
prob['ratio_comp.Cb'] = .39
prob.run_model()
print("-- L/B = 3.0, B/T = 2.5, T/L =0.15, Cb = 0.39 --")
print("L = ", prob['ratio_comp.L'])
print("B = ", prob['ratio_comp.B'])
print("T = ", prob['ratio_comp.T'])
print("Cb = ", prob['ratio_comp.Cb'])
