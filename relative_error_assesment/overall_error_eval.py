import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib.pyplot as plt

# Adds parent folder to path so that you can use files from it
import sys
import os
sys.path.append(os.path.abspath(".."))

# Import necessary functions and constants from the project
from equation_constants import tm
from solving.analytical_solution import compute_a
from solving.numerical_solution import LSODA, Runge_kutta_45, BDF
from solving.heun import Heun





# Get the analytical solution for comparison
def analytical(t):
    return compute_a(t);

# Calculate the final height
hf = analytical(tm)

# Define a relative error of the last point compared to precise analytical solution hf in logarithmic form for better representation
def global_error(v):
    return np.log10(abs(v-hf)/hf);

# Define function that for each method and number of steps n returns the log10 of final relative error
def evaluate_methods(n):
    # Get the solution from LSODA, Runge-Kutta 45, and Euler
    l, _ = LSODA(n)
    rk, _ = Runge_kutta_45(n)
    eu, _ = BDF(n)
    h, _ = Heun(n,0.67)
    
    # Calculate log10 of relative error for each method, we take only the last member of the numerical solution
    l_error = global_error(l[-1,1])
    rk_error = global_error(rk.y[1,-1])
    eu_error = global_error(eu.y[1,-1])
    h_error = global_error(h[-1])
    
    return l_error, rk_error, eu_error, h_error;

# Define number of steps range be mindful when chosing the range this calculation will get lineary longer with size of NN, for big sizes of
## NN you will also reach the limit of threads for concurent futures and will need to implement batching to asses the interval in sections
NN = np.arange(5, 501)

# Initialize lists for storing errors
lerrors = []
rkerrors = []
euerrors = []
herrors = []

# Use ThreadPoolExecutor to evaluate each method concurrently, this is used to effectively use multiple cores for this potentially
## complicated calculation
with ThreadPoolExecutor() as executor:
    # Submit tasks for LSODA, Runge-Kutta 45, and Euler
    futures = [executor.submit(evaluate_methods, n) for n in NN]
    
    # Add error values to prepared lists in order of NN and print the added result so that user knows somthing is happening
    for n, future in zip(NN, as_completed(futures)):
        l_error, rk_error, eu_error, h_error = future.result()
        lerrors.append(l_error)
        rkerrors.append(rk_error)
        euerrors.append(eu_error)
        herrors.append(h_error)
        print(f"Added result for {n} steps")


# Plot the log10 of final relative errors for each method
plt.figure(figsize=(12, 8))
plt.plot(NN, lerrors, label= 'LSODA')
plt.plot(NN, rkerrors, label= 'Runge-Kutta 4/5')
plt.plot(NN, euerrors, label= 'BDF', color = 'Red')
plt.plot(NN, herrors, label = 'Heun', color = 'Grey')

# Add labels and shows plot with legend
plt.xlabel(r'$N$')
plt.ylabel(r'$\log{r}$')
plt.legend()
plt.show()
