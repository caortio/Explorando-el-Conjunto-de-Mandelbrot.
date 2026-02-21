"""
Cardioide: parametrización directa.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def plot_cardioide():
    t = np.linspace(0, 2 * np.pi, 1000)
    c = 0.5 * np.exp(1j * t) - 0.25 * np.exp(2j * t)
    
    fig = plt.figure(figsize=(5, 5), dpi=300)
    
    plt.plot(c.real, c.imag, lw=3, color='blue')
    plt.fill(c.real, c.imag, alpha=0.3, color='blue')
    
    plt.axis('equal')
    plt.grid(alpha=0.4)
    
    plt.tight_layout(pad=0.5)
    
    return fig


if __name__ == "__main__":
    fig = plot_cardioide()
    
    import os 
    from pathlib import Path
    ruta_completa = Path("resultados/figuras") / f"cardioide.pdf"

    fig.savefig(ruta_completa, format="pdf", dpi=400, bbox_inches="tight")
    print(f"Figura guardada en: {ruta_completa.resolve()}")
    plt.show()