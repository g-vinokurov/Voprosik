# Код позаимствован из проекта робота T-1337
# Форма АКБ вписывается в отсек для АКБ того проекта
# Лишние элементы были удалены

from build123d import *
from ocp_vscode import show

unit_size           = 8.0 # lego unit size
unit_height         = 9.6 # lego brick height


with BuildPart() as part:
    # База
    length = unit_size * 14
    width  = unit_size * 10
    height = unit_height
    Box(length, width, height)

    # Вырез
    x_pos = 0
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = unit_size * 12
        width  = unit_size * 8
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    # Стойки
    
    x_pos = unit_size * -6
    y_pos = unit_size * -4.5
    z_pos = unit_height * 2
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 2
        width  = unit_size * 1
        height = unit_height * 3
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height, align=align)
    
    x_pos = unit_size * -6
    y_pos = unit_size * 4.5
    z_pos = unit_height * 2
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 2
        width  = unit_size * 1
        height = unit_height * 3
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height, align=align)
    
    x_pos = unit_size * 6.5
    y_pos = 0
    z_pos = unit_height * 2
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 1
        width  = unit_size * 10
        height = unit_height * 3
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height, align=align)
    
    x_pos = unit_size * 6.5
    y_pos = 0
    z_pos = unit_height * 2
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = unit_size * 1
        width  = unit_size * 8
        height = unit_height * 1.5
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height, align=align)

    
    points = [
        # Top
        (unit_size * -6.5, unit_size * 4.5, 0),
        (unit_size * -6.5, unit_size * -4.5, 0),
        (unit_size * 6.5, unit_size * 4.5, 0),
        (unit_size * 6.5, unit_size * -4.5, 0),
    ]
    
    # Отверстия под крепежные винты
    for point in points:
        with BuildPart(Location(point), mode=Mode.SUBTRACT):
            radius = 1.5
            height = unit_height * 10
            align  = (Align.CENTER, Align.CENTER, Align.CENTER)
            Cylinder(radius, height, align=align)

    roundable_edges = part.edges().filter_by(Axis.Z)
    fillet(roundable_edges, radius=2)

filename = f'{__file__.rstrip('.py')}'

show(part.part, names=[filename])
export_stl(part.part, f'{filename}.stl')
