"""
Conjunto de Mandelbrot con etiquetas de centros de períodos exactos
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.path import Path as MatPath 
from pathlib import Path

def iterate_fc_and_derivative(c, p):
    z = 0j
    dzdc = 0j
    for _ in range(p):
        dzdc = 2 * z * dzdc + 1
        z = z * z + c
    return z, dzdc

def newton_center(c0, p, tol=1e-14, max_iter=50):
    c = c0
    for _ in range(max_iter):
        z, dzdc = iterate_fc_and_derivative(c, p)
        if abs(z) < tol:
            return c
        if dzdc == 0:
            return None
        c -= z / dzdc
    return None


def find_centers(p, seeds=2000, R=2.0):
    roots = []
    for k in range(seeds):
        theta = 2 * np.pi * k / seeds
        r = R * (k / seeds)
        c0 = r * np.exp(1j * theta)
        root = newton_center(c0, p)
        if root is None:
            continue
        if not any(abs(root - r0) < 1e-10 for r0 in roots):
            roots.append(root)
    return roots


def exact_period_centers(p, all_centers):
    exact = []
    for c in all_centers[p]:
        if not any(
            abs(iterate_fc_and_derivative(c, q)[0]) < 1e-12
            for q in range(1, p)
        ):
            exact.append(c)
    return exact


def mandelbrot(width, height, re_start, re_end, im_start, im_end, max_iter):
    re = np.linspace(re_start, re_end, width)
    im = np.linspace(im_start, im_end, height)
    C = re[np.newaxis, :] + 1j * im[:, np.newaxis]

    Z = np.zeros_like(C)
    escaped = np.zeros(C.shape, dtype=bool)
    M = np.zeros(C.shape)

    for i in range(max_iter):
        Z[~escaped] = Z[~escaped]**2 + C[~escaped]
        new = np.abs(Z) > 2
        M[new & ~escaped] = i
        escaped |= new

    M[~escaped] = np.nan
    return re, im, M


def filter_centers(centers, max_period, min_dist):
    selected = []
    for p in sorted(centers.keys()):
        if p > max_period:
            continue
        for c in centers[p]:
            if all(abs(c - c0) > min_dist for _, c0 in selected):
                selected.append((p, c))
    return selected

def plot_mandelbrot_con_centros_periodicos():
    MAX_PERIOD_COMPUTE = 8
    MAX_PERIOD_LABEL   = 7
    MIN_LABEL_DISTANCE = 0.08

    all_centers = {}
    for p in range(1, MAX_PERIOD_COMPUTE + 1):
        print(f" → período {p}")
        all_centers[p] = find_centers(p)

    exact_centers = {
        p: exact_period_centers(p, all_centers)
        for p in all_centers
    }

    labels = filter_centers(exact_centers, max_period=MAX_PERIOD_LABEL, min_dist=MIN_LABEL_DISTANCE
    )

    # Colormap personalizado
    cmap_custom = LinearSegmentedColormap.from_list(
        "mandelbrot_custom",
        [
            (0.0, (0.95, 0.95, 1.0)),  
            (0.5, (0.98, 0.98, 1.0)),  
            (1.0, (1.0, 1.0, 1.0))     
        ]
    )
    cmap_custom.set_bad("black")  

    re_start = -2
    re_end   = 1
    im_start = -1.2
    im_end   = 1.2
    width    = 1000
    height   = 1000
    max_iter = 500

    print("Renderizando conjunto de Mandelbrot...")
    re, im, M = mandelbrot(width, height, re_start, re_end, im_start, im_end, max_iter)

    # Figura
    fig = plt.figure(figsize=(8, 8), dpi=300)

    plt.imshow(M, extent=[re[0], re[-1], im[0], im[-1]], origin="lower", cmap=cmap_custom)

    #Ejes visibles
    ax = plt.gca()

    ax.tick_params(
        axis="both",
        direction="out",
        length=4,
        width=0.8,
        colors="black"
    )

    ax.set_xticks(np.arange(-2, 1.1, 0.5))
    ax.set_yticks(np.arange(-1.2, 1.21, 0.4))

    for spine in ax.spines.values():
        spine.set_linewidth(0.8)
        spine.set_color("black")

    #Ejes no visibles
    #plt.xticks([])
    #plt.yticks([])
    
    # Etiquetas de períodos
    for p, c in labels:
        plt.text(c.real, c.imag, str(p), fontsize=11, color="black", ha="center", va="center",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, boxstyle="round,pad=0.15"))



    plt.tight_layout(pad=0.5)
    return fig


if __name__ == "__main__":
    fig = plot_mandelbrot_con_centros_periodicos()
    
    import os 
    from pathlib import Path
    ruta_completa = Path("resultados/figuras") / f"mandelbrotConPeriodos.pdf"

    fig.savefig(ruta_completa, format="pdf", dpi=400, bbox_inches="tight")
    print(f"Figura guardada en: {ruta_completa.resolve()}")
    plt.show()