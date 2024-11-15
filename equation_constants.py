## Defining equation constants form the problem instructions
# Initial rocket weight in kilograms
mi = 12.8e3
# Final rocket weight (without fuel and oxydizer) in kilograms
mf = 4e3
# Rate of fuel consumprion in kilograms per second
r = 0.130e3
# Generated thrust force in newtons
f = 2.5e5
# Gravitational acceleration in meters per second
g = 9.81
# Scaling constant for the results, 1 for meters 1000 for kilometers etc.
scale = 1000
# Burn duration
tm = (mi-mf)/r
# Initial state of system in order velocity and position
h0 = [0,0]
