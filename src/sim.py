#  ~~~ IMPORTS & CONSTANTS 
import numpy as np
import matplotlib.pyplot as plt

G = 9.81

#  ~~~ THE PHYSICS: derivatives  ~~~
def derivatives(state, t):

    x, y, vx, vy = state
    # unpacks array [state] into 4 variables x= distance on x axis, y= distance on y axis, and then velocity of each is vx and vy

    dxdt = vx
    dydt = vy
    # position changes at rate of velocity
    # velocity is rate distance changes - same as dxdt and dydt

    dvxdt = 0
    dvydt = -G
# set to 0 - no horizontal force and therefore no accelleration, and no external forces e.g. drag so only -G acting "vacuum"
   

    return np.array([dxdt, dydt, dvxdt, dvydt])

# returns the rates in the same order as the state [x, y, vx, vy] - important as 'state + dt*rates' adds element by elememt

#  ~~~ THE INTEGRATOR  ~~~
def step_euler(f, state, t, dt):
    # advances state forwards by a small time step (dt)

    rates = f(state, t)
    # asks function for rates at current state

    return state + dt * rates
# new state = old state + (rate x time step)
# only an approximation - as step_euler assumes rates stay constant over dt 

def run_sim(v0, theta_deg, dt):
    theta = np.radians(theta_deg)   # convert deg to rad ONCE
    
    state =np.array([0, 0, v0 * np.cos(theta), v0 * np.sin(theta)])
    t=0
    
    states = [state]
    
    
    while state[1] >= 0:
        previous_state = state
        # remember the state BEFORE stepping. when loop ends, last step has overshot below ground, we need step before to interpolate exact landing spot

        state = step_euler(derivatives, state, t, dt)
        states.append(state)
        
        
        t += dt
        # advance the state by dt, advance the clock by dt 


    #  ~~~ LANDING POINT: interpolation  ~~~
    # since loop ends 1 step AFTER crossing y=0, last step is underground. we estimate between the last 2 points the path crosses y=0
    
    y_prev = previous_state[1]  #height just before crossing(+ve)
    y_last = state[1] # height just after crossing (-ve)
    
    fraction = y_prev / (y_prev - y_last)
    # how far along the last step (0 to 1) the path crossed y=0
    
    x_prev = previous_state[0]
    x_last = state[0]
    # x just before and after the crossing 
    
    x_landing = x_prev + fraction * (x_last - x_prev)
    # go 'fraction' of the way from x_prev to x_last

    return x_landing, np.array(states)

#  ~~~ VALIDATION  ~~~
v0 = 100
theta_deg = 45
dt = 0.01


x_landing, states = run_sim(v0, theta_deg, dt)

print("--- Stage 1 validation ---")
print("Landing x = ", x_landing)
theta_rad = np.radians(theta_deg)

R_analytic = v0**2 * np.sin(2 * theta_rad) / G
# the textbook range formula for a projectile on flat ground, no drag (suvat)


print("Analytic range =", R_analytic)

error = abs((x_landing - R_analytic) / R_analytic) * 100
print("Error =", error, "%")
# percentagedifference between simulate and exact range 

#  ~~~ CONVERGANCE SWEEP  ~~~

dts = np.logspace(-4, -1, 10)

errors = []

for dt_i in dts:
    x_land, _ = run_sim(v0, theta_deg, dt_i)
    err = abs(x_land - R_analytic)
    errors.append(err)
    
errors= np.array(errors)


plt.loglog(dts, errors, "o-")
plt.xlabel("Time step dt (s)")
plt.ylabel("Landing error (m)")
plt.title("Vacuum flight: Euler landing error vs dt")
plt.grid(True)
plt.savefig("/Users/anatolekacar/Documents/GitHub/missle-mk-i/docs/convergence.png", dpi=200)
plt.show()

slope, intercept =  np.polyfit(np.log10(dts), np.log10(errors), 1)
print("--- dt convergence ---")
print("slope =",slope)
    
# Takeaway: error ≈ vx·dt, so it’s directly proportional to dt. Halve dt, halve the error. That’s what “first-order” means, and it’s what your dt sweep should show.

# ~~~  PLOT  ~~~
plt.plot(states[:, 0], states[:, 1])
# plots all rows of collumn 0 (x) against all rows of collumn 1 (y)

plt.xlabel("Horizontal distance (m)")
plt.ylabel("Height (m)")
plt.title("Vacuum flight (Euler, dt = 0.01 s)")
plt.axis("equal")
plt.savefig("/Users/anatolekacar/Documents/GitHub/missle-mk-i/docs/flight_path.png", dpi=200)
plt.show()