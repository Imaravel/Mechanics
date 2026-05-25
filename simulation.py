"""
Verificación numérica de la helicidad del par enlazado:
vórtice rectilíneo (eje x) + anillo de vorticidad (radio R en plano x=0).

Resultado teórico (Moffatt 1969):   H = 2 γ_L γ_R.

Idea: la helicidad se calcula como
        H = γ_L ∫_L v_R · dl  +  γ_R ∫_R v_L · dl,
ya que ω está concentrada en las dos curvas. Cada integral, por
Stokes, equivale al número de enlace × circulación del otro vórtice.

Autor: proyecto de curso de Mecánica Clásica.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# Parámetros físicos
gamma_L = 1.0     # circulación del vórtice rectilíneo
gamma_R = 1.0     # circulación del anillo
R       = 1.0     # radio del anillo


# Campos de velocidad (ley de Biot--Savart)
def v_line(r):
    """Velocidad inducida por el vórtice rectilíneo a lo largo del eje x."""
    x, y, z = r
    rho2 = y*y + z*z
    if rho2 < 1e-14:
        return np.zeros(3)
    f = gamma_L / (2.0 * np.pi * rho2)
    return np.array([0.0, -f*z, f*y])

def v_ring(r, N=400):
    """Velocidad inducida por el anillo (Biot–Savart discretizado)."""
    theta  = np.linspace(0.0, 2*np.pi, N, endpoint=False)
    dtheta = 2*np.pi / N
    ring_pos = np.column_stack([np.zeros(N), R*np.cos(theta), R*np.sin(theta)])
    dl       = np.column_stack([np.zeros(N), -R*np.sin(theta), R*np.cos(theta)]) * dtheta
    diff     = r - ring_pos
    dist     = np.linalg.norm(diff, axis=1)
    mask     = dist > 1e-6
    integrand = np.cross(dl[mask], diff[mask]) / (dist[mask, None]**3)
    return (gamma_R / (4.0 * np.pi)) * integrand.sum(axis=0)

# Cálculo numérico de la helicidad por integrales de línea
def helicity_line_contribution(L_half=50.0, N=4000):
    """γ_L * ∫_L v_R · dl,  L = eje x truncado en (-L_half, L_half)."""
    x_vals = np.linspace(-L_half, L_half, N)
    dx = x_vals[1] - x_vals[0]
    integral = 0.0
    for x in x_vals:
        v = v_ring(np.array([x, 1e-5, 1e-5]))  # evita la singularidad del eje
        integral += v[0] * dx
    return gamma_L * integral

def helicity_ring_contribution(N=600):
    """γ_R * ∫_R v_L · dl_R."""
    theta  = np.linspace(0.0, 2*np.pi, N, endpoint=False)
    dtheta = 2*np.pi / N
    integral = 0.0
    for t in theta:
        r  = np.array([0.0, R*np.cos(t), R*np.sin(t)])
        v  = v_line(r)
        dl = np.array([0.0, -R*np.sin(t), R*np.cos(t)]) * dtheta
        integral += float(np.dot(v, dl))
    return gamma_R * integral

H_line  = helicity_line_contribution()
H_ring  = helicity_ring_contribution()
H_total = H_line + H_ring
H_th    = 2.0 * gamma_L * gamma_R
err     = abs(H_total - H_th) / H_th * 100.0

print("---- Helicidad del par enlazado ----")
print(f"  Contribución de la línea  γ_L ∫_L v_R·dl = {H_line:.6f}")
print(f"  Contribución del anillo   γ_R ∫_R v_L·dl = {H_ring:.6f}")
print(f"  Helicidad numérica  H = {H_total:.6f}")
print(f"  Predicción teórica  2 γ_L γ_R = {H_th:.6f}")
print(f"  Error relativo: {err:.4f} %")


# Figura: geometría 3D + corte transversal
fig = plt.figure(figsize=(8.6, 4.0))

# (a) vista 3D del enlace
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
xs = np.linspace(-2.2, 2.2, 100)
ax1.plot(xs, np.zeros_like(xs), np.zeros_like(xs),
         color='#c0392b', lw=2.5, label=r'$L$: vórtice rectilíneo $\gamma_L$')
phi = np.linspace(0, 2*np.pi, 200)
ax1.plot(np.zeros_like(phi), R*np.cos(phi), R*np.sin(phi),
         color='#1f4e79', lw=2.5, label=r'$R$: anillo $\gamma_R$')
ax1.set_xlabel('x'); ax1.set_ylabel('y'); ax1.set_zlabel('z')
ax1.set_title(r'(a) Líneas de vorticidad enlazadas, $\mathrm{Lk}=1$', fontsize=10)
ax1.legend(loc='upper left', fontsize=8)
ax1.set_box_aspect([2.2, 1.2, 1.2])
ax1.view_init(elev=18, azim=-55)

# (b) campo de velocidad de v_R en el plano y=0 (donde está la línea)
ax2 = fig.add_subplot(1, 2, 2)
xg = np.linspace(-2.0, 2.0, 28)
zg = np.linspace(-2.0, 2.0, 28)
X, Z = np.meshgrid(xg, zg)
U = np.zeros_like(X); W = np.zeros_like(X)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        v = v_ring(np.array([X[i, j], 0.0, Z[i, j]]))
        U[i, j], W[i, j] = v[0], v[2]
speed = np.sqrt(U*U + W*W)
ax2.streamplot(X, Z, U, W, color=np.log(speed+1e-6),
               cmap='viridis', density=1.3, linewidth=0.9, arrowsize=0.9)
ax2.plot([-2.0, 2.0], [0.0, 0.0], color='#c0392b', lw=2.0,
         label=r'$L$ (eje $x$)')
ax2.plot([0.0, 0.0], [-R, R], 'o', color='#1f4e79', ms=6,
         label=r'cortes del anillo')
ax2.set_xlabel(r'$x$'); ax2.set_ylabel(r'$z$')
ax2.set_title(r'(b) Líneas de $\mathbf{v}_R$ en el plano $y=0$', fontsize=10)
ax2.set_aspect('equal'); ax2.legend(loc='upper right', fontsize=8)

plt.tight_layout()
plt.savefig('/Users/ardila/Desktop/vortices.pdf', bbox_inches='tight')
plt.savefig('/Users/ardila/Desktop/vortices.png', dpi=160, bbox_inches='tight')
print("Figura guardada: vortices.pdf / vortices.png")