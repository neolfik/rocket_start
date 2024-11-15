This folder contains the full code necessary to solve problem of rocket start in one dimension and in a homogeneous gravitational field analytically and numerically using purely python.


Constants and problem instructions

The constants needed for the analytical and numerical solution are in file equation_constants.py. There is also a parameter scale that scales the results to accommodate different units, if you change it you need to change the labeling of y axis of the solution graph in rocket_start.py when plotting the solution.


Finding the solution

The function you need to call for solving the system is rocket_start.py. It contains the final usage of methods defined in folder ./solving/, if you don't change the scale there should be no need to change the program for successful solution. In this file all numerical methods used from pythons libraries, LSODA, Euler(BDF) and Runge-Kutta 4(5), are called with a parameter, that is number of steps you want the function to take, be aware that all listed methods are adaptive so they will most likely internally alter the number of steps they take. Lastly custom version of Heun method is called it has two parameters and that are in order number of steps and a weight coefficient in interval [0,1), one is excluded because of the nature of the computation. The weight coefficient can be out of the defined interval, called function will try to interpret it so that the coefficient falls into designated interval, but it may not have the intended value. The reason the coefficient is used so that you can alter the weight of Euler approximation and subsequent approximation of step in the analyzed function. This has value only because we can determine the optimal value of gamma when compared to analytical solution easily.


Folder ./solving/

This folder contains all function necessary for both analytical and numerical solution of the problem.

In file analytical_solution.py there is solution of the problem using solely python that return a function of constants into which it automatically substitutes from equation_constants.py and finally return analytical solution of the problem dependent only on time.

In file numerical_solution.py numerical methods from python libraries are called in a specific way that returns solution and respective time interval with steps for more convenient plotting, the only necessary parameter is number of steps the function should use. It is made to solve solely this problem with defined constants in equation_constants.py.

In file heun.py is a custom Heun method dependent on number of steps it needs to take and a weight coefficient discussed above and in the respective file.


Folder ./relative_error_assesment/

In this folder are files that are not called by the rocket_start.py and you need to call them separately. They are used to find relative error of used method compared to analytical solution. This can be only done because the analytical solution exist. The relative errors are plotted on a log10 scale so we can compare them easier and tha graph has a good shape.

In file overall_error_eval.py relative error of all functions dependent on the number of steps taken is calculated and then plotted. There we can see that the python libraries methods use different number of steps then number user provides, the relative error is constant. But we can at least compare the custom Heun method to the python library ones. For 4 steps there seems to be some internal error or bug in the code since it returns relative error of 1 from the python libraries methods. 

In file heun_error_evaluation.py relative error of custom Heun function is computed for a plane of points for number of steps and coefficient gamma, the calculation is rather time consuming in order to get satisfactory result so be aware of that. The program then plots the 3D graph of relative error and finds the lowest value of error and the respective number of steps and coefficient gamma. In this part for the used constants the minimum occurs for a reasonable amount of steps, (0,250) to lower the time consumed, at 174 steps. This happens because of inner rounding since the numbers are relatively small and because of randomness of the method, if we disregard this abnormality the minimum occurs for the biggest number of steps and a specific value of gamma that is around 0.67 for the used constants. The minimum at 174 can possibly occur at different place based on machine used, this speculation was not confirmed and if the minimum point is mentioned in the calculation description it does not mean you will get the minimum for the same number of steps or that this speculation is right in the beginning. Since this calculation is rather long the main results like the minimal and maximal value of error are save in a file, if you want the graphs from matplotlib, you can display the .csv file that is saved after running the error analysis.

In minimize_heun.txt are results of heun_error_evaluation.py run previously, the format of the file is not great but saves previously computed values for comparison, since the values can differ a little even if you run the program multiple times with same initial parameters.


Folder ./project_figures/

In this folder are graphs used in the final report and are computed for higher number of steps in error assessment so you can pull them up and don't need to run the error assessment itself

The only .pdf file contains the summary of the solution of this problem and theory of the used methods.
