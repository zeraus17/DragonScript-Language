"""Tests de las funcionalidades v2 de DragonScript.

Cubre:
* Palabras clave en español (SENSAR, ESQUIVAR, ENTRENAR, GRAVEDAD, TECNICA,
  TRANSMITIR, FUSION, DESEO, INVERTIR, CANON, RELLENO, CAPSULA, ACTIVAR,
  EVOLUCIONA, YO, KI, SCOUTER).
* Recorrido enumerativo RASTREAR ... EN ... (foreach).
* Rangos [inicio..fin] y la función RANGO.
* Concatenación de grupos (listas) con '+'.
* Builtins de listas: ABSORBER, CABEZA, COLA, LONGITUD, ESTA_VACIA.
* Compatibilidad hacia atrás con las palabras en inglés.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dragonscript import run_source_capture
from dragonscript.errors import TypeErrorDS, RuntimeError_


class TestKeywordsEspanol(unittest.TestCase):
    def run_code(self, code):
        return run_source_capture(code)

    def test_ki_y_scouter(self):
        self.assertEqual(self.run_code('KI x = 5\nSCOUTER x'), "5\n")

    def test_sensar_esquivar(self):
        code = """
KI poder = 9000
SENSAR poder > 8000 {
    SCOUTER "fuerte"
} ESQUIVAR {
    SCOUTER "debil"
}
"""
        self.assertEqual(self.run_code(code), "fuerte\n")

    def test_esquivar_sensar_elseif(self):
        code = """
KI n = 2
SENSAR n == 1 {
    SCOUTER "uno"
} ESQUIVAR SENSAR n == 2 {
    SCOUTER "dos"
} ESQUIVAR {
    SCOUTER "otro"
}
"""
        self.assertEqual(self.run_code(code), "dos\n")

    def test_entrenar_while(self):
        code = """
KI c = 3
ENTRENAR c > 0 {
    SCOUTER c
    c -= 1
}
"""
        self.assertEqual(self.run_code(code), "3\n2\n1\n")

    def test_gravedad_repeticion(self):
        code = """
GRAVEDAD 3 {
    SCOUTER "ki"
}
"""
        self.assertEqual(self.run_code(code), "ki\nki\nki\n")

    def test_tecnica_transmitir(self):
        code = """
TECNICA doble(x) {
    TRANSMITIR x * 2
}
SCOUTER doble(21)
"""
        self.assertEqual(self.run_code(code), "42\n")

    def test_operadores_logicos_espanol(self):
        self.assertEqual(self.run_code("SCOUTER CANON FUSION CANON"), "TRUE\n")
        self.assertEqual(self.run_code("SCOUTER RELLENO DESEO CANON"), "TRUE\n")
        self.assertEqual(self.run_code("SCOUTER INVERTIR RELLENO"), "TRUE\n")

    def test_booleanos_y_null(self):
        self.assertEqual(self.run_code("SCOUTER CANON"), "TRUE\n")
        self.assertEqual(self.run_code("SCOUTER RELLENO"), "FALSE\n")
        self.assertEqual(self.run_code("SCOUTER VACIO"), "NULL\n")


class TestGuerreroEspanol(unittest.TestCase):
    def run_code(self, code):
        return run_source_capture(code)

    def test_guerrero_invocar_yo(self):
        code = """
CAPSULA Saiyajin {
    TECNICA __init__(nombre, poder) {
        YO.nombre = nombre
        YO.poder = poder
    }
    TECNICA describir() {
        TRANSMITIR YO.nombre + " -> " + YO.poder
    }
}
KI goku = ACTIVAR Saiyajin("Goku", 9001)
SCOUTER goku.describir()
"""
        self.assertEqual(self.run_code(code), "Goku -> 9001\n")

    def test_evoluciona_herencia(self):
        code = """
CAPSULA Saiyajin {
    TECNICA __init__(poder) {
        YO.poder = poder
    }
    TECNICA nivel() {
        TRANSMITIR YO.poder
    }
}
CAPSULA Super EVOLUCIONA Saiyajin {
    TECNICA __init__(poder) {
        Saiyajin.__init__(YO, poder * 10)
    }
}
KI g = ACTIVAR Super(5)
SCOUTER g.nivel()
"""
        self.assertEqual(self.run_code(code), "50\n")

    def test_campo_privado_via_yo(self):
        code = """
