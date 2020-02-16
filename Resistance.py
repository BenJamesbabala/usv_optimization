from __future__ import division, print_function
import openmdao.api as om
import math

class Resistance(om.ExplicitComponent):
    """
    Evaluates the hull resistance using Series 64 model test data
    """
    
    def setup(self) :
        #setup inputs or variables needed for function
        self.add_input('L', val=0.0)
        self.add_input('S', val=0.0)
        self.add_input('Delta', val=0.0)
        self.add_input('Cb', val=0.0)
        self.add_input('Vk', val=0.0)

        self.add_output('R', val=0.0)

        # Finite difference all partials.
        self.declare_partials('*', '*', method='fd')
    
    def compute(self, inputs, outputs) :
        #inputs
        L = inputs['L']
        S = inputs['S']
        Delta = inputs['Delta']
        Cb = inputs['Cb']
        Vk = inputs['Vk']

        #constants
        rho = 1026.0 #kg/m^3
        g = 9.81 #m/s^2
        
        #conversion
        V = Vk/1.944 #m/s
        Fn = V/math.sqrt(g*L) #unitless
        D3 = math.pow(Delta,(1/3)) #meters
        
        #set up equation for C_R
        if Cb < 0.3:
            #print("Block too low")
            a, n = 0, 0
        elif Cb < 0.4 and Cb >= 0.3 :
            if Fn < 0.35:
                a, n = 0, 0
                #print("invalid Froude Number")
            elif Fn < 0.45 and Fn >= 0.35 :
                a, n = 288, -2.33
            elif Fn < 0.55 and Fn >= 0.45 :
                a, n = 751, -2.76
            elif Fn < 0.65 and Fn >= 0.55 :
                a, n = 758, -2.81
            elif Fn < 0.75 and Fn >= 0.65 :
                a, n = 279, -2.42
            elif Fn < 0.85 and Fn >= 0.75 :
                a, n = 106, -2.06
            elif Fn < 0.95 and Fn >= 0.85 :
                a, n = 47, -1.74
            elif Fn < 1.05 and Fn >= 0.95 :
                a, n = 25, -1.50
            else:
                a,n = 0,0
                #print("invalid Froude Number")
        elif Cb < 0.5 and Cb >= 0.4 :
            if Fn < 0.35:
                a, n = 0, 0
                #print("invalid Froude Number")
            elif Fn < 0.45 and Fn >= 0.35 :
                a, n = 36726, -4.41
            elif Fn < 0.55 and Fn >= 0.45 :
                a, n = 55159, -4.61
            elif Fn < 0.65 and Fn >= 0.55 :
                a, n = 42184, -4.56
            elif Fn < 0.75 and Fn >= 0.65 :
                a, n = 29257, -4.47
            elif Fn < 0.85 and Fn >= 0.75 :
                a, n = 27130, -4.51
            elif Fn < 0.95 and Fn >= 0.85 :
                a, n = 20657, -4.46
            elif Fn < 1.05 and Fn >= 0.95 :
                a, n = 11644, -4.24
            else:
                a,n = 0,0
                #print("invalid Froude Number")
        elif Cb < 0.6 and Cb >= 0.5 :
            if Fn < 0.35:
                a, n = 0, 0
                #print("invalid Froude Number")
            elif Fn < 0.45 and Fn >= 0.35 :
                a, n = 926, -2.74
            elif Fn < 0.55 and Fn >= 0.45 :
                a, n = 1775, -3.05
            elif Fn < 0.65 and Fn >= 0.55 :
                a, n = 1642, -3.08
            elif Fn < 0.75 and Fn >= 0.65 :
                a, n = 1106, -2.98
            elif Fn < 0.85 and Fn >= 0.75 :
                a, n = 783, -2.90
            elif Fn < 0.95 and Fn >= 0.85 :
                a, n = 458, -2.73
            elif Fn < 1.05 and Fn >= 0.95 :
                a, n = 199, -2.38
            else:
                a,n = 0,0
                #print("invalid Froude Number")
        else:
            #print("Block too high")
            a, n = 0, 0
            
        #estimate C_R
        C = (a*(math.pow((L/D3),n)))/1000 #unitless
        
        #checks
        #print("C_R: ", round(C,5), " - ")
        #print("S: ",round(S,2), " m^2 ")
        #print("V: ",round(V,3), " m/s ")
        #print("Fn: ",round(Fn,4), " - ")
        
        #calulate and return R
        outputs['R'] = C*(0.5)*rho*S*V*V #newtons

if __name__ == "__main__":
    #define the model
    model = om.Group()
    #setup independent variables, will be chosen
    ivc = om.IndepVarComp()
    ivc.add_output('L', 30) #meters
    ivc.add_output('S', 400) #meters^2
    ivc.add_output('Delta', 650) #metric tonnes
    ivc.add_output('Cb', 0.45) #unitless
    ivc.add_output('Vk', 16) #knots
    #define subsystems to reference variables
    model.add_subsystem('des_vars', ivc)
    model.add_subsystem('resist_comp', Resistance())

    #connect variables
    model.connect('des_vars.L', 'resist_comp.L')
    model.connect('des_vars.S', 'resist_comp.S')
    model.connect('des_vars.Delta', 'resist_comp.Delta')
    model.connect('des_vars.Cb', 'resist_comp.Cb')
    model.connect('des_vars.Vk', 'resist_comp.Vk')
    
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
    prob['des_vars.Vk'] = 16
    prob.run_model()
    print(prob['resist_comp.R'])

    
    
    
    