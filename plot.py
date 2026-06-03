import numpy as np
import matplotlib.pyplot as plt

R_EARTH = 6371  # km

def plot_orbit(altitude_km, color, label, linestyle='-'):
    r = altitude_km
    theta = np.linspace(0, 2 * np.pi, 500)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    plt.plot(x, y, color=color, linestyle=linestyle, label=label)

def plot_transfer(r1, r2, color='orange', label='Transfer Orbit'):
    a = (r1 + r2) / 2
    e = (r2 - r1) / (r2 + r1)
    theta = np.linspace(0, np.pi, 300)  # half ellipse only
    x = a * np.cos(theta) - a * e       # shift by focus
    y = a * np.sqrt(1 - e**2) * np.sin(theta)
    plt.plot(x, y, color=color, linestyle='--', label=label)

