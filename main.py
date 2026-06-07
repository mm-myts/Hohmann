import scipy.constants as const

from plot import *
from v_graph import *

massPB = 5.97216787e24
MU = massPB * const.G

# PRIMARY BODY

initial_altitude = float(input("Starting altitude (km): "))
initial_radius = initial_altitude*1000 + R_EARTH*1000        # m

# DESTINATION BODY

final_altitude = float(input("Final altitude (km): "))
final_radius = final_altitude*1000 + R_EARTH*1000           # m

# HOHMANN TRANSFER TIME

HTT = np.sqrt(((4*const.pi**2)/(const.G * massPB))*((initial_radius+final_radius)/2)**3)/(2)


# PLOTTING THE SPACE

c_blue   = '#4a9eff'
c_orange = '#ff7c3a'
c_green  = '#3ecf8e'
c_burn   = '#ff4e4e'
c_text   = '#e0e0e0'
c_muted  = '#888888'
c_grid   = '#2a2a3a'
c_bg     = '#0f1117'
c_legend = '#1a1a2e'

# Orbits
r1 = initial_radius / 1000      # km
r2 = final_radius / 1000        # km


# --- Figure ---
fig, ax = plt.subplots(1, 2)
fig.patch.set_facecolor(c_bg)
ax[0].set_facecolor(c_bg)

# Earth — filled circle + subtle atmosphere glow ring
earth = Circle((0, 0), R_EARTH, color='#1a6fa8', zorder=3, label='Earth')
atmo  = Circle((0, 0), R_EARTH * 1.04, color='#1a6fa8', alpha=0.12, zorder=2)
ax[0].add_patch(earth)
ax[0].add_patch(atmo)

# Faint Earth grid lines (meridians/parallels feel)
for ang in np.linspace(0, np.pi, 6):
    x = R_EARTH * np.cos(ang)
    y = R_EARTH * np.sin(ang)
    ax[0].plot([x, -x], [y, -y], color='#0d4f7a', lw=0.5, alpha=0.4, zorder=4)
for r in [R_EARTH * 0.5, R_EARTH * 0.85]:
    c = Circle((0,0), r, fill=False, edgecolor='#0d4f7a', lw=0.5, alpha=0.4, zorder=4)
    ax[0].add_patch(c)

# Orbits
plot_orbit(ax[0], r1, c_blue,  f'Initial orbit  ({initial_altitude} km alt)', lw=2.0)
plot_orbit(ax[0], r2, c_green, f'Target orbit  ({final_altitude} km alt)',  lw=2.0)
plot_transfer(ax[0], r1, r2)

# Burn markers
burn1_x, burn1_y = r1, 0
burn2_x, burn2_y = -r2, 0

ax[0].plot(burn1_x, burn1_y, 'o', color=c_burn, markersize=9, zorder=6,
        markeredgecolor=c_bg, markeredgewidth=1.2, label='Burn 1  (periapsis)')
ax[0].plot(burn2_x, burn2_y, 'o', color=c_burn, markersize=9, zorder=6,
        markeredgecolor=c_bg, markeredgewidth=1.2, label='Burn 2  (apoapsis)')

# Burn labels
offset = r2 * 0.04
ax[0].text(burn1_x + offset, burn1_y + offset, 'Δv₁', color=c_burn,
        fontsize=10, fontweight='normal', va='bottom')
ax[0].text(burn2_x - offset, burn2_y + offset, 'Δv₂', color=c_burn,
        fontsize=10, fontweight='normal', va='bottom', ha='right')

# Direction arrow on transfer arc (midpoint)
a_mid = (r1 + r2) / 2
e_mid = (r2 - r1) / (r2 + r1)
th_arr = np.pi * 0.52
x_arr = a_mid * np.cos(th_arr) - a_mid * e_mid
y_arr = a_mid * np.sqrt(1 - e_mid**2) * np.sin(th_arr)
dx = -np.sin(th_arr) * r2 * 0.04
dy =  np.cos(th_arr) * np.sqrt(1 - e_mid**2) * r2 * 0.04
ax[0].annotate('', xy=(x_arr + dx, y_arr + dy), xytext=(x_arr, y_arr),
            arrowprops=dict(arrowstyle='->', color=c_orange, lw=1.8))

# "Earth" label
ax[0].text(0, 0, 'Earth', color='#a0d4f5', fontsize=9, ha='center', va='center',
        fontweight='normal', zorder=5)

# Styling
ax[0].set_aspect('equal')
lim = r2 * 1.18
ax[0].set_xlim(-lim, lim)
ax[0].set_ylim(-lim, lim)

ax[0].set_xlabel('x  (km)', color=c_text, fontsize=11, labelpad=8)
ax[0].set_ylabel('y  (km)', color=c_text, fontsize=11, labelpad=8)
ax[0].set_title('Hohmann transfer: orbital geometry', color=c_text, fontsize=13,
             fontweight='normal', pad=14)

ax[0].tick_params(colors=c_muted, labelsize=9)
for spine in ax[0].spines.values():
    spine.set_edgecolor(c_grid)
ax[0].grid(True, color=c_grid, lw=0.5, alpha=0.5, linestyle=':')

# Scale ticks to 10^4 km for readability
ax[0].ticklabel_format(style='sci', axis='both', scilimits=(4,4))
ax[0].xaxis.offsetText.set_color(c_muted)
ax[0].yaxis.offsetText.set_color(c_muted)

