import numpy as np
from scipy.integrate import odeint, solve_ivp

# Adds parent folder to path so that you can use files from it
import sys
import os
sys.path.append(os.path.abspath(".."))

# Import the constants from the problem instructions
from equation_constants import mi, r, f, g, tm, h0




# System of differential equations for LSODA method
def ode_sys_ls(h, t):
    # h[0] is velocity, h[1] is height and t is variable
    return [f / (mi - r * t) - g, h[0]];

# System of differential equations for Runge-Kutta 4(5) method
def ode_sys(t, h):
    # h[0] is velocity, h[1] is height and t is variable
    return [f / (mi - r * t) - g, h[0]];

# Solve differential equation numerically using LSODA method from scipy.integrate.odeint
def LSODA(step):
    # Changing initial conditions format
    H0 = np.array(h0)

    # Defining time interval with steps for the method
    t = np.linspace(0.0, tm, step)
    
    # Solve system
    return odeint(ode_sys_ls, H0, t), t;

# Solve differential equation numerically using Runge-Kutta 4(5) from solve_ivp, it uses RK5 but estimates the uncertainty with RK4
def Runge_kutta_45(step):
    # Time interval for evaluation with steps
    t = np.linspace(0, tm, step)

    # Solve the system
    return solve_ivp(ode_sys, [0, tm], h0, method='RK45', t_eval=t),t;

# Solve differential equation numerically using BDF method, from solve_ivp
def BDF(step):
    # Time interval for evaluation with steps
    t = np.linspace(0, tm, step)

    # Solve the system
    return solve_ivp(ode_sys, [0, tm], h0, method='BDF', t_eval=t),t;

