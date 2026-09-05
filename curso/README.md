# 🐉 Curso de Programación con DragonScript

Este curso te enseña a **programar desde cero** usando DragonScript, un
lenguaje temático de Dragon Ball donde las palabras clave están en español.

La secuencia de conceptos sigue el enfoque pedagógico del curso de
**Introducción a la Programación (estilo Gobstones, UNQ)**: cada lección
introduce **una idea nueva** apoyándose en las anteriores. No hace falta
saber nada de programación para empezar.

---

## ▶️ Cómo ejecutar una lección

En Windows, abrí una terminal en la carpeta del proyecto y escribí:

```
python main.py examples\curso\01_programas.ds
```

Cambiá el número/nombre del archivo para correr otra lección. También podés
abrir el proyecto en **Visual Studio Code** y apretar **F5** (ver la guía
`EJECUTAR_F5.pdf` en la raíz del proyecto).

---

## 📚 Orden recomendado de las lecciones

| # | Archivo | Concepto que aprendés |
|---|---------|-----------------------|
| 01 | `01_programas.ds` | Qué es un programa. Mostrar cosas con `SCOUTER`. Comentarios. |
| 02 | `02_procedimientos.ds` | Procedimientos (`TECNICA`) y contratos (qué promete cada uno). |
| 03 | `03_repeticion_simple.ds` | Repetir una cantidad fija de veces con `GRAVEDAD`. |
| 04 | `04_parametros.ds` | Pasarle datos a un procedimiento con parámetros. |
| 05 | `05_expresiones_tipos.ds` | Expresiones y tipos: números, textos, booleanos, `VACIO`. |
| 06 | `06_alternativa_condicional.ds` | Decidir con `SENSAR` / `ESQUIVAR` / `ESQUIVAR SENSAR`. |
| 07 | `07_funciones_simples.ds` | Funciones que devuelven un valor con `TRANSMITIR`. |
| 08 | `08_repeticion_condicional.ds` | Repetir mientras algo se cumpla con `ENTRENAR`. |
| 09 | `09_variables.ds` | Variables con `KI`: guardar y cambiar valores. Acumuladores. |
| 10 | `10_funciones_con_procesamiento.ds` | Funciones con lógica interna (mayor, factorial...). |
| 11 | `11_recorrido_acumulacion.ds` | Recorrer un grupo con `RASTREAR` y acumular. |
| 12 | `12_busqueda.ds` | Buscar sabiendo que está y sin saber si está. |
| 13 | `13_recorridos_enumerativos.ds` | Recorrer rangos de números `[1..10]`. |
| 14 | `14_registros.ds` | Registros y variantes con `CAPSULA`: crear, acceder, modificar campos. |
| 15 | `15_listas.ds` | Listas y sus funciones (`CABEZA`, `COLA`, `ABSORBER`, `LONGITUD`...). |
| 16 | `16_procesamiento_listas.ds` | Transformar, filtrar y reducir listas. |
| 17 | `17_tablero.ds` | El Tablero estilo Gobstones: el cabezal `GUERRERO`, esferas y direcciones. |
| 18 | `18_recorrido_tablero.ds` | Recorrer todas las celdas de un tablero fila por fila. |

---

## 🈹 Mini-diccionario de palabras clave

Todas las palabras del lenguaje son del universo Dragon Ball y están en
español. Estas son las que usa el curso:

| Palabra | Significa | Ejemplo |
|---------|-----------|---------|
| `KI` | declarar una variable | `KI poder = 9000` |
| `SCOUTER` | mostrar en pantalla | `SCOUTER "Hola"` |
| `SENSAR` | si (condición) | `SENSAR x > 5 { ... }` |
| `ESQUIVAR` | si no (else) | `ESQUIVAR { ... }` |
| `ENTRENAR` | mientras (while) | `ENTRENAR x > 0 { ... }` |
| `GRAVEDAD` | repetir N veces | `GRAVEDAD 3 { ... }` |
| `RASTREAR ... EN` | recorrer cada elemento | `RASTREAR x EN grupo { ... }` |
| `TECNICA` | definir función/procedimiento | `TECNICA saludar() { ... }` |
| `TRANSMITIR` | devolver un valor (return) | `TRANSMITIR x * 2` |
| `CAPSULA` | definir un registro/clase | `CAPSULA Peleador { ... }` |
| `ACTIVAR` | crear un registro/objeto | `ACTIVAR Peleador(...)` |
| `EVOLUCIONA` | heredar de otro guerrero | `CAPSULA A EVOLUCIONA B { ... }` |
| `YO` | el propio registro (self) | `YO.nombre = nombre` |
| `FUSION` / `DESEO` / `INVERTIR` | y / o / no | `a > 0 FUSION b > 0` |
| `CANON` / `RELLENO` / `VACIO` | verdadero / falso / nulo | `SENSAR listo == CANON` |

---

## 🎯 Comandos del Tablero (lecciones 17-18)

El tablero es una grilla estilo Gobstones. `GUERRERO` es el cabezal.

| Palabra | Significa | Ejemplo |
|---------|-----------|---------|
| `INICIAR_TABLERO` | crear un tablero (ancho, alto) | `INICIAR_TABLERO(4, 3)` |
| `GUERRERO` | el cabezal del tablero | — |
| `NORTE` / `SUR` / `ESTE` / `OESTE` | direcciones | `VOLAR(NORTE)` |
| `ESFERA_1` ... `ESFERA_4` | los cuatro tipos de esfera | `CARGAR(ESFERA_1)` |
| `VOLAR` | mover el cabezal | `VOLAR(ESTE)` |
| `PUEDE_VOLAR` | ¿se puede mover sin caerse? | `SENSAR PUEDE_VOLAR(ESTE) { ... }` |
| `CARGAR` / `DRENAR` | poner / sacar una esfera | `CARGAR(ESFERA_2)` |
| `HAY` / `CUANTAS` | ¿hay? / ¿cuántas? | `CUANTAS(ESFERA_1)` |
| `POSICION_X` / `POSICION_Y` | columna / fila del cabezal | `POSICION_X()` |
| `MOSTRAR_TABLERO` | dibujar el tablero | `MOSTRAR_TABLERO()` |

---

## 💪 Funciones para listas

| Función | Qué hace |
|---------|----------|
| `LONGITUD(lista)` | cuántos elementos tiene |
| `ESTA_VACIA(lista)` | `CANON` si no tiene elementos |
| `CABEZA(lista)` | el primer elemento |
| `COLA(lista)` | todos menos el primero |
| `ABSORBER(lista, x)` | una lista nueva con `x` al final |
| `RANGO(a, b)` | la lista `[a, a+1, ..., b]` |

¡A entrenar! 🔥
