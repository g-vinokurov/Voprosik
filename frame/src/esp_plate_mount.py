# Код позаимствован из проекта робота T-1337
# Форма АКБ вписывается в отсек для АКБ того проекта
# Лишние элементы были удалены

from build123d import *
from ocp_vscode import show

unit_size           = 8.0 # lego unit size
unit_height         = 9.6 # lego brick height


with BuildPart() as part:
    # База
    length = unit_size * 8
    width  = unit_size * 8
    height = unit_height
    Box(length, width, height)

    # Вырезы
    x = 19
    y = 32 - 3
    z = 0
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        length = 26
        width  = 6
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x = 19
    y = -32 + 3
    z = 0
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        length = 26
        width  = 6
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x = -22
    y = 0
    z = 0
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        length = 20
        width  = 64
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)

    # Отверстия под крепежные винты (3 mm)
    points = [
        # Arduino Uno
        (-36 + 4 + 32, 27.5, 0),
        (-36 + 4 + 31, -20.9, 0),
    ]
    for point in points:
        with BuildPart(Location(point), mode=Mode.SUBTRACT):
            radius = 1.5
            height = unit_height * 10
            align  = (Align.CENTER, Align.CENTER, Align.CENTER)
            Cylinder(radius, height, align=align)
    
    # Утоплялки под крепежные винты (3 mm)
    z_pos = unit_height / 2 - 1.5
    points = [
        (-36 + 4 + 32, 27.5, z_pos),
        (-36 + 4 + 31, -20.9, z_pos),
    ]
    for point in points:
        with BuildPart(Location(point), mode=Mode.SUBTRACT):
            radius = 3
            height = 3
            align  = (Align.CENTER, Align.CENTER, Align.CENTER)
            Cylinder(radius, height, align=align)
    

    # Отверстия под крепежные винты (2 mm)
    points = [
        # ESP Plate (50 mm x 70 mm)
        (29,  23, 0),
        (29,  -23, 0),
    ]
    for point in points:
        with BuildPart(Location(point), mode=Mode.SUBTRACT):
            radius = 1
            height = unit_height * 10
            align  = (Align.CENTER, Align.CENTER, Align.CENTER)
            Cylinder(radius, height, align=align)
    
    # Утоплялки под крепежные винты
    z_pos = -unit_height / 2 + 1
    points = [
        (29,  23, z_pos),
        (29,  -23, z_pos),
    ]
    for point in points:
        with BuildPart(Location(point), mode=Mode.SUBTRACT):
            radius = 2
            height = 2
            align  = (Align.CENTER, Align.CENTER, Align.CENTER)
            Cylinder(radius, height, align=align)

    roundable_edges = part.edges().filter_by(Axis.Z)
    fillet(roundable_edges, radius=2)

filename = f'{__file__.rstrip('.py')}'

show(part.part, names=[filename])
export_stl(part.part, f'{filename}.stl')
