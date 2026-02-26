# Explorando el Conjunto de Mandelbrot.

Trabajo Fin de Grado Matemáticas - Universidad de La Rioja 
Carmen Ortiz Olivan, Curso 2025-2026

Implementación y visualización de fractales clásicos:  
- Conjunto de Mandelbrot (completo, regiones, zooms, periodos).
- Conjuntos de Julia llenos asociados a la función cuadrática z²+c dado un valor del parámetro c.
- Diagrama de Feigenbaum.  
- Curva de Koch.  
- Función de Weierstrass.  
- Panel que muestra la relación del conjunto de Mandelbrot con algunos conjuntos de Julia llenos.

## Observaciones
La mayoría de imágenes se generan iterando una función un cierto número de iteraciones. Está elegido uno en cada caso para que la figura se vea con una precisión razonable, pero este puede aumentarse o reducirse.

## Instalación

```bash
python -m venv .venv
.\.venv\Scripts\activate    # Windows
pip install -r requirements.txt

## Generar figuras
python src/visualization/nombreFichero.py
