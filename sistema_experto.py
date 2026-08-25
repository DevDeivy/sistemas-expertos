# ============================================================
# SISTEMA EXPERTO PARA RECOMENDACIÓN DE CARROS
# CLIPSpy + Gradio
# ============================================================

import clips
import gradio as gr


# ============================================================
# FUNCIÓN DEL SISTEMA EXPERTO
# ============================================================

def recomendar_carro(presupuesto, uso, pasajeros, prioridad):

    # Crear entorno CLIPS
    env = clips.Environment()

    # ========================================================
    # REGLAS DEL SISTEMA EXPERTO
    # ========================================================

    # REGLA 1
    env.build("""
    (defrule carro-economico-ciudad
        (presupuesto bajo)
        (uso ciudad)
        (pasajeros pocos)
        =>
        (assert (recomendacion "Kia Picanto"))
        (assert (motivo "Es un vehículo compacto, económico y adecuado para desplazamientos urbanos."))
    )
    """)

    # REGLA 2
    env.build("""
    (defrule carro-familiar
        (presupuesto medio)
        (uso familiar)
        (pasajeros muchos)
        =>
        (assert (recomendacion "Toyota Corolla Cross"))
        (assert (motivo "Ofrece espacio para la familia, comodidad y buena versatilidad para diferentes recorridos."))
    )
    """)

    # REGLA 3
    env.build("""
    (defrule carro-deportivo
        (presupuesto alto)
        (uso personal)
        (prioridad rendimiento)
        =>
        (assert (recomendacion "Mazda MX-5"))
        (assert (motivo "Es una opción orientada a quienes buscan una experiencia de conducción deportiva y dinámica."))
    )
    """)

    # REGLA 4
    env.build("""
    (defrule carro-ahorrador
        (presupuesto bajo)
        (prioridad ahorro)
        =>
        (assert (recomendacion "Renault Kwid"))
        (assert (motivo "Es una alternativa económica para usuarios que priorizan el ahorro y los costos de movilidad."))
    )
    """)

    # REGLA 5
    env.build("""
    (defrule carro-trabajo
        (presupuesto medio)
        (uso trabajo)
        (prioridad rendimiento)
        =>
        (assert (recomendacion "Toyota Hilux"))
        (assert (motivo "Es una alternativa robusta para trabajo y actividades que requieren mayor capacidad y resistencia."))
    )
    """)

    # REGLA 6
    env.build("""
    (defrule carro-familiar-ahorro
        (presupuesto medio)
        (uso familiar)
        (pasajeros muchos)
        (prioridad ahorro)
        =>
        (assert (recomendacion "Suzuki Ertiga"))
        (assert (motivo "Es una alternativa familiar que busca combinar espacio, practicidad y economía."))
    )
    """)

    # ========================================================
    # NORMALIZAR LOS DATOS
    # ========================================================

    presupuesto = presupuesto.lower()
    uso = uso.lower()
    pasajeros = pasajeros.lower()
    prioridad = prioridad.lower()

    # ========================================================
    # INSERTAR LOS HECHOS
    # ========================================================

    env.assert_string(f"(presupuesto {presupuesto})")
    env.assert_string(f"(uso {uso})")
    env.assert_string(f"(pasajeros {pasajeros})")
    env.assert_string(f"(prioridad {prioridad})")

    # ========================================================
    # EJECUTAR MOTOR DE INFERENCIA
    # ========================================================

    env.run()

    # ========================================================
    # OBTENER RESULTADO
    # ========================================================

    recomendacion = None
    motivo = None

    for fact in env.facts():

        if fact.template.name == "recomendacion":
            recomendacion = fact[0]

        elif fact.template.name == "motivo":
            motivo = fact[0]

    # ========================================================
    # MOSTRAR RESULTADO
    # ========================================================

    if recomendacion:

        resultado = f"""
#  Recomendación del Sistema Experto

## Vehículo recomendado

### {recomendacion}

### ¿Por qué?

{motivo}

---

### Características seleccionadas

-  **Presupuesto:** {presupuesto.capitalize()}
-  **Uso:** {uso.capitalize()}
-  **Pasajeros:** {pasajeros.capitalize()}
-  **Prioridad:** {prioridad.capitalize()}

---

La recomendación fue generada mediante un conjunto de reglas
utilizando **CLIPSpy** y su motor de inferencia.
"""

        return resultado

    else:

        return """
#  No se encontró una recomendación

El sistema no encontró una regla que coincida exactamente
con las características seleccionadas.

Prueba con otra combinación de opciones.
"""


# ============================================================
# INTERFAZ GRÁFICA
# ============================================================

with gr.Blocks(
    title="Sistema Experto - Recomendación de Carros"
) as interfaz:

    gr.Markdown("""
    #  Sistema Experto para Recomendar Carros

    Selecciona las características del vehículo que necesitas
    y el sistema experto analizará las opciones utilizando
    **CLIPSpy**.
    """)

    with gr.Row():

        # ====================================================
        # PANEL DE ENTRADA
        # ====================================================

        with gr.Column():

            presupuesto = gr.Dropdown(
                choices=[
                    "bajo",
                    "medio",
                    "alto"
                ],
                label=" Presupuesto",
                value="medio"
            )

            uso = gr.Dropdown(
                choices=[
                    "ciudad",
                    "familiar",
                    "personal",
                    "trabajo"
                ],
                label=" Uso principal",
                value="ciudad"
            )

            pasajeros = gr.Dropdown(
                choices=[
                    "pocos",
                    "muchos"
                ],
                label=" Número de pasajeros",
                value="pocos"
            )

            prioridad = gr.Dropdown(
                choices=[
                    "ahorro",
                    "rendimiento"
                ],
                label=" Prioridad",
                value="ahorro"
            )

            boton = gr.Button(
                "🚗 Recomendar carro",
                variant="primary"
            )

        # ====================================================
        # PANEL DE RESULTADO
        # ====================================================

        with gr.Column():

            resultado = gr.Markdown("""
            ## Resultado

            Selecciona las características del carro que buscas
            y presiona **Recomendar carro**.
            """)

    # ========================================================
    # CONECTAR BOTÓN CON SISTEMA EXPERTO
    # ========================================================

    boton.click(
        fn=recomendar_carro,
        inputs=[
            presupuesto,
            uso,
            pasajeros,
            prioridad
        ],
        outputs=resultado
    )


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":
    interfaz.launch()