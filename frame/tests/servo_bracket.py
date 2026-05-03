
from build123d import *
from ocp_vscode import show

with BuildPart() as part:
    length = 80
    width  = 20
    height = 5
    Box(length, width, height)

    # Отверстия под крепежные винты
    points = [
        (-35, 5, 0),
        (-35, -5, 0),
        (-25, 5, 0),
        (-25, -5, 0),
    ]
    for point in points:
        with BuildPart(Location(point), mode=Mode.SUBTRACT):
            radius = 1.2
            height = 5
            align  = (Align.CENTER, Align.CENTER, Align.CENTER)
            Cylinder(radius, height, align=align)

    # Выемка под болт крепления серво
    x = -30
    y = 0
    z = 0
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        radius = 3.5
        height = 5
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Cylinder(radius, height, align=align)

    roundable_edges = part.edges().filter_by(Axis.Z)
    fillet(roundable_edges, radius=9)

filename = f'{__file__[:-3]}'

show(part.part, names=[filename])
export_stl(part.part, f'{filename}.stl')
