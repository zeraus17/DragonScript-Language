# 🔍 Ejercicio: Análisis de Niveles de Poder

## 📋 Descripción

Tienes una lista de niveles de poder de guerreros. Debes crear funciones simples que recorran la lista y obtengan información útil.

## 🎯 Objetivos

Implementa las siguientes 5 funciones usando **RASTREAR** (foreach):

### 1\. `sumarPoderes(poderes)`

Recorre la lista y suma todos los niveles de poder.

**Pista:** Usa una variable acumuladora (KI suma = 0).

**Ejemplo:**

```
sumarPoderes([100, 200, 300]) → 600
```

### 2\. `contarFuertes(poderes, minimo)`

Cuenta cuántos guerreros tienen un poder mayor o igual al mínimo.

**Pista:** Variable contador que incrementas cuando encuentras uno fuerte.

**Ejemplo:**

```
contarFuertes([100, 500, 200, 600], 300) → 2
```

### 3\. `encontrarMaximo(poderes)`

Encuentra el nivel de poder más alto de la lista.

**Pista:** Mantén una variable con el máximo encontrado hasta ahora.

**Ejemplo:**

```
encontrarMaximo([100, 500, 200]) → 500
```

### 4\. `mostrarTodos(poderes)`

Recorre e imprime cada poder con su posición.

**Formato de salida:**

```
Guerrero 1: 9000
Guerrero 2: 8500
Guerrero 3: 7000
```

**Pista:** Usa un contador que incrementas en cada iteración.

### 5\. `duplicarPoderes(poderes)`

Crea una nueva lista donde cada poder esté duplicado (multiplicado por 2).

**Pista:** Crea lista vacía, usa ABSORBER para agregar cada poder duplicado.

**Ejemplo:**

```
duplicarPoderes([100, 200, 300]) → [200, 400, 600]
```

## 💡 Conceptos que Practicarás

* ✅ Recorrido con RASTREAR

* ✅ Variables acumuladoras (suma, contador)

* ✅ Búsqueda de máximo

* ✅ Construcción de nuevas listas

* ✅ Condicionales dentro de recorridos

## 📝 Ejemplo de Uso

```dragonscript
KI poderes = [9000, 8500, 7000, 4500, 10000]

SCOUTER("Suma total: " + STR(sumarPoderes(poderes)))
SCOUTER("Guerreros fuertes (>=5000): " + STR(contarFuertes(poderes, 5000)))
SCOUTER("Poder máximo: " + STR(encontrarMaximo(poderes)))

mostrarTodos(poderes)

KI duplicados = duplicarPoderes(poderes)
SCOUTER("Poderes duplicados: ")
mostrarTodos(duplicados)
```

## 🎓 Nivel de Dificultad

**Básico** - Ideal para practicar las lecciones 11 (Recorrido y Acumulación) y 13 (Recorridos Enumerativos).

## ✨ Estructura Básica de RASTREAR

Todas las funciones usan este patrón:

```dragonscript
TECNICA miFuncion(lista) {
    KI resultado = 0  # o [], o VACIO según necesites
    
    RASTREAR elemento EN lista {
        # Procesar cada elemento
        resultado = resultado + elemento
    }
    
    TRANSMITIR resultado
}
```

---

¡Es simple pero muy útil para dominar los recorridos! 🐉