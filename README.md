# Conjunto de Mandelbrot y Conjunto de Julia lleno

Trabajo Fin de Grado Matemáticas - Universidad de La Rioja 
Carmen Ortiz Olivan, Curso 2025-2026

Implementación y visualización de fractales clásicos:  
- Conjunto de Mandelbrot (completo, regiones, zooms, periodos)  
- Conjuntos de Julia parametrizados  
- Diagrama de Feigenbaum  
- Curva de Koch  
- Función de Weierstrass  
- Relación Mandelbrot–Julia

## Instalación

```bash
python -m venv .venv
.\.venv\Scripts\activate    # Windows
pip install -r requirements.txt

## Generar figuras
python src/visualization/generate_all.py --all
# o solo una: python ... --only mandelbrot_full