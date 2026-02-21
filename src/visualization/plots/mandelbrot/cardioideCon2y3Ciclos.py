"""
Cardioide principal, 2-ciclo atractor y 3-ciclos atractores en el plano complejo.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath          # ← Import correcto para polígonos
from multiprocessing import Pool, cpu_count
from pathlib import Path as PathlibPath            # ← Renombrado para evitar conflicto
import sys


def iterate_fc_vector(c, N=800):
    """Itera z → z² + c y devuelve la órbita completa."""
    z = np.zeros_like(c, dtype=complex)
    orbit = np.zeros((N, c.size), dtype=complex)
    for i in range(N):
        z = z**2 + c
        orbit[i] = z
    return orbit


def is_strict_period_3(orbit):
    """Detecta periodo 3 estricto mirando los últimos valores."""
    tail = orbit[-60:]
    Npoints = orbit.shape[1]
    result = np.zeros(Npoints, dtype=bool)
    for j in range(Npoints):
        vals = tail[:, j]
        unique_vals = np.unique(np.round(vals, decimals=4))
        result[j] = (len(unique_vals) == 3)
    return result


def process_row(x, cardioid_path, center_real, center_imag, radius, im_vals):
    """Procesa una fila horizontal (valor fijo de Re(c))."""
    row_real = []
    row_imag = []
    for y in im_vals:
        c = np.array([x + 1j * y])

        # Exclusión geométrica
        is_in_disk = (x - center_real)**2 + (y - center_imag)**2 < (radius - 1e-2)**2
        is_in_cardioid = cardioid_path.contains_point((x + 1e-2, y))

        if not is_in_disk and not is_in_cardioid:
            orbit = iterate_fc_vector(c)
            if is_strict_period_3(orbit)[0]:
                row_real.append(x)
                row_imag.append(y)
    return row_real, row_imag


def plot_periodo_3():
    """Función principal que genera la figura."""
    # 1. Cardioide principal
    t = np.linspace(0, 2*np.pi, 2000)
    c_cardioid = 0.5*np.exp(1j*t) - 0.25*np.exp(2j*t)
    cardioid_path = MPath(np.column_stack([c_cardioid.real, c_cardioid.imag]))

    # 2. Disco del 2-ciclo
    center_real = -1.0
    center_imag = 0.0
    radius = 0.25

    t_disk = np.linspace(0, 2*np.pi, 400)
    x_disk = center_real + radius * np.cos(t_disk)
    y_disk = center_imag + radius * np.sin(t_disk)

    # 3. Muestreo del plano
    re_vals = np.linspace(-2, 0.5, 600)
    im_vals = np.linspace(-1.3, 1.3, 600)

    # Multiprocesamiento
    print("Calculando puntos con periodo 3... (puede tardar varios minutos)")
    with Pool(cpu_count()) as pool:
        results = pool.starmap(
            process_row,
            [(x, cardioid_path, center_real, center_imag, radius, im_vals) for x in re_vals]
        )

    C3_real, C3_imag = [], []
    for r_real, r_imag in results:
        C3_real.extend(r_real)
        C3_imag.extend(r_imag)

    print(f"Se encontraron {len(C3_real)} puntos con periodo 3 estricto.")

    # 4. Gráfica final
    fig = plt.figure(figsize=(8, 8), dpi=300)

    plt.scatter(C3_real, C3_imag, s=1, color='blue', alpha=0.6)

    # Disco 2-ciclo
    plt.plot(x_disk, y_disk, color='blue', linewidth=2)
    plt.fill(x_disk, y_disk, color='blue', alpha=0.25)

    # Cardioide
    plt.plot(c_cardioid.real, c_cardioid.imag, lw=3, color='blue')
    plt.fill(c_cardioid.real, c_cardioid.imag, color='blue', alpha=0.3)

    plt.axis('equal')
    plt.xlim(-2, 0.5)
    plt.ylim(-1.3, 1.3)
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout(pad=0.8)
    return fig

if __name__ == "__main__":
    fig = plot_periodo_3()

    import os 
    from pathlib import Path
    ruta_completa = Path("resultados/figuras") / f"cardioideCon2y3Ciclos.pdf"

    fig.savefig(ruta_completa, format="pdf", dpi=400, bbox_inches="tight")
    print(f"Figura guardada en: {ruta_completa.resolve()}")
    plt.show()