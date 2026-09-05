# test_tablero.py
from dragonscript.gui_tablero import TableroGUI

# 1. Creamos un tablero de 3x3
gui = TableroGUI(ancho=3, alto=3)

# 2. Estado inicial: Guerrero en (0,0)
gui.renderizar(guerrero_pos=(0, 0), celdas={})

# 3. Simulamos meter una esfera en (0,0)
gui.renderizar(guerrero_pos=(0, 0), celdas={(0, 0): {"ESFERA_1": 1}})

# 4. Mover al NORTE -> (0,1)
gui.renderizar(guerrero_pos=(0, 1), celdas={(0, 0): {"ESFERA_1": 1}})

# 5. Mover al ESTE -> (1,1) y cargar otra esfera
gui.renderizar(
    guerrero_pos=(1, 1), 
    celdas={(0, 0): {"ESFERA_1": 1}, (1, 1): {"ESFERA_2": 1}}
)

# 6. Mantiene la ventana abierta para ver el resultado final
gui.mantener_abierto()