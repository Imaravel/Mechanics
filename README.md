
# gauge-fluid-helicity

Verificación numérica de la helicidad de un par enlazado de vórtices ---
una recta y un anillo --- mediante la ley de Biot--Savart. Sirve de
material de apoyo para el trabajo de curso *"Análisis de la formulación
variacional del fluido ideal a partir del principio gauge"*.

## Contexto físico

En la formulación gauge del fluido ideal, la vorticidad
$\boldsymbol{\omega}=\nabla\times\mathbf{v}$ es el campo de norma asociado al
grupo de rotaciones locales $SO(3)$. La cantidad

$$
\mathcal{H} \;=\; \int_V \boldsymbol{\omega}\cdot\mathbf{v}\,d^3x,
$$

llamada **helicidad**, es entonces el análogo hidrodinámico del término
topológico de Chern--Simons. Moffatt (1969) demostró que mide el enlace y
anudamiento de las líneas de vorticidad: para $N$ filamentos cerrados de
circulaciones $\gamma_i$ y números de enlace $\mathrm{Lk}(i,j)$,

$$
\mathcal{H} \;=\; 2\sum_{i<j}\gamma_i\gamma_j\,\mathrm{Lk}(i,j).
$$

El caso de prueba más sencillo es el par enlazado **recta $+$ anillo**: un
vórtice rectilíneo $L$ sobre el eje $x$ atravesando una vez a un anillo de
vorticidad $R$ de radio $R$ en el plano $x=0$. Como $\mathrm{Lk}(L,R)=1$,

$$
\mathcal{H}_{\text{teórico}} \;=\; 2\gamma_L\gamma_R.
$$

Este repositorio comprueba numéricamente esta predicción.

## Qué hace el script

1. Calcula el campo de velocidad inducido por la recta de forma analítica.
2. Calcula el campo del anillo discretizando Biot--Savart con $N=400$ puntos.
3. Evalúa la helicidad como suma de dos integrales de línea
   (que por Stokes equivalen al número de enlace):

$$
\mathcal{H} \;=\; \gamma_L\!\int_L \mathbf{v}_R\!\cdot d\boldsymbol{\ell}
                 \;+\; \gamma_R\!\int_R \mathbf{v}_L\!\cdot d\boldsymbol{\ell}.
$$

4. Compara con el valor teórico y reporta el error relativo.
5. Genera la figura `vortices.pdf` / `vortices.png` con dos paneles:
   (a) la geometría 3D del enlace y (b) las líneas de corriente de
   $\mathbf{v}_R$ en el plano $y=0$ que contiene a $L$.

## Requisitos

```
python >= 3.9
numpy
matplotlib
```

Instalación rápida:

```bash
pip install numpy matplotlib
```

## Uso

```bash
python simulation.py
```

Salida esperada en consola:

```
---- Helicidad del par enlazado ----
  Contribución de la línea  γ_L ∫_L v_R·dl = 0.999800
  Contribución del anillo   γ_R ∫_R v_L·dl = 1.000000
  Helicidad numérica  H = 1.999800
  Predicción teórica  2 γ_L γ_R = 2.000000
  Error relativo: 0.0100 %
Figura guardada: vortices.pdf / vortices.png
```

El error relativo del orden de $10^{-4}$ es consistente con $\mathcal{O}(N^{-2})$
para la regla del trapecio aplicada a un integrando suave y periódico.

## Parámetros que se pueden modificar

Al inicio de `simulation.py`:

| Variable    | Significado                              | Valor por defecto |
|-------------|------------------------------------------|-------------------|
| `gamma_L`   | Circulación del vórtice rectilíneo       | `1.0`             |
| `gamma_R`   | Circulación del anillo                   | `1.0`             |
| `R`         | Radio del anillo                         | `1.0`             |

Dentro de las funciones de integración pueden ajustarse:

- `N` (puntos angulares para Biot--Savart sobre el anillo) — afecta la
  precisión del campo $\mathbf{v}_R$.
- `L_half` y el número de pasos para la integral sobre la recta — controlan
  qué tan lejos se trunca el eje $x$.

## Cómo extenderlo

Algunas direcciones naturales para seguir trabajando:

- **Nudos no triviales:** sustituir uno de los filamentos por un nudo trébol
  y verificar que la helicidad escala con el número de auto-enlace.
- **Pares enlazados múltiples:** dos anillos entrelazados como en los
  experimentos de Kleckner & Irvine sobre vorticidad anudada.
- **Disipación:** añadir un término viscoso y estudiar cómo decae la
  helicidad en función del número de Reynolds.
- **Visualización:** reemplazar el `streamplot` por una integración explícita
  de las líneas de corriente de $\mathbf{v}_L+\mathbf{v}_R$.

## Referencias

- T. Kambe, *Variational formulation of ideal fluid flows according to gauge
  principle*, Fluid Dyn. Res. **40**, 399 (2008). [arXiv:0709.2964](https://arxiv.org/abs/0709.2964)
- H. K. Moffatt, *The degree of knottedness of tangled vortex lines*,
  J. Fluid Mech. **35**, 117 (1969).
- F. P. Bretherton, *A note on Hamilton's principle for perfect fluids*,
  J. Fluid Mech. **44**, 19 (1970).

## Cita sugerida

Si este código le resulta útil para un trabajo académico, una cita posible es:

```bibtex
@misc{gauge-fluid-helicity,
  author = {[Autor]},
  title  = {gauge-fluid-helicity: numerical verification of vortex linking helicity},
  year   = {2026},
  url    = {https://github.com/usuario/gauge-fluid-helicity},
  note   = {Trabajo de curso, Universidad de los Andes}
}
```

## Licencia

MIT.
