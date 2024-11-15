from sympy import symbols, Function, dsolve, Eq, Derivative, simplify, log, expand_log, pprint
from sympy.utilities.lambdify import lambdify
import numpy as np

# Adds parent folder to path so that you can use files from it
import sys
import os
sys.path.append(os.path.abspath(".."))

# Import constants from the problem instructions
from equation_constants import mi, r, f, g





# Define variables as symbols for the method
t = symbols('t')
h = Function('h')(t)
ff, mmi, rr, gg = symbols('f mi r g')

# Define the differential equation of second order
eq = Eq(Derivative(h, t, 2), ff / (mmi - rr * t) - gg)

# Solve for initial conditions x(0) = 0, x'(0) = 0 and simplify
sol = simplify(expand_log(dsolve(eq, ics={h.subs(t, 0): 0, h.diff(t).subs(t, 0): 0})))

# Substitute degenerated logarithmic that could not be simplified by sympy
log_expr = - log(-mmi) + log(-mmi+rr*t)
log_subs = log(1-rr*t/mmi)
sol = sol.subs(log_expr, log_subs)

# Print analytical solution
print("Analytical solution to the problem: ")
pprint(sol.rhs)

# Extract the right hand side of the solution as an expression and substitute for variables that we consider constant from 
## equation_constants file
rhs_substituted = simplify(sol.rhs.subs(ff, f).subs(mmi, mi).subs(rr, r).subs(gg, g).evalf())

# Convert t from symbol back to variable and analytical function to function of a variable t
compute_a = lambdify(t , rhs_substituted, modules={'numpy': {'log': np.log}})
