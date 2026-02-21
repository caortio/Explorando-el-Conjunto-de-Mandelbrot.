"""
Generación del copo de nieve de Koch (curva de Koch cerrada).
"""

import matplotlib.pyplot as plt
from math import sin, cos, pi


def koch_curve(xi, yi, xf, yf, n):
    """
    Función recursiva que dibuja un segmento de la curva de Koch.
    """
    if n == 0:
        plt.plot([xi, xf], [yi, yf], color="blue", linewidth=0.7)
    else:
        x1 = xi + (xf - xi) / 3.0
        y1 = yi + (yf - yi) / 3.0

        x3 = xf - (xf - xi) / 3.0
        y3 = yf - (yf - yi) / 3.0

        x2 = (x1+x3) * cos(pi/3) - (y3-y1) * sin(pi/3)
        y2 = (y1+y3) * cos(pi/3) + (x3-x1) * sin(pi/3)

        koch_curve(xi, yi, x1, y1, n-1)
        koch_curve(x1, y1, x2, y2, n-1)
        koch_curve(x2, y2, x3, y3, n-1)
        koch_curve(x3, y3, xf, yf, n-1)


def plot_koch_snowflake(side_length, iterations, figsize, dpi):
    """
    Genera y devuelve la figura del copo de nieve de Koch.
    
    Retorna: matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    x1, y1 = 0, 0
    x2 = side_length * cos(2 * pi / 3)
    y2 = side_length * sin(2 * pi / 3)
    x3 = side_length * cos(pi / 3)
    y3 = side_length * sin(pi / 3)

    koch_curve(x1, y1, x2, y2, iterations)
    koch_curve(x2, y2, x3, y3, iterations)
    koch_curve(x3, y3, x1, y1, iterations)

    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    return fig


# ── Ejecución directa ────────────────────────────────
if __name__ == "__main__":
    fig = plot_koch_snowflake(200,6,(6,6),400)
    plt.show()