import numpy as np
import matplotlib.pyplot as plt

# Import functions used to calculate the solution
from equation_constants import scale, tm
from solving.analytical_solution import compute_a
from solving.numerical_solution import LSODA, Runge_kutta_45, BDF
from solving.heun import Heun




# Compute analytical solution purely dependent on time and assign it to a function
def analytical(t):
    return compute_a(t);

# Calculate the maximum height for comparison
hmax = analytical(tm)

# Get the solution data from python packages using number of steps, that is automatically tinkered by the method so the input step number
## doesn't need to correspond to the actual number of steps the function took
h, tn = LSODA(100)
rk, t_rk = Runge_kutta_45(100)
b, t_b = BDF(100)

# Get the solution from custom version of Heun method using number of steps and a value gamma that tinkers with the distribution of Heun
## method solving, where 1 means Euler method, but the way of calculating does not allow one so we will not be able to use 1 as value of
## gamma, and 0 coresponds to a method that entirely depends on second approximation for next value and completely disregerds 
## Euler method step 
# For better understanding look into the solving/heun.py file where the method is explained on the code itself, for complete mathematic 
## derivation look into the report file for the whole problem
# The gamma value used is 0.67, the value was determined in relative_error_assesment to achieve the smallest possible relative error
## in comparison to the analytical solution, the used number of steps 27 is small, again this was computed in relative_error_assesment
## as the optimal number of steps for this problem and initial conditions up till 70 steps, it is most likely a side effect of machine 
## rounding so it may vary from machine to machine so it is advised to run relative_error_assesment/heun_error_evaluation.py to determine 
## the best function parameters. If the number is different it means another error evaluation was made for higher number of steps.
heun, t_heun = Heun(174,0.7)


# Make a array for time at which the analytical solution will be evaluated 
t = np.linspace(0.0, tm, 1000)

# Make a list of analytical solution values for previously made time array, scaling for analytical solution is done here because
## of the analyt variable type
analyt = []
for i in t:
    analyt.append(analytical(i)/scale)


# Plot the results of numerical solutions and analytical solution, if the plot is not to your liking you can change scaling of the height
## initially it is set so that heinght is measured in kilometers, if necessary change the value of scale in equation_constants.py
plt.plot(t_heun, heun/scale, label = 'Heun')
plt.plot(t_rk, rk.y[1]/scale, 'r', label='Runge-Kutta 45')
plt.plot(t_b, b.y[1]/scale, 'r', label='BDF')
plt.plot(tn, h[:,1]/scale,color = "Blue", label = r'LSODA')

# Plot the analytical solution
plt.plot(t, analyt, '--', color = "Black", label='Analytical Solution')

# Plot a height reached at the end of the burn for comparison
plt.plot(t, [hmax / scale] * len(t), '-.',color = "Green", label='Max Height')

# Label the axes, the y axis is initially set to kilometers, if you change the scale value you should slter the y axis label too
plt.xlabel(r"$t\,[s]$")
plt.ylabel(r"$h\,[km]$")
plt.legend()
plt.show()
