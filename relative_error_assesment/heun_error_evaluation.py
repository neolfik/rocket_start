import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib.pyplot as plt

# Adds parent folder to path so that you can use files from it
import sys
import os
sys.path.append(os.path.abspath(".."))

# Imports necessary functions and constants
from equation_constants import tm
from solving.analytical_solution import compute_a
from solving.heun import Heun



# Computes analytical solution for reference
def analytical(t):
    return compute_a(t);

# Calculates the final value of analytical solution
hf = analytical(tm)

# Defines log10 of final relative error
def global_error(v):
    return np.log10(abs(v-hf)/hf);

# Finds a relative error based on gamma and number of steps
def Heun_n_g(n,g):
    h,_ = Heun(n,g)
    return global_error(h[-1])


# Define the interval of steps and gamma at which to evaluate the relative error be cautious when increasing the size of NN and G since the 
## time needed for this calculation increases very fast, much faster than lineary, and if you increase G too much you will reach Maximum
## number of threads for concurent future library, in that case you will need to start batchin the G interval, if you want to try this
## long calculation make the batch implementation and test it beforehead, since if you need to use it you will need to wait for several tens 
## of minutes from my estimation
NN = np.arange(5, 506)
G = np.linspace(0,0.999,500)

# Define the map for the errors by the lenght of NN an G
map_error = np.zeros((len(NN), len(G)))

# Loop through each value of NN to calculate the errors for all G values
for i, n in enumerate(NN):
    # For each n define a array to which add the errors in order
    ner = []

    # Split the tasks
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(Heun_n_g, n, g) for g in G]

        # Collect the results as they complete into ner array
        for future in as_completed(futures):
            ner.append(future.result())

    # Convert ner list to a NumPy array and assign it to corresponding map_error row
    map_error[i, :] = np.array(ner)

    # Print the number of steps for which the calculation was completed
    print("Added result for ", n, " steps")

# Create a meshgrid for plotting
NN_grid, G_grid = np.meshgrid(NN, G, indexing="ij")

# Plot the results
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(NN_grid, G_grid, map_error, cmap="viridis")

# Add labels
ax.set_xlabel(r'$N$')
ax.set_ylabel(r'$\gamma$')
ax.set_zlabel(r'$\ln{r}$')

# Find the maximum value in map_error and its index
max_error = map_error.max()
max_index = np.unravel_index(map_error.argmax(), map_error.shape)  # Get the 2D index

# Use the index to find the corresponding values in NN and G
max_NN_value = NN[max_index[0]]
max_G_value = G[max_index[1]]

print("Maximum global error:", 10**max_error)
print("Value of NN for maximum global error:", max_NN_value)
print("Value of G for maximum global error:", max_G_value)

# Find the minimum value in map_error and its index
min_error = map_error.min()
min_index = np.unravel_index(map_error.argmin(), map_error.shape)  # Get the 2D index

# Use the index to find the corresponding values in NN and G
min_NN_value = NN[min_index[0]]
min_G_value = G[min_index[1]]

print("Minimum global error:", 10**min_error)
print("Value of NN for minimum global error:", min_NN_value)
print("Value of G for minimum global error:", min_G_value)

# Write results to the file `minimize_heun.dat`
with open("minimize_heun.dat", "a") as file:
    file.write(f"{NN[0]}\t{NN[-1]}\t{len(NN)}\t{G[0]}\t{G[-1]}\t{len(G)}\t{10**min_error}\t{min_NN_value}\t{min_G_value}\t{10**max_error}\t{max_NN_value}\t{max_G_value}\n")

# Define the filename with size included
filename = f"map_N_{NN[0]}-{NN[-1]}_gamma_0-0.999_num_{len(G)}.csv"

# Save the array to a CSV file
np.savetxt(filename, map_error, delimiter=",", fmt='%.5f')

plt.show()

# Make a 2D slice of previous graph at the minimal and maximal values for both gamma and number of steps
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# For constant number of steps
ax1.plot(G, map_error[max_index[0], :], label=r'$N_{max}$='+f'{NN[max_index[0]]}', color='Blue')
ax1.plot(G, map_error[min_index[0], :], label=r'$N_{min}$='+f'{NN[min_index[0]]}', color='Red')
ax1.set_xlabel(r'$\gamma$')
ax1.set_ylabel(r'$\log{r}$')
ax1.set_title(r'Řez podle počtu kroků pro maximální a minimální relativní chybu')
ax1.legend()

# For constant gamma
ax2.plot(NN, map_error[:, max_index[1]], label=r'$\gamma_{max}$='+f'{G[max_index[1]]:.2f}', color='Blue')
ax2.plot(NN, map_error[:, min_index[1]], label=r'$\gamma_{min}$='+f'{G[min_index[1]]:.2f}', color='Red')
ax2.set_xlabel(r'$N$')
ax2.set_ylabel(r'$\log{r}$')
ax2.set_title(r'Řez podle $\gamma$ pro maximální a minimální relativní chybu')
ax2.legend()

plt.tight_layout()
plt.show()
