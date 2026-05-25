# gauge-fluid-helicity

Verificación numérica de la helicidad de un par enlazado de vórtices ---
una recta y un anillo --- mediante la ley de Biot--Savart. Sirve de
material de apoyo para el trabajo de curso *"Análisis de la formulación
variacional del fluido ideal a partir del principio gauge"*.

## Contexto físico

En la formulación gauge del fluido ideal, la **vorticidad**
(`omega = curl v`) es el campo de norma asociado al grupo de rotaciones
locales SO(3). La cantidad

    H = integral sobre V de (omega . v) d^3x

llamada **helicidad**, es el análogo hidrodinámico del término topológico
de Chern--Simons. Moffatt (1969) demostró que mide el enlace y anudamiento
de las líneas de vorticidad: para N filamentos cerrados de circulaciones
`gamma_i` y números de enlace mutuos `Lk(i,j)`,

    H = 2 * suma sobre i<j de [gamma_i * gamma_j * Lk(i,j)].

El caso de prueba más sencillo es el par enlazado **recta + anillo**:
un vórtice rectilíneo L sobre el eje x atravesando una vez a un anillo
de vorticidad R de radio R en el plano x=0. Como `Lk(L,R) = 1`, la
predicción teórica es:

    H_teorico = 2 * gamma_L * gamma_R.

Este repositorio comprueba numéricamente esa predicción.

## Qué hace el script

1. Calcula el campo de velocidad inducido por la recta de forma analítica.
2. Calcula el campo del anillo discretizando Biot--Savart con N = 400 puntos.
3. Evalúa la helicidad como suma de dos integrales de línea
   (que por el teorema de Stokes equivalen al número de enlace
   multiplicado por la circulación):

       H = gamma_L * (integral sobre L de v_R . dl)
         + gamma_R * (integral sobre R de v_L . dl).

4. Compara con el valor teórico y reporta el error relativo.
5. Genera la figura `vortices.pdf` / `vortices.png` con dos paneles:
   (a) la geometría 3D del enlace y (b) las líneas de corriente del
   campo del anillo en el plano y = 0 que contiene a la recta.

## Requisitos

- Python 3.9 o superior
- NumPy
- Matplotlib

Instalación rápida:

    pip install numpy matplotlib

## Uso

    python simulation.py

Salida esperada en consola:

    ---- Helicidad del par enlazado ----
      Contribucion de la linea  gamma_L * int_L v_R . dl = 0.999800
      Contribucion del anillo   gamma_R * int_R v_L . dl = 1.000000
      Helicidad numerica  H = 1.999800
      Prediccion teorica  2 gamma_L gamma_R = 2.000000
      Error relativo: 0.0100 %
    Figura guardada: vortices.pdf / vortices.png

El error relativo del orden de 10^-4 es consistente con el orden N^-2
esperado para la regla del trapecio aplicada a un integrando suave
y periódico.

## Parámetros que se pueden modificar

Al inicio de `simulation.py`:

| Variable  | Significado                          | Valor por defecto |
|-----------|--------------------------------------|-------------------|
| `gamma_L` | Circulación del vórtice rectilíneo   | 1.0               |
| `gamma_R` | Circulación del anillo               | 1.0               |
| `R`       | Radio del anillo                     | 1.0               |

Dentro de las funciones de integración pueden ajustarse:

- `N` (puntos angulares para Biot--Savart sobre el anillo) afecta la
  precisión del campo del anillo.
- `L_half` y el número de pasos para la integral sobre la recta
  controlan qué tan lejos se trunca el eje x.

## Cómo extenderlo

Algunas direcciones naturales para seguir trabajando:

- **Nudos no triviales:** sustituir uno de los filamentos por un nudo
  trébol y verificar que la helicidad escala con el número de
  auto-enlace.
- **Pares enlazados múltiples:** dos anillos entrelazados como en los
  experimentos de Kleckner y Irvine sobre vorticidad anudada.
- **Disipación:** añadir un término viscoso y estudiar cómo decae la
  helicidad en función del número de Reynolds.
- **Visualización:** reemplazar el `streamplot` por una integración
  explícita de las líneas de corriente del campo total.

## Referencias

- T. Kambe, *Variational formulation of ideal fluid flows according to
  gauge principle*, Fluid Dyn. Res. **40**, 399 (2008).
  arXiv:0709.2964 [nlin.CD].
- H. K. Moffatt, *The degree of knottedness of tangled vortex lines*,
  J. Fluid Mech. **35**, 117 (1969).
- F. P. Bretherton, *A note on Hamilton's principle for perfect fluids*,
  J. Fluid Mech. **44**, 19 (1970).

## Cita sugerida

Si este código le resulta útil para un trabajo académico, una cita posible es:

    Autor, "gauge-fluid-helicity: numerical verification of vortex
    linking helicity", 2026. Trabajo de curso, Universidad de los Andes.
    https://github.com/usuario/gauge-fluid-helicity

## Licencia

MIT.
