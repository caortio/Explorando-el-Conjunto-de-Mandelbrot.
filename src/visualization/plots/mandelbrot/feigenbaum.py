"""
Diagrama de Feigenbaum
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def mandel_orbit(c, x0=0.0, N=500, transient=400):
    x = x0
    for _ in range(transient):
        x = x * x + c
    
    orbit = []
    for _ in range(N - transient):
        x = x * x + c
        orbit.append(x)
    
    return orbit


def plot_diagrama_feigenbaum():
    C_list = np.linspace(-2.0, 1.0, 1000)     
    N_total = 500                             
    transient = 400                           
    x0 = 0.0                                  

    x_select = []
    c_select = []

    for c in C_list:
        orbit = mandel_orbit(c, x0, N_total, transient)
        x_select.extend(orbit)
        c_select.extend([c] * len(orbit))

    x_select = np.array(x_select)
    c_select = np.array(c_select)

    fig = plt.figure(figsize=(10, 6), dpi=300)

    plt.scatter(c_select, x_select, color='blue', s=0.2, alpha=0.6, rasterized=True)

    plt.xlabel('c', fontsize=11)
    plt.ylabel('x', fontsize=11)

    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout(pad=1.0)

    return fig


if __name__ == "__main__":
    fig = plot_diagrama_feigenbaum()

    import os 
    from pathlib import Path
    ruta_completa = Path("resultados/figuras") / f"feigenbaum.pdf"

    fig.savefig(ruta_completa, format="pdf", dpi=400, bbox_inches="tight")
    print(f"Figura guardada en: {ruta_completa.resolve()}")
    plt.show()