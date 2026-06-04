import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

MU = 398600.4418  # km^3/s^2

def kepler_E(M, e):
    E = M.copy()
    for _ in range(50):
        dE = (M - E + e * np.sin(E)) / (1 - e * np.cos(E))
        E += dE
        if np.max(np.abs(dE)) < 1e-12:
            break
    return E

def hohmann_v(t, r1, r2, mu=398600.4418):
    a = (r1 + r2) / 2
    e = (r2 - r1) / (r1 + r2)
    T = np.pi * np.sqrt(a**3 / mu)
    t = np.clip(t, 0, T)
    M = np.pi * t / T
    E = kepler_E(M, e)
    r = a * (1 - e * np.cos(E))
    return np.sqrt(mu * (2/r - 1/a))

def v_total(t, r1, r2, mu=398600.4418):
    a  = (r1 + r2) / 2
    T  = np.pi * np.sqrt(a**3 / mu)
    v1 = np.sqrt(mu / r1)          # computed from parameters, not outer scope
    v2 = np.sqrt(mu / r2)
    t  = np.asarray(t, dtype=float)
    out = np.empty_like(t)
    out[t < 0]                    = v1
    out[(t >= 0) & (t <= T)]      = hohmann_v(t[(t >= 0) & (t <= T)], r1, r2, mu)
    out[t > T]                    = v2
    return out, T, v1, v2