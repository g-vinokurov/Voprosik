
from build123d import *
from ocp_vscode import show

with BuildPart() as part:
    length = 60
    width  = 60
    height = 20
    Box(length, width, height)
    
    # Скругленный край около оси вращения
    x = 0
    y = -30
    z = 0
    with BuildPart(Location((x, y, z))):
        radius = 10
        height = 60
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Cylinder(radius, height, align=align, rotation=(0, 90, 0))
    
    # Вырез внутренности
    x = 0
    y = -22.5
    z = 0
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        length = 50
        width  = 55
        height = 20
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x = -27
    y = 27
    z = 0
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        length = 6
        width  = 6
        height = 20
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x = 27
    y = 27
    z = 0
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        length = 6
        width  = 6
        height = 20
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x = 0
    y = 15
    z = 0
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        length = 42
        width  = 22
        height = 20
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    # Скругления у сустава
    x = 24
    y = 24
    z = 0
    with BuildPart(Location((x, y, z))):
        radius = 6
        height = 20
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Cylinder(radius, height, align=align)
    
    x = -24
    y = 24
    z = 0
    with BuildPart(Location((x, y, z))):
        radius = 6
        height = 20
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Cylinder(radius, height, align=align)
    
    # Ещё раз вырез
    x = 0
    y = 15
    z = 0
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        length = 42
        width  = 22
        height = 20
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    # Отверстия под крепежные винты 3 mm
    points = [
        (0, -10, 0),
        (0, -6,  0),
    ]
    for point in points:
        with BuildPart(Location(point), mode=Mode.SUBTRACT):
            radius = 1.5
            height = 60
            align  = (Align.CENTER, Align.CENTER, Align.CENTER)
            Cylinder(radius, height, align=align, rotation=(0, 90, 0))

    # Выемка под болт крепления серво
    x = 0
    y = -30
    z = 0
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        radius = 3.5
        height = 60
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Cylinder(radius, height, align=align, rotation=(0, 90, 0))
    
    # Отверстия под крепежные винты 3 mm
    points = [
        (24, 20, 0),
        (24, 10, 0),
        (-24, 20, 0),
        (-24, 10, 0),
    ]
    for point in points:
        with BuildPart(Location(point), mode=Mode.SUBTRACT):
            radius = 1.5
            height = 20
            align  = (Align.CENTER, Align.CENTER, Align.CENTER)
            Cylinder(radius, height, align=align)
    
    roundable_edges = part.edges().filter_by(Axis.Z)
    fillet(roundable_edges, radius=1)

filename = f'{__file__[:-3]}'

show(part.part, names=[filename])
export_stl(part.part, f'{filename}.stl')
