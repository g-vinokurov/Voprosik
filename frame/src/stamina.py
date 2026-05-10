# Код позаимствован из проекта робота T-1337
# Форма АКБ вписывается в отсек для АКБ того проекта
# Лишние элементы были удалены

from build123d import *
from ocp_vscode import show

unit_size           = 8.0 # lego unit size
unit_height         = 9.6 # lego brick height


with BuildPart() as part:
    # База
    length = unit_size * 26
    width  = unit_size * 14
    height = unit_height
    Box(length, width, height)

    # Крепления сервоприводов
    x_pos = unit_size * 8.5
    y_pos = unit_size * 5.5
    z_pos = unit_height * 1
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 9
        width  = unit_size * 3
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * 8.5
    y_pos = unit_size * -5.5
    z_pos = unit_height * 1
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 9
        width  = unit_size * 3
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * -8.5
    y_pos = unit_size * 5.5
    z_pos = unit_height * 1
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 9
        width  = unit_size * 3
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * -8.5
    y_pos = unit_size * -5.5
    z_pos = unit_height * 1
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 9
        width  = unit_size * 3
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height, align=align)
    
    # Стойки для понижаек и Arduino Uno
    z_pos = unit_height
    points = [
        # DC-DC
        (-26.5, 10, z_pos),
        (-26.5, -10, z_pos),
        (-26.5, 10 + 39, z_pos),
        (-26.5, -10 - 39, z_pos),
        (-26.5 + 53, 10, z_pos),
        (-26.5 + 53, -10, z_pos),
        (-26.5 + 53, 10 + 39, z_pos),
        (-26.5 + 53, -10 - 39, z_pos),
        (-97, 39/2, z_pos),
        (-97, -39/2, z_pos),
        (-97 + 53, 39/2, z_pos),
        (-97 + 53, -39/2, z_pos),
        # Arduino Uno
        (36, 22, z_pos),
        (36, -6, z_pos),
        (88, 27.5, z_pos),
        (87, -20.9, z_pos),
    ]
    for point in points:
        with BuildPart(Location(point)):
            length = 8
            width  = 8
            height = unit_height
            align  = (Align.CENTER, Align.CENTER, Align.CENTER)
            Box(length, width, height, align=align)

    # Вырезы под сервоприводы
    x_pos = unit_size * 8.5
    y_pos = unit_size * 7 - 11
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = 42
        width  = 22
        height = unit_height * 3
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * -8.5
    y_pos = unit_size * 7 - 11
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = 42
        width  = 22
        height = unit_height * 3
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * 8.5
    y_pos = unit_size * -7 + 11
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = 42
        width  = 22
        height = unit_height * 3
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * -8.5
    y_pos = unit_size * -7 + 11
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = 42
        width  = 22
        height = unit_height * 3
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    # Вырезы
    x_pos = 0
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = unit_size * 5
        width  = unit_size * 6
        height = unit_height * 3
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * -6
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = unit_size * 4
        width  = unit_size * 4
        height = unit_height * 3
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * 7
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = unit_size * 4
        width  = unit_size * 4
        height = unit_height * 3
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)

    # Отверстия под крепежные винты
    points = [
        # Wheelbase
        (unit_size * 0,    unit_size * 3.5,  0),
        (unit_size * 0,    unit_size * -3.5, 0),
        (unit_size * 7,    unit_size * 3.5,  0),
        (unit_size * 7,    unit_size * -3.5, 0),
        (unit_size * -7,   unit_size * 3.5,  0),
        (unit_size * -7,   unit_size * -3.5, 0),
        (unit_size * -9.5, unit_size * 0,    0),
        (unit_size * 9.5,  unit_size * 0,    0),
        # Servo
        (unit_size * -8.5 + 24, unit_size * 7 - 11 + 5, 0),
        (unit_size * -8.5 + 24, unit_size * 7 - 11 - 5, 0),
        (unit_size * -8.5 - 24, unit_size * 7 - 11 + 5, 0),
        (unit_size * -8.5 - 24, unit_size * 7 - 11 - 5, 0),
        (unit_size * 8.5 + 24, unit_size * 7 - 11 + 5, 0),
        (unit_size * 8.5 + 24, unit_size * 7 - 11 - 5, 0),
        (unit_size * 8.5 - 24, unit_size * 7 - 11 + 5, 0),
        (unit_size * 8.5 - 24, unit_size * 7 - 11 - 5, 0),
        (unit_size * -8.5 + 24, unit_size * -7 + 11 + 5, 0),
        (unit_size * -8.5 + 24, unit_size * -7 + 11 - 5, 0),
        (unit_size * -8.5 - 24, unit_size * -7 + 11 + 5, 0),
        (unit_size * -8.5 - 24, unit_size * -7 + 11 - 5, 0),
        (unit_size * 8.5 + 24, unit_size * -7 + 11 + 5, 0),
        (unit_size * 8.5 + 24, unit_size * -7 + 11 - 5, 0),
        (unit_size * 8.5 - 24, unit_size * -7 + 11 + 5, 0),
        (unit_size * 8.5 - 24, unit_size * -7 + 11 - 5, 0),
        # DC-DC
        # 53, 39
        (-26.5, 10, 0),
        (-26.5, -10, 0),
        (-26.5, 10 + 39, 0),
        (-26.5, -10 - 39, 0),
        (-26.5 + 53, 10, 0),
        (-26.5 + 53, -10, 0),
        (-26.5 + 53, 10 + 39, 0),
        (-26.5 + 53, -10 - 39, 0),
        (-97, 39/2, 0),
        (-97, -39/2, 0),
        (-97 + 53, 39/2, 0),
        (-97 + 53, -39/2, 0),
        # Arduino Uno
        (36, 22, 0),
        (36, -6, 0),
        (88, 27.5, 0),
        (87, -20.9, 0),
        # Top
        (unit_size * -4.5, unit_size * 6, 0),
        (unit_size * -4.5, unit_size * -6, 0),
        (unit_size * 4.5, unit_size * 6, 0),
        (unit_size * 4.5, unit_size * -6, 0),
    ]
    for point in points:
        with BuildPart(Location(point), mode=Mode.SUBTRACT):
            radius = 1.5
            height = unit_height * 10
            align  = (Align.CENTER, Align.CENTER, Align.CENTER)
            Cylinder(radius, height, align=align)
    
    # Утоплялки под крепежные винты
    z_pos = unit_height / 2 - 1.5
    points = [
        # Wheelbase
        (unit_size * 0,    unit_size * 3.5,  z_pos),
        (unit_size * 0,    unit_size * -3.5, z_pos),
        (unit_size * 7,    unit_size * 3.5,  z_pos),
        (unit_size * 7,    unit_size * -3.5, z_pos),
        (unit_size * -7,   unit_size * 3.5,  z_pos),
        (unit_size * -7,   unit_size * -3.5, z_pos),
        (unit_size * -9.5, unit_size * 0,    z_pos),
        (unit_size * 9.5,  unit_size * 0,    z_pos),
    ]
    for point in points:
        with BuildPart(Location(point), mode=Mode.SUBTRACT):
            radius = 3
            height = 3
            align  = (Align.CENTER, Align.CENTER, Align.CENTER)
            Cylinder(radius, height, align=align)

    roundable_edges = part.edges().filter_by(Axis.Z)
    fillet(roundable_edges, radius=2)

filename = f'{__file__.rstrip('.py')}'

show(part.part, names=[filename])
export_stl(part.part, f'{filename}.stl')