CAPSULA Caja {
    TECNICA __init__(v) {
        YO._secreto = v
    }
    TECNICA ver() {
        TRANSMITIR YO._secreto
    }
}
KI c = ACTIVAR Caja(7)
SCOUTER c.ver()
"""
        self.assertEqual(self.run_code(code), "7\n")


class TestRastrearYRangos(unittest.TestCase):
    def run_code(self, code):
        return run_source_capture(code)

    def test_rastrear_lista(self):
        code = """
RASTREAR g EN ["a", "b", "c"] {
    SCOUTER g
}
"""
        self.assertEqual(self.run_code(code), "a\nb\nc\n")

    def test_rastrear_texto(self):
        code = """
RASTREAR ch EN "abc" {
    SCOUTER ch
}
"""
        self.assertEqual(self.run_code(code), "a\nb\nc\n")

    def test_rango_inclusivo(self):
        self.assertEqual(self.run_code("SCOUTER [1..5]"), "[1, 2, 3, 4, 5]\n")

    def test_rango_vacio(self):
        self.assertEqual(self.run_code("SCOUTER [5..1]"), "[]\n")

    def test_rastrear_rango_acumulacion(self):
        code = """
KI total = 0
RASTREAR n EN [1..4] {
    total += n
}
SCOUTER total
"""
        self.assertEqual(self.run_code(code), "10\n")

    def test_rango_requiere_enteros(self):
        with self.assertRaises(TypeErrorDS):
            self.run_code('SCOUTER [1.5..3]')


class TestListas(unittest.TestCase):
    def run_code(self, code):
        return run_source_capture(code)

    def test_concat_listas(self):
        self.assertEqual(self.run_code("SCOUTER [1, 2] + [3, 4]"),
                         "[1, 2, 3, 4]\n")

    def test_absorber(self):
        self.assertEqual(self.run_code('SCOUTER ABSORBER([1, 2], 3)'),
                         "[1, 2, 3]\n")

    def test_cabeza(self):
        self.assertEqual(self.run_code('SCOUTER CABEZA([10, 20, 30])'), "10\n")

    def test_cola(self):
        self.assertEqual(self.run_code('SCOUTER COLA([10, 20, 30])'),
                         "[20, 30]\n")

    def test_longitud(self):
        self.assertEqual(self.run_code('SCOUTER LONGITUD([1, 2, 3])'), "3\n")

    def test_esta_vacia(self):
        self.assertEqual(self.run_code('SCOUTER ESTA_VACIA([])'), "TRUE\n")
        self.assertEqual(self.run_code('SCOUTER ESTA_VACIA([1])'), "FALSE\n")

    def test_rango_builtin(self):
        self.assertEqual(self.run_code('SCOUTER RANGO(2, 5)'),
                         "[2, 3, 4, 5]\n")

    def test_cabeza_lista_vacia_error(self):
        with self.assertRaises(TypeErrorDS):
            self.run_code('SCOUTER CABEZA([])')


class TestBackwardCompat(unittest.TestCase):
    def run_code(self, code):
        return run_source_capture(code)

    def test_ingles_sigue_funcionando(self):
        code = """
KI power = 9000
IF power > 8000 {
    SCOUTER "fuerte"
} ELSE {
    SCOUTER "debil"
}
"""
        self.assertEqual(self.run_code(code), "fuerte\n")

    def test_while_ingles(self):
        code = """
KI c = 2
WHILE c > 0 {
    SCOUTER c
    c -= 1
}
"""
        self.assertEqual(self.run_code(code), "2\n1\n")

    def test_technique_ingles(self):
        code = """
TECHNIQUE sq(x) {
    RETURN x * x
}
SCOUTER sq(5)
"""
        self.assertEqual(self.run_code(code), "25\n")

    def test_self_ingles(self):
        code = """
WARRIOR C {
    TECHNIQUE __init__(v) {
        SELF.v = v
    }
    TECHNIQUE get() {
        RETURN SELF.v
    }
}
KI o = CREATE C(9)
SCOUTER o.get()
"""
        self.assertEqual(self.run_code(code), "9\n")


class TestTablero(unittest.TestCase):
    """Tests del tablero estilo Gobstones (GUERRERO, VOLAR, esferas)."""

    def run_code(self, code):
        return run_source_capture(code)

    def test_posicion_inicial(self):
        code = """
