"""
Tangente en el 3-ciclo.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from pathlib import Path


def f(x):
    return x**2 - 1.75


def g(x):
    return f(f(f(x))) - x


def plot_tangente_periodo_3():
    x = np.linspace(-2, 2, 4000)
    y = f(f(f(x)))  # f³(x)

    fig = plt.figure(figsize=(6, 6), dpi=300)

    # Curvas principales
    plt.plot(x, y, color='black')
    plt.plot(x, x, color='red')
    plt.ylim(-2.5, 2.5)
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.grid(True, linestyle=':', alpha=0.4)
    plt.tight_layout(pad=0.8)

    return fig


if __name__ == "__main__":
    fig = plot_tangente_periodo_3()

    import os 
    from pathlib import Path
    ruta_completa = Path("resultados/figuras") / f"puntosPeriodo3.pdf"

    fig.savefig(ruta_completa, format="pdf", dpi=400, bbox_inches="tight")
    print(f"Figura guardada en: {ruta_completa.resolve()}")
    plt.show()