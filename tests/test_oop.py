"""Tests de la Programación Orientada a Objetos (POO) de DragonScript.

Cubre: clases y objetos, constructor, métodos, atributos de instancia y de
clase, métodos estáticos, encapsulación (miembros privados), herencia simple
y múltiple (MRO), sobrecarga de operadores y __str__.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dragonscript import run_source_capture
from dragonscript.errors import (RuntimeError_, TypeErrorDS, ArgumentError)


class TestOOP(unittest.TestCase):
    def run_code(self, code):
        return run_source_capture(code)

    # --------------------------------------------------- clases y objetos
    def test_clase_basica_y_metodo(self):
        code = """
WARRIOR Saiyan {
    TECHNIQUE __init__(name) {
        SELF.name = name
    }
    TECHNIQUE saludar() {
        SCOUTER "Hola, soy " + SELF.name
    }
}
KI g = CREATE Saiyan("Goku")
g.saludar()
"""
        self.assertEqual(self.run_code(code), "Hola, soy Goku\n")

    def test_atributo_de_instancia(self):
        code = """
WARRIOR C {
    TECHNIQUE __init__(x) { SELF.x = x }
}
KI c = CREATE C(42)
SCOUTER c.x
"""
        self.assertEqual(self.run_code(code), "42\n")

    def test_constructor_valida_argumentos(self):
        code = """
WARRIOR C {
    TECHNIQUE __init__(a) { SELF.a = a }
}
KI c = CREATE C(1, 2)
"""
        with self.assertRaises(ArgumentError):
            self.run_code(code)

    def test_create_sin_constructor_con_args_falla(self):
        code = """
WARRIOR C { }
KI c = CREATE C(1)
"""
        with self.assertRaises(ArgumentError):
            self.run_code(code)

    def test_create_de_no_clase_falla(self):
        code = """
KI x = 5
KI y = CREATE x()
"""
        with self.assertRaises(TypeErrorDS):
            self.run_code(code)

    # ------------------------------------------------ atributos de clase
    def test_atributo_de_clase_compartido(self):
        code = """
WARRIOR C {
    planeta = "Tierra"
    TECHNIQUE __init__() { SELF.x = 1 }
}
KI a = CREATE C()
SCOUTER a.planeta
SCOUTER C.planeta
"""
        self.assertEqual(self.run_code(code), "Tierra\nTierra\n")

    def test_metodo_estatico(self):
        code = """
WARRIOR C {
    STATIC TECHNIQUE especie() { RETURN "saiyan" }
}
SCOUTER C.especie()
"""
        self.assertEqual(self.run_code(code), "saiyan\n")

    def test_metodo_estatico_desde_instancia(self):
        code = """
WARRIOR C {
    STATIC TECHNIQUE especie() { RETURN "saiyan" }
    TECHNIQUE __init__() { SELF.x = 1 }
}
KI c = CREATE C()
SCOUTER c.especie()
"""
        self.assertEqual(self.run_code(code), "saiyan\n")

    # ------------------------------------------------------ encapsulación
    def test_miembro_privado_no_accesible_fuera(self):
        code = """
WARRIOR C {
    TECHNIQUE __init__() { SELF._secret = 42 }
}
KI c = CREATE C()
SCOUTER c._secret
"""
        with self.assertRaises(RuntimeError_):
            self.run_code(code)

    def test_miembro_privado_accesible_via_self(self):
        code = """
WARRIOR C {
    TECHNIQUE __init__() { SELF._secret = 42 }
    TECHNIQUE reveal() { RETURN SELF._secret }
}
KI c = CREATE C()
SCOUTER c.reveal()
"""
        self.assertEqual(self.run_code(code), "42\n")

    def test_asignar_miembro_privado_fuera_falla(self):
        code = """
WARRIOR C {
    TECHNIQUE __init__() { SELF._x = 1 }
}
KI c = CREATE C()
c._x = 2
"""
        with self.assertRaises(RuntimeError_):
            self.run_code(code)

    # --------------------------------------------------- herencia simple
    def test_herencia_simple(self):
        code = """
