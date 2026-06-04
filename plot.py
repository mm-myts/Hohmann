import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

R_EARTH = 6371  # km

def plot_orbit(ax, radius_km, color, label, linestyle='-', lw=2.0, alpha=1.0):
    theta = np.linspace(0, 2 * np.pi, 500)
    x = radius_km * np.cos(theta)
    y = radius_km * np.sin(theta)
    ax.plot(x, y, color=color, linestyle=linestyle, lw=lw, alpha=alpha, label=label)

def plot_transfer(ax, r1, r2, color=None, label='Transfer orbit'):
    color = color or '#ff7c3a'
    a = (r1 + r2) / 2
    e = (r2 - r1) / (r2 + r1)
    theta = np.linspace(0, np.pi, 300)
    x = a * np.cos(theta) - a * e
    y = a * np.sqrt(1 - e**2) * np.sin(theta)
    ax.plot(x, y, color=color, linestyle='--', lw=2.0, label=label)