INICIAR_TABLERO(3, 3)
SCOUTER STR(POSICION_X()) + "," + STR(POSICION_Y())
"""
        self.assertEqual(self.run_code(code), "0,0\n")

    def test_volar_norte_este(self):
        code = """
INICIAR_TABLERO(3, 3)
VOLAR(NORTE)
VOLAR(ESTE)
SCOUTER STR(POSICION_X()) + "," + STR(POSICION_Y())
"""
        self.assertEqual(self.run_code(code), "1,1\n")

    def test_cargar_y_cuantas(self):
        code = """
INICIAR_TABLERO(2, 2)
CARGAR(ESFERA_1)
CARGAR(ESFERA_1)
CARGAR(ESFERA_3)
SCOUTER STR(CUANTAS(ESFERA_1)) + "-" + STR(CUANTAS(ESFERA_3))
"""
        self.assertEqual(self.run_code(code), "2-1\n")

    def test_hay_esfera(self):
        code = """
INICIAR_TABLERO(2, 2)
SCOUTER STR(HAY(ESFERA_2))
CARGAR(ESFERA_2)
SCOUTER STR(HAY(ESFERA_2))
"""
        self.assertEqual(self.run_code(code), "FALSE\nTRUE\n")

    def test_drenar(self):
        code = """
INICIAR_TABLERO(2, 2)
CARGAR(ESFERA_4)
CARGAR(ESFERA_4)
DRENAR(ESFERA_4)
SCOUTER STR(CUANTAS(ESFERA_4))
"""
        self.assertEqual(self.run_code(code), "1\n")

    def test_puede_volar_borde(self):
        code = """
INICIAR_TABLERO(2, 2)
SCOUTER STR(PUEDE_VOLAR(SUR))
SCOUTER STR(PUEDE_VOLAR(NORTE))
"""
        self.assertEqual(self.run_code(code), "FALSE\nTRUE\n")

    def test_volar_contra_borde_falla(self):
        code = """
INICIAR_TABLERO(2, 2)
VOLAR(SUR)
"""
        with self.assertRaises(RuntimeError_):
            self.run_code(code)

    def test_drenar_vacio_falla(self):
        code = """
INICIAR_TABLERO(2, 2)
DRENAR(ESFERA_1)
"""
        with self.assertRaises(RuntimeError_):
            self.run_code(code)

    def test_esfera_invalida_falla(self):
        code = """
INICIAR_TABLERO(2, 2)
CARGAR("ESFERA_9")
"""
        with self.assertRaises(TypeErrorDS):
            self.run_code(code)

    def test_celdas_independientes(self):
        # Cada celda guarda sus propias esferas.
        code = """
INICIAR_TABLERO(2, 1)
CARGAR(ESFERA_1)
VOLAR(ESTE)
SCOUTER STR(CUANTAS(ESFERA_1))
"""
        self.assertEqual(self.run_code(code), "0\n")

    def test_recorrido_completo_cuenta(self):
        # Recorre todas las celdas y suma; 2x2 = 4 esferas.
        code = """
INICIAR_TABLERO(2, 2)
TECNICA sembrar() { CARGAR(ESFERA_1) }
sembrar()
VOLAR(ESTE)
sembrar()
VOLAR(NORTE)
sembrar()
VOLAR(OESTE)
sembrar()
KI total = CUANTAS(ESFERA_1)
VOLAR(ESTE)
total = total + CUANTAS(ESFERA_1)
VOLAR(SUR)
total = total + CUANTAS(ESFERA_1)
VOLAR(OESTE)
total = total + CUANTAS(ESFERA_1)
SCOUTER total
"""
        self.assertEqual(self.run_code(code), "4\n")

    def test_mostrar_tablero_incluye_guerrero(self):
        code = """
INICIAR_TABLERO(2, 2)
MOSTRAR_TABLERO()
"""
        salida = self.run_code(code)
        self.assertIn("GUERRERO", salida)
        self.assertIn("TABLERO 2x2", salida)


if __name__ == "__main__":
    unittest.main()
