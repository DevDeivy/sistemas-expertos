# ============================================================
# SISTEMA DE RAZONAMIENTO DIFUSO PARA DIAGNÓSTICO DE FIEBRE
# SKFuzzy + Gradio
# ============================================================

import numpy as np 
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import gradio as gr
import io
from PIL import Image


# ============================================================
# VARIABLES DIFUSAS (UNIVERSOS DE DISCURSO)
# ============================================================

temperatura = ctrl.Antecedent(np.arange(36, 41.1, 0.1), 'temperatura')
dolor = ctrl.Antecedent(np.arange(0, 11, 1), 'dolor')
fatiga = ctrl.Antecedent(np.arange(0, 11, 1), 'fatiga')
gravedad = ctrl.Consequent(np.arange(0, 11, 1), 'gravedad')


# ============================================================
# FUNCIONES DE MEMBRESÍA
# ============================================================

# Temperatura corporal (°C)
temperatura['normal'] = fuzz.trimf(temperatura.universe, [36, 36, 37.5])
temperatura['febricula'] = fuzz.trimf(temperatura.universe, [37, 38, 39])
temperatura['alta'] = fuzz.trimf(temperatura.universe, [38.5, 41, 41])

# Dolor corporal (0-10)
dolor['leve'] = fuzz.trimf(dolor.universe, [0, 0, 4])
dolor['moderado'] = fuzz.trimf(dolor.universe, [3, 5, 7])
dolor['severo'] = fuzz.trimf(dolor.universe, [6, 10, 10])

# Fatiga (0-10)
fatiga['baja'] = fuzz.trimf(fatiga.universe, [0, 0, 4])
fatiga['media'] = fuzz.trimf(fatiga.universe, [3, 5, 7])
fatiga['alta'] = fuzz.trimf(fatiga.universe, [6, 10, 10])

# Gravedad del cuadro (salida, 0-10)
gravedad['leve'] = fuzz.trimf(gravedad.universe, [0, 0, 4])
gravedad['moderada'] = fuzz.trimf(gravedad.universe, [3, 5, 7])
gravedad['grave'] = fuzz.trimf(gravedad.universe, [6, 10, 10])


# ============================================================
# BASE DE REGLAS (mínimo 5 — aquí van 7)
# ============================================================

regla1 = ctrl.Rule(temperatura['alta'] & dolor['severo'], gravedad['grave'])
regla2 = ctrl.Rule(temperatura['normal'] & fatiga['baja'], gravedad['leve'])
regla3 = ctrl.Rule(temperatura['febricula'] & dolor['moderado'], gravedad['moderada'])
regla4 = ctrl.Rule(fatiga['alta'] & dolor['severo'], gravedad['grave'])
regla5 = ctrl.Rule(temperatura['alta'] & fatiga['alta'], gravedad['grave'])
regla6 = ctrl.Rule(temperatura['normal'] & dolor['leve'] & fatiga['baja'], gravedad['leve'])
regla7 = ctrl.Rule(temperatura['febricula'] & fatiga['media'], gravedad['moderada'])

reglas = [regla1, regla2, regla3, regla4, regla5, regla6, regla7]
sistema_ctrl = ctrl.ControlSystem(reglas)


# ============================================================
# FUNCIÓN PRINCIPAL DE DIAGNÓSTICO
# ============================================================

def diagnosticar(temp, dol, fat):

    sim = ctrl.ControlSystemSimulation(sistema_ctrl)

    sim.input['temperatura'] = temp
    sim.input['dolor'] = dol
    sim.input['fatiga'] = fat

    sim.compute()

    valor = sim.output['gravedad']

    # ========================================================
    # CLASIFICACIÓN DEL RESULTADO
    # ========================================================

    if valor < 3.5:
        categoria = "Leve"
        recomendacion = "Reposo, hidratación y observación en casa."
    elif valor < 6.5:
        categoria = "Moderado"
        recomendacion = "Vigilar la evolución; considerar antipiréticos y consultar si empeora."
    else:
        categoria = "Grave"
        recomendacion = "Se recomienda buscar atención médica lo antes posible."

    # ========================================================
    # GRÁFICA DE LA FUNCIÓN DE MEMBRESÍA DE SALIDA
    # ========================================================

    gravedad.view(sim=sim)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    imagen = Image.open(buf)

    # ========================================================
    # RESULTADO
    # ========================================================

    resultado = f"""
#  Diagnóstico difuso

## Nivel de gravedad estimado: {valor:.2f} / 10

### Categoría: {categoria}

### Recomendación

{recomendacion}

---

### Datos ingresados

-  **Temperatura:** {temp} °C
-  **Dolor corporal:** {dol} / 10
-  **Fatiga:** {fat} / 10

---

El resultado fue calculado mediante lógica difusa tipo Mamdani
utilizando **scikit-fuzzy**, con {len(reglas)} reglas y centroide
como método de defuzzificación.
"""

    return resultado, imagen


# ============================================================
# INTERFAZ GRÁFICA
# ============================================================

with gr.Blocks(
    title="Sistema Difuso - Diagnóstico de Fiebre"
) as interfaz:

    gr.Markdown("""
    #  Sistema de Razonamiento Difuso para Diagnóstico de Fiebre

    Ingresa los síntomas y el sistema estimará el nivel de
    gravedad utilizando **scikit-fuzzy (SKFuzzy)**.
    """)

    with gr.Row():

        # ====================================================
        # PANEL DE ENTRADA
        # ====================================================

        with gr.Column():

            temp_input = gr.Slider(
                36, 41,
                value=37,
                step=0.1,
                label=" Temperatura corporal (°C)"
            )

            dolor_input = gr.Slider(
                0, 10,
                value=3,
                step=1,
                label=" Dolor corporal (0-10)"
            )

            fatiga_input = gr.Slider(
                0, 10,
                value=3,
                step=1,
                label=" Fatiga (0-10)"
            )

            boton = gr.Button(
                " Diagnosticar",
                variant="primary"
            )

        # ====================================================
        # PANEL DE RESULTADO
        # ====================================================

        with gr.Column():

            resultado_md = gr.Markdown("""
            ## Resultado

            Ajusta los valores y presiona **Diagnosticar**.
            """)

            grafica = gr.Image(label="Función de membresía de salida (gravedad)")

    # ========================================================
    # CONECTAR BOTÓN CON SISTEMA DIFUSO
    # ========================================================

    boton.click(
        fn=diagnosticar,
        inputs=[
            temp_input,
            dolor_input,
            fatiga_input
        ],
        outputs=[
            resultado_md,
            grafica
        ]
    )


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":
    interfaz.launch()