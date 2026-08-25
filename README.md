# 🚗 Sistema Experto para Recomendación de Carros

## Descripción

Este proyecto consiste en un sistema experto desarrollado en Python utilizando la librería CLIPSpy.

El sistema tiene como objetivo recomendar un carro de acuerdo con las necesidades del usuario.

Para realizar la recomendación se analizan cuatro características:

- Presupuesto.
- Uso principal.
- Número de pasajeros.
- Prioridad del usuario.

A partir de estos datos, el sistema utiliza reglas de inferencia para generar una recomendación.

---

## Tecnologías utilizadas

- Python
- CLIPSpy
- Gradio
- Git
- GitHub

---

## CLIPSpy

CLIPSpy es una librería de Python que permite trabajar con el motor de reglas CLIPS.

En este proyecto CLIPSpy permite:

1. Crear el entorno de CLIPS.
2. Definir las reglas.
3. Insertar los hechos.
4. Ejecutar el motor de inferencia.
5. Obtener la recomendación generada.

---

## Reglas

El sistema contiene 6 reglas:

### Regla 1
Presupuesto bajo + ciudad + pocos pasajeros → Kia Picanto.

### Regla 2
Presupuesto medio + familiar + muchos pasajeros → Toyota Corolla Cross.

### Regla 3
Presupuesto alto + uso personal + prioridad rendimiento → Mazda MX-5.

### Regla 4
Presupuesto bajo + prioridad ahorro → Renault Kwid.

### Regla 5
Presupuesto medio + trabajo + prioridad rendimiento → Toyota Hilux.

### Regla 6
Presupuesto medio + familiar + muchos pasajeros + prioridad ahorro → Suzuki Ertiga.

---

## Interfaz gráfica

La interfaz gráfica fue desarrollada utilizando Gradio.

El usuario selecciona:

- Presupuesto.
- Uso principal.
- Número de pasajeros.
- Prioridad.

Después presiona el botón de recomendación.

La información se envía al sistema experto, donde CLIPSpy analiza las reglas y genera una conclusión.

---

## Arquitectura

```text
Usuario
   ↓
Interfaz Gradio
   ↓
Características del usuario
   ↓
Hechos CLIPS
   ↓
Reglas
   ↓
Motor de inferencia
   ↓
Recomendación
   ↓
Interfaz gráfica