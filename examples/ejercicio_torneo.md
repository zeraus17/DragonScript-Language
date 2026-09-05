# 🥋 Ejercicio: Torneo de Artes Marciales

## 📋 Descripción

El **Torneo de Artes Marciales** necesita un sistema para gestionar los participantes. Debes crear un programa en DragonScript que ayude a organizar el torneo.

## 🎯 Objetivos

Primero, define una clase con `CAPSULA` llamada `Participante` con estos campos:
- `nombre`: nombre del participante
- `poder`: nivel de poder
- `raza`: raza del guerrero (ej: "Saiyajin", "Humano", "Namekiano")
- `victorias`: contador de victorias (iniciar en 0)

**Sintaxis:**
```dragonscript
CAPSULA Participante {
    TECNICA __init__(nombre, poder, raza) {
        YO.nombre = nombre
        # ... completa el resto
    }
}
```

Luego, implementa las siguientes funciones (TECNICA) para gestionar el torneo:

### 1. `registrarGuerrero(nombre, poder, raza)`
Crea y retorna un CAPSULA usando `ACTIVAR Participante(...)`.

**Sintaxis:**
```dragonscript
TRANSMITIR ACTIVAR Participante(nombre, poder, raza)
```

### 2. `mostrarGuerrero(guerrero)`
Imprime (SCOUTER) la información completa de un guerrero en formato legible.

Ejemplo de salida:
```
=== GOKU ===
Poder: 9000
Raza: Saiyajin
Victorias: 5
```

### 3. `guerreroMasFuerte(guerreros)`
Recibe una lista de guerreros y retorna el que tiene mayor nivel de poder.

**Pista:** Usa RASTREAR para recorrer la lista y mantén una variable con el máximo.

### 4. `filtrarPorPoderMinimo(guerreros, minimo)`
Retorna una nueva lista con solo los guerreros que tienen un nivel de poder mayor o igual al mínimo especificado.

**Pista:** Crea una lista vacía y usa ABSORBER para agregar los que cumplan la condición.

### 5. `promedioPoderTotal(guerreros)`
Calcula y retorna el promedio del nivel de poder de todos los guerreros.

**Pista:** Acumula la suma con RASTREAR y divide por LONGITUD.

### 6. `simularCombate(g1, g2)`
Simula un combate entre dos guerreros. El que tiene mayor poder gana y aumenta sus victorias en 1.

Imprime quién ganó y retorna al ganador.

## 🧪 Programa Principal

Tu programa debe:

1. Crear una lista con al menos 5 guerreros del torneo
2. Mostrar todos los guerreros inscritos
3. Encontrar y mostrar al guerrero más fuerte
4. Filtrar guerreros con poder >= 5000 y mostrarlos
5. Calcular y mostrar el promedio de poder del torneo
6. Simular 3 combates entre diferentes guerreros
7. Mostrar el estado final de todos los guerreros

## 💡 Conceptos que Practicarás

- ✅ Registros (CAPSULA, ACTIVAR, YO)
- ✅ Listas y manipulación
- ✅ Iteración con RASTREAR
- ✅ Funciones con parámetros y retorno (TECNICA, TRANSMITIR)
- ✅ Variables acumuladoras (KI)
- ✅ Búsqueda y filtrado
- ✅ Condicionales (SENSAR/ESQUIVAR)

## 📝 Ejemplo de Salida Esperada

```
🥋 TORNEO DE ARTES MARCIALES 🥋

=== Guerreros Inscritos ===
=== GOKU ===
Poder: 9000
Raza: Saiyajin
Victorias: 0

=== VEGETA ===
Poder: 8500
Raza: Saiyajin
Victorias: 0

... (más guerreros)

🏆 Guerrero más fuerte: GOKU (Poder: 9000)

💪 Guerreros elite (poder >= 5000):
=== GOKU ===
... (lista filtrada)

📊 Promedio de poder: 6250

⚔️ COMBATES:
GOKU vs VEGETA → ¡GOKU gana!
...

=== Estado Final del Torneo ===
... (mostrar todos con sus victorias actualizadas)
```

## 🚀 ¿Cómo Empezar?

1. Copia la plantilla de `ejercicio_torneo_plantilla.ds`
2. Implementa cada función paso a paso
3. Prueba cada función antes de continuar con la siguiente
4. Ejecuta: `python main.py examples/ejercicio_torneo_plantilla.ds`

## 🎓 Nivel de Dificultad

**Intermedio** - Requiere dominio de las lecciones 1-15 del curso.

## ✨ Desafío Extra (Opcional)

- Crea una función `rankingGuerreros(guerreros)` que ordene la lista por número de victorias (mayor a menor)
- Implementa un sistema de "mejor de 3" combates
- Agrega un campo `tecnica_especial` a cada guerrero y úsalo en los combates

---

¡Buena suerte, guerrero! 🐉
