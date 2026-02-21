"""
Cardioide principal y 2-ciclo atractor en el plano complejo.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from pathlib import Path


def plot_cardioide_con_disco():
    """
    Genera la gráfica de la cardioide con el disco del 2-ciclo superpuesto.
    """
    # Cardioide principal
    t = np.linspace(0, 2 * np.pi, 1000)
    c_cardioid = 0.5 * np.exp(1j * t) - 0.25 * np.exp(2j * t)

    # Disco (2-ciclo atractor)
    center_real = -1
    center_imag = 0
    radius = 0.25

    t_disk = np.linspace(0, 2 * np.pi, 400)
    x_disk = center_real + radius * np.cos(t_disk)
    y_disk = center_imag + radius * np.sin(t_disk)

    fig = plt.figure(figsize=(6, 6), dpi=300)
    ax = plt.gca()

    # Disco
    ax.plot(x_disk, y_disk, color='blue', linewidth=2)
    ax.fill(x_disk, y_disk, color='blue', alpha=0.2)

    # Cardioide
    ax.plot(c_cardioid.real, c_cardioid.imag, color='blue', linewidth=3)
    ax.fill(c_cardioid.real, c_cardioid.imag, color='blue', alpha=0.3)

    # Configuración de ejes
    ax.axis('equal')
    ax.set_xlim(-1.3, 0.45)
    ax.set_ylim(-0.9, 0.9)

    ax.xaxis.set_major_locator(MultipleLocator(0.2))
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout(pad=0.8)

    return fig


if __name__ == "__main__":
    fig = plot_cardioide_con_disco()

    import os 
    from pathlib import Path
    ruta_completa = Path("resultados/figuras") / f"cardioideCon2Ciclo.pdf"

    fig.savefig(ruta_completa, format="pdf", dpi=400, bbox_inches="tight")
    print(f"Figura guardada en: {ruta_completa.resolve()}")
    plt.show()