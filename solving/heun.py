import numpy as np

# Adds parent folder to path so that you can use files from it
import sys
import os
sys.path.append(os.path.abspath(".."))

# Import constants from problem instructions
from equation_constants import tm, f, mi, r, g, h0






# System of differential equations for Heun
def sys(h, t):
    # h[0] is velocity, h[1] is height and t is variable
    return [f / (mi - r * t) - g, h[0]];

# Custom function using heun method for solving, number of steps and gamma parameter are needed, the gamma parameter will be explained later
def Heun(N,gam):
    # The gamma parameter must be between 0 and 1, without 1, this part of the code rounds gamma to needed interval in case of it being 
    ## out of required interval 0 to 1
    if gam>=1:
        print("Coefficient bigger than one")
        order = int(np.floor(np.log(gam)))
        gam = gam/(10**(order+1))
        print("     Coefficient interpreted as: ", gam)
    elif gam<0:
        print("Coefficient lower than zero")
        order = int(np.floor(np.log(abs(gam))))
        gam = - gam / (10**(order + 1))
        print("     Coefficient interpreted as: ", gam)
    

    # Define the time interval and steps for the method
    t = np.linspace(0,tm,N)
    
    # Change the format of initial conditions 
    x0 = np.array(h0)

    # Get dimensions of expected result from initial conditions and time interval with steps
    N=x0.shape[0]
    Nt=t.shape[0]
    
    # Define a matrix to store results based on previoustly determined shape
    x=np.zeros((Nt,N))

    # Setting the first row of result to initial conditions
    x[0,:]=x0

    # This part will be dedicated to brief description of gamma
    ## Gamma determines the weight this Heun method gives to the usual Euler step k1 and approximation step later denoted as k2, the sum of
    ### weight of k1 and k2 must be equal to one. The weight that this particular function uses determines weight of Euler step k1.
    ### The weight of k2 is then b = 1 - gam.
    ## In second approximation k2 there are additionally two parameters A and B that make the difference compared to usual Euler step k1,
    ### those parameters must be the same and are equal 1/(2*(1-gam))
    # All those parameters and their derivation is desribed in the report file for the whole problem. 
    a = 1/(2*(1-gam))
    b = 1-gam

    # Adds next values of the solution into x matrix
    for j in range(Nt-1):
        # Computes the size of time interval in case the stepping is not homogeneous
        h=t[j+1]-t[j]
        # Computes the usual Euler step based on the defined system sys(x,t)
        k1=h*np.array(sys(x[j,:],t[j]))
        # Computes the second approximation with the coefficients based on gamma
        k2=h*np.array(sys(x[j,:]+a*k1,t[j]+a*h))
        # Adds together k1 and k2 in respect to their weight gam and 1-gam and saves it in new line of the result matrix x
        x[j+1,:]=x[j,:]+gam*k1+b*k2
    # Returns the final solution for height, ignoring velocity, and time interval with steps used for evaluation. If you need the velocity
    ## change the return value to x but be aware that it will break few other parts of the code you will need to correct afterwards
    return x[:,1], t;


