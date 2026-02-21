"""
Generación de la función de Weierstrass.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def weierstrass(x, a, b, n):
    W = np.zeros_like(x)
    for i in range(n):
        W += a**i * np.cos(b**i * np.pi * x)
    return W


def plot_weierstrass():
    x = np.linspace(-2, 2, 8000)
    y = weierstrass(x, 0.5, 8, 50)

    fig, ax = plt.subplots(figsize=(12, 6))

    # Curva de Weierstrass
    ax.plot(x, y, color="blue", linewidth=2)

    # Ejes y bordes
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_linewidth(1)
    ax.spines['bottom'].set_linewidth(1)
    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout()
    
    return fig


if __name__ == "__main__":
    fig = plot_weierstrass()
    
    import os 
    from pathlib import Path
    ruta_completa = Path("resultados/figuras") / f"weierstrass.pdf"

    fig.savefig(ruta_completa, format="pdf", dpi=400, bbox_inches="tight")
    print(f"Figura guardada en: {ruta_completa.resolve()}")
    plt.show()