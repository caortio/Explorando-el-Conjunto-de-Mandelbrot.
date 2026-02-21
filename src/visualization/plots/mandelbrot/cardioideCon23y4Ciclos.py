"""
Puntos con período 3 y período 4 estricto en el plano de parámetros c,
excluyendo cardioide principal y disco del 2-ciclo + zoom en bulbo ≈ -1.94079
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path as MatPath          # ← Import correcto para polígonos
from multiprocessing import Pool, cpu_count
from pathlib import Path                             # ← Ahora sin alias, usado solo para carpetas


# ────────────────────────────────────────────────────────
# Funciones auxiliares
# ────────────────────────────────────────────────────────

def iterate_fc_vector(c, N=800):
    """Itera z → z² + c para vector de c's"""
    z = np.zeros_like(c, dtype=complex)
    orbit = np.zeros((N, c.size), dtype=complex)
    for i in range(N):
        z = z**2 + c
        orbit[i] = z
    return orbit


def is_strict_period_3(orbit):
    """Detecta período 3 estricto en los últimos valores"""
    tail = orbit[-60:]
    result = np.zeros(orbit.shape[1], dtype=bool)
    for j in range(orbit.shape[1]):
        vals = tail[:, j]
        unique_vals = np.unique(np.round(vals, 4))
        result[j] = (len(unique_vals) == 3)
    return result


def iterate_fc(c, z0=0, N=600, R=10):
    """Iteración clásica para un solo c"""
    z = z0
    orbit = []
    for _ in range(N):
        z = z*z + c
        if abs(z) > R:
            return None
        orbit.append(z)
    return np.array(orbit)


def is_period_4(orbit, tol=1e-5):
    """Detecta período 4 aproximado"""
    if orbit is None or len(orbit) < 5:
        return False
    z = orbit[-1]
    for k in [1, 2, 3]:
        if abs(z - orbit[-1-k]) < tol:
            return False
    return abs(z - orbit[-5]) < tol


def process_row_period3(x, cardioid_path, center_real, center_imag, radius, im_vals):
    """Procesa una fila horizontal para período 3"""
    row_real = []
    row_imag = []
    for y in im_vals:
        c = np.array([x + 1j*y])
        is_in_disk = (x - center_real)**2 + (y - center_imag)**2 < (radius - 1e-2)**2
        is_in_cardioid = cardioid_path.contains_point((x + 1e-2, y))
        if not is_in_disk and not is_in_cardioid:
            orbit = iterate_fc_vector(c)
            if is_strict_period_3(orbit)[0]:
                row_real.append(x)
                row_imag.append(y)
    return row_real, row_imag


# ────────────────────────────────────────────────────────
# Figura principal
# ────────────────────────────────────────────────────────

def plot_periodos_3_y_4_con_bulbo():
    print("Preparando cardioide y disco...")

    # Cardioide principal
    t = np.linspace(0, 2*np.pi, 2000)
    c_cardioid = 0.5*np.exp(1j*t) - 0.25*np.exp(2j*t)
    cardioid_path = MatPath(np.column_stack([c_cardioid.real, c_cardioid.imag]))

    # Disco 2-ciclo
    center_real = -1.0
    center_imag = 0.0
    radius = 0.25

    t_disk = np.linspace(0, 2*np.pi, 400)
    x_disk = center_real + radius * np.cos(t_disk)
    y_disk = center_imag + radius * np.sin(t_disk)

    # Muestreo global
    re_vals = np.linspace(-2, 0.5, 600)
    im_vals = np.linspace(-1.3, 1.3, 600)

    # Período 3 
    C3_real, C3_imag = [], []
    with Pool(cpu_count()) as pool:
        results = pool.starmap(
            process_row_period3,
            [(x, cardioid_path, center_real, center_imag, radius, im_vals) for x in re_vals]
        )
    for r_real, r_imag in results:
        C3_real.extend(r_real)
        C3_imag.extend(r_imag)

    # Período 4 global 
    C4_real, C4_imag = [], []
    for x in re_vals:
        for y in im_vals:
            is_in_disk = (x - center_real)**2 + (y - center_imag)**2 < radius**2
            is_in_cardioid = cardioid_path.contains_point((x, y))
            if not is_in_disk and not is_in_cardioid:
                c = x + 1j*y
                orbit = iterate_fc(c)
                if orbit is not None and is_period_4(orbit[300:]):
                    C4_real.append(x)
                    C4_imag.append(y)

    zoom_center = -1.94079
    zoom_radius = 0.04
    re_zoom = np.linspace(zoom_center - zoom_radius, zoom_center + zoom_radius, 500)
    im_zoom = np.linspace(-0.08, 0.08, 500)

    for x in re_zoom:
        for y in im_zoom:
            c = x + 1j*y
            orbit = iterate_fc(c, N=800)
            if orbit is not None and is_period_4(orbit[400:]):
                C4_real.append(x)
                C4_imag.append(y)

    C3_set = set(zip(np.round(C3_real, 4), np.round(C3_imag, 4)))
    C4_set = set(zip(np.round(C4_real, 4), np.round(C4_imag, 4)))
    C4_only = C4_set - C3_set
    C4_only_real = [p[0] for p in C4_only]
    C4_only_imag = [p[1] for p in C4_only]

    # Gráfica final
    fig = plt.figure(figsize=(8, 8), dpi=300)

    plt.scatter(C3_real, C3_imag, s=1, color='blue', alpha=0.6)
    plt.scatter(C4_only_real, C4_only_imag, s=1, color='blue', alpha=0.6)

    plt.plot(x_disk, y_disk, color='blue', linewidth=2)
    plt.fill(x_disk, y_disk, color='blue', alpha=0.25)

    plt.plot(c_cardioid.real, c_cardioid.imag, lw=3, color='blue')
    plt.fill(c_cardioid.real, c_cardioid.imag, color='blue', alpha=0.3)

    plt.axis('equal')
    plt.xlim(-2, 0.5)
    plt.ylim(-1.3, 1.3)
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout(pad=0.8)
    return fig


if __name__ == "__main__":
    fig = plot_periodos_3_y_4_con_bulbo()

    import os 
    from pathlib import Path
    ruta_completa = Path("resultados/figuras") / f"cardioideCon23y4Ciclos.pdf"

    fig.savefig(ruta_completa, format="pdf", dpi=400, bbox_inches="tight")
    print(f"Figura guardada en: {ruta_completa.resolve()}")
    plt.show()