import scipy.constants as const
from math import sqrt

from plot import *

massPB = 5.97216787e24

# PRIMARY BODY

initial_altitude = float(input("Starting altitude (km): "))
initial_radius = initial_altitude*1000 + R_EARTH*1000

# DESTINATION BODY

final_altitude = float(input("Final altitude (km): "))
final_radius = final_altitude*1000 + R_EARTH*1000

# HOHMANN TRANSFER TIME

HTT = sqrt(((4*const.pi**2)/(const.G * massPB))*((initial_radius+final_radius)/2)**3)/(2)

#ANSWER

htt = HTT

years = int(htt//(365*24*60*60))
htt -= years * (365*24*60*60)

months = int(htt//(30*24*60*60))
htt -= months * (30*24*60*60)

days = int(htt//(24*60*60))
htt -= days * (24*60*60)

hours = htt//(60*60)
htt -= hours * (60*60)

mins = round(htt/60, 2)

if years > 0:
        print("Time:", years, "years", months, "months", days, "days")
elif months > 0:
        print("Time:", months, "months", days, "days", hours, "hours")
elif days > 0:
        print("Time:", days, "days", hours, "hours", mins, "minutes")
elif hours > 1:
        print("Time:", hours, "hours", mins, "minutes")
else:
        print("Time:", mins + hours*60, "minutes")

# DELTA-V @ B1
dv1 = sqrt(2*const.G*massPB*(1/initial_radius-1/(initial_radius+final_radius))) - sqrt(const.G*massPB/initial_radius)

# DELTA-V @ B2
dv2 = sqrt(2*const.G*massPB*(1/final_radius-1/(initial_radius+final_radius))) - sqrt(const.G*massPB/final_radius)


print("Delta-v at burn 1:", round(dv1, 2))

print("Delta-v at burn 2:", round(dv2, 2))

# PLOTTING THE SPACE


# Setup 
fig, ax = plt.subplots(figsize=(8, 8))
plt.style.use('dark_background')

# Earth
earth = plt.Circle((0, 0), R_EARTH, color='deepskyblue', label='Earth')
ax.add_patch(earth)

# Orbits
r1 = initial_radius / 1000 
r2 = final_radius / 1000 

plot_orbit(r1, 'lime', f'Initial Orbit ({initial_altitude}km)')
plot_orbit(r2, 'red', f'Target Orbit ({final_altitude}km)')
plot_transfer(r1, r2)

# Burn markers
plt.plot(r1, 0, 'o', color='lime', markersize=10, label='Burn 1')
plt.plot(-r2, 0, 'o', color='red', markersize=10, label='Burn 2')

ax.set_aspect('equal')
ax.legend(loc='upper right')
plt.title('Hohmann Transfer: LEO → GEO')
plt.tight_layout()
plt.show()


