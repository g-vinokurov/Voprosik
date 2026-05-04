from build123d import *
from ocp_vscode import show

with BuildPart() as результат:
    Cylinder(10, 30)                                           # вертикальный
    with BuildPart(mode=Mode.INTERSECT):
        Cylinder(6, 40, rotation=(90, 0, 0), align=Align.CENTER)  # горизонтальный

show(результат)