legend_elements = [
    Line2D([0],[0], color=c_blue,   lw=2,   label=f'Initial orbit  ({initial_altitude} km alt)'),
    Line2D([0],[0], color=c_orange, lw=2, linestyle='--', label='Transfer ellipse'),
    Line2D([0],[0], color=c_green,  lw=2,   label=f'Target orbit  ({final_altitude} km alt)'),
    Line2D([0],[0], color=c_burn,   lw=0, marker='o', markersize=7,
           markeredgecolor=c_bg, markeredgewidth=1, label='Δv burn points'),
]
ax[0].legend(handles=legend_elements, loc='upper right',
          facecolor=c_legend, edgecolor=c_grid, labelcolor=c_text, fontsize=9,
          framealpha=1.0)


# DELTA V GRAPH  — use km throughout to match v_total / hohmann_v

MU_KM = 398600.4418   # km³/s²

a   = (r1 + r2) / 2                              # km
T   = HTT                                         # seconds (HTT is unit-agnostic)
v1  = np.sqrt(MU_KM / r1)                        # km/s
v2  = np.sqrt(MU_KM / r2)
vTp = np.sqrt(MU_KM * (2/r1 - 1/a))
vTa = np.sqrt(MU_KM * (2/r2 - 1/a))

pre_dur  = T * 0.12
post_dur = T * 0.12
t_pre    = np.linspace(-pre_dur, 0, 200)
t_coast  = np.linspace(0, T, 800)
t_post   = np.linspace(T, T + post_dur, 200)
t_all    = np.concatenate([t_pre, t_coast, t_post])

v_all, _, _, _ = v_total(t_all, r1, r2)          # km, matches v_graph.py's MU

# Convert time axis to minutes
t_min = t_all / 60

# --- Plot --
ax[1].set_facecolor(c_bg)

mask_pre   = t_all < 0
mask_coast = (t_all >= 0) & (t_all <= T)
mask_post  = t_all > T

ax[1].plot(t_min[mask_pre],   v_all[mask_pre],   color=c_blue,   lw=2.2, solid_capstyle='round')
ax[1].plot(t_min[mask_coast], v_all[mask_coast], color=c_orange, lw=2.2, solid_capstyle='round')
ax[1].plot(t_min[mask_post],  v_all[mask_post],  color=c_green,  lw=2.2, solid_capstyle='round')

# Burns
t0_min = 0
tT_min = T / 60

ax[1].annotate('', xy=(t0_min, vTp), xytext=(t0_min, v1),
    arrowprops=dict(arrowstyle='->', color=c_burn, lw=2.0))
ax[1].annotate('', xy=(tT_min, v2), xytext=(tT_min, vTa),
    arrowprops=dict(arrowstyle='->', color=c_burn, lw=2.0))

ax[1].scatter([t0_min, tT_min], [v1, vTa], color=c_burn, s=40, zorder=5)
ax[1].scatter([t0_min, tT_min], [vTp, v2], color=c_burn, s=40, zorder=5)

dv1 = vTp - v1
dv2 = v2  - vTa

ax[1].text(t0_min + (tT_min - t0_min)*0.013, (v1 + vTp)/2,
        f'Δv₁ = +{dv1:.3f} km/s', color=c_burn, fontsize=9.5, va='center')
ax[1].text(tT_min + (tT_min - t0_min)*0.013, (vTa + v2)/2,
        f'Δv₂ = +{dv2:.3f} km/s', color=c_burn, fontsize=9.5, va='center')

# Horizontal reference lines
for val, lbl, col in [(v1, f'v₁ = {v1:.3f} km/s', c_blue),
                       (v2, f'v₂ = {v2:.3f} km/s', c_green)]:
    ax[1].axhline(val, color=col, lw=0.7, ls='--', alpha=0.4)
    ax[1].text(t_min[-1]*1.002, val, lbl, color=col, fontsize=8.5, va='center')

# Burn time lines
for tm in [t0_min, tT_min]:
    ax[1].axvline(tm, color=c_burn, lw=0.8, ls=':', alpha=0.5)

# Phase labels
ax[1].text((t_min[mask_pre].mean()),   v1 + 0.18, 'Initial orbit\n(circular)',
        color=c_blue, fontsize=8.5, ha='center', va='bottom', alpha=0.85)
ax[1].text((t_min[mask_coast].mean()), (vTp+vTa)/2 + 0.22, 'Transfer ellipse\n(vis-viva coast)',
        color=c_orange, fontsize=8.5, ha='center', va='bottom', alpha=0.85)
ax[1].text((t_min[mask_post].mean()),  v2 + 0.18, 'Final orbit\n(circular)',
        color=c_green, fontsize=8.5, ha='center', va='bottom', alpha=0.85)

ax[1].set_xlabel('Time  (minutes)', color=c_text, fontsize=11, labelpad=8)
ax[1].set_ylabel('Speed  (km/s)',   color=c_text, fontsize=11, labelpad=8)
ax[1].set_title('Hohmann transfer: v(t)',
             color=c_text, fontsize=13, fontweight='normal', pad=14)

ax[1].tick_params(colors=c_muted, labelsize=9)
for spine in ax[1].spines.values():
    spine.set_edgecolor(c_grid)
ax[1].grid(True, color=c_grid, lw=0.6, alpha=0.7)
ax[1].set_xlim(t_min[0], t_min[-1] * 1.13)
ax[1].set_ylim(0, vTp * 1.25)

legend_elements = [
    Line2D([0],[0], color=c_blue,   lw=2, label='Initial circular orbit'),
    Line2D([0],[0], color=c_orange, lw=2, label='Transfer ellipse (Kepler)'),
    Line2D([0],[0], color=c_green,  lw=2, label='Final circular orbit'),
    Line2D([0],[0], color=c_burn,   lw=1.5, marker='>', markersize=6, label='Δv burn'),
]
ax[1].legend(handles=legend_elements, loc='upper right',
          facecolor='#1a1a2e', edgecolor=c_grid, labelcolor=c_text, fontsize=9)


plt.show()