WARRIOR Animal {
    TECHNIQUE sonido() { RETURN "..." }
    TECHNIQUE describir() { RETURN "hace " + SELF.sonido() }
}
WARRIOR Perro EVOLVES Animal {
    TECHNIQUE sonido() { RETURN "guau" }
}
KI p = CREATE Perro()
SCOUTER p.describir()
"""
        self.assertEqual(self.run_code(code), "hace guau\n")

    def test_llamada_constructor_padre(self):
        code = """
WARRIOR Base {
    TECHNIQUE __init__(x) { SELF.x = x }
}
WARRIOR Hija EVOLVES Base {
    TECHNIQUE __init__(x, y) {
        Base.__init__(SELF, x)
        SELF.y = y
    }
}
KI h = CREATE Hija(1, 2)
SCOUTER h.x
SCOUTER h.y
"""
        self.assertEqual(self.run_code(code), "1\n2\n")

    def test_evolves_de_no_clase_falla(self):
        code = """
KI x = 5
WARRIOR C EVOLVES x { }
"""
        with self.assertRaises(TypeErrorDS):
            self.run_code(code)

    # ------------------------------------------------- herencia múltiple
    def test_herencia_multiple_mro(self):
        code = """
WARRIOR A { TECHNIQUE m() { RETURN "A" } }
WARRIOR B { TECHNIQUE m() { RETURN "B" } TECHNIQUE n() { RETURN "n-B" } }
WARRIOR C EVOLVES A, B {
    TECHNIQUE __init__() { SELF.x = 1 }
}
KI c = CREATE C()
SCOUTER c.m()
SCOUTER c.n()
"""
        # m() se resuelve primero en A (aparece antes en EVOLVES).
        self.assertEqual(self.run_code(code), "A\nn-B\n")

    # ----------------------------------------- sobrecarga de operadores
    def test_sobrecarga_suma(self):
        code = """
WARRIOR Vec {
    TECHNIQUE __init__(v) { SELF.v = v }
    TECHNIQUE __add__(other) { RETURN CREATE Vec(SELF.v + other.v) }
}
KI a = CREATE Vec(3)
KI b = CREATE Vec(4)
KI c = a + b
SCOUTER c.v
"""
        self.assertEqual(self.run_code(code), "7\n")

    def test_sobrecarga_comparaciones(self):
        code = """
WARRIOR N {
    TECHNIQUE __init__(v) { SELF.v = v }
    TECHNIQUE __gt__(o) { RETURN SELF.v > o.v }
    TECHNIQUE __eq__(o) { RETURN SELF.v == o.v }
}
KI a = CREATE N(10)
KI b = CREATE N(5)
KI c = CREATE N(10)
IF a > b { SCOUTER "mayor" }
IF a == c { SCOUTER "igual" }
"""
        self.assertEqual(self.run_code(code), "mayor\nigual\n")

    def test_neq_derivado_de_eq(self):
        code = """
WARRIOR N {
    TECHNIQUE __init__(v) { SELF.v = v }
    TECHNIQUE __eq__(o) { RETURN SELF.v == o.v }
}
KI a = CREATE N(1)
KI b = CREATE N(2)
IF a != b { SCOUTER "distintos" }
"""
        self.assertEqual(self.run_code(code), "distintos\n")

    # ---------------------------------------------------------- __str__
    def test_str_personalizado(self):
        code = """
WARRIOR P {
    TECHNIQUE __init__(n) { SELF.n = n }
    TECHNIQUE __str__() { RETURN "P<" + SELF.n + ">" }
}
KI p = CREATE P("goku")
SCOUTER p
"""
        self.assertEqual(self.run_code(code), "P<goku>\n")

    def test_str_por_defecto(self):
        code = """
WARRIOR P {
    TECHNIQUE __init__(n) { SELF.n = n }
}
KI p = CREATE P("goku")
SCOUTER p
"""
        self.assertEqual(self.run_code(code), "<P n=goku>\n")

    # ------------------------------------------------- errores de acceso
    def test_propiedad_inexistente_falla(self):
        code = """
WARRIOR C { TECHNIQUE __init__() { SELF.x = 1 } }
KI c = CREATE C()
SCOUTER c.y
"""
        with self.assertRaises(RuntimeError_):
            self.run_code(code)


if __name__ == "__main__":
    unittest.main()
