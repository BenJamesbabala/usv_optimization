import math

def series64(L, S, Delta, Cb, Vk) : #inputs in meters, meters^2, metric tonnes, unitless, knots
    #constants
    rho = 1026.0 #kg/m^3
    g = 9.81 #m/s^2
    
    #conversion
    V = Vk/1.944 #m/s
    Fn = V/math.sqrt(g*L) #unitless
    D3 = math.pow(Delta,(1/3)) #meters
    
    #set up equation for C_R
    if Cb < 0.3:
        print("Block too low")
        a, n = 0, 0
    elif Cb < 0.4 and Cb >= 0.3 :
        if Fn < 0.35:
            a, n = 0, 0
            print("invalid Froude Number")
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
            print("invalid Froude Number")
    elif Cb < 0.5 and Cb >= 0.4 :
        if Fn < 0.35:
            a, n = 0, 0
            print("invalid Froude Number")
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
            print("invalid Froude Number")
    elif Cb < 0.6 and Cb >= 0.5 :
        if Fn < 0.35:
            a, n = 0, 0
            print("invalid Froude Number")
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
            print("invalid Froude Number")
    else:
        print("Block too high")
        a, n = 0, 0
        
    #estimate C_R
    C = (a*(math.pow((L/D3),n)))/1000 #unitless
    
    #checks
    print("C_R: ", round(C,5), " - ")
    print("S: ",round(S,2), " m^2 ")
    print("V: ",round(V,3), " m/s ")
    print("Fn: ",round(Fn,4), " - ")
    
    #calulate and return R
    R = C*(0.5)*rho*S*V*V #newtons
    print("R: ",round((R/1000),2)," kN ")
    return R

R = series64(30,400,650,.45,16) #inputs in meters, meters^2, metric tonnes, unitless, knots
#R = series64(40,500,800,.45,16) #inputs in meters, meters^2, metric tonnes, unitless, knots
