# Код позаимствован из проекта робота T-1337
# Форма АКБ вписывается в отсек для АКБ того проекта
# Лишние элементы были удалены

from build123d import *
from ocp_vscode import show

unit_size           = 8.0 # lego unit size
unit_height         = 9.6 # lego brick height


with BuildPart() as part:
    # База
    length = unit_size * 30
    width  = unit_size * 14
    height = unit_height
    Box(length, width, height)

    # Крепления сервоприводов
    x_pos = unit_size * 10.5
    y_pos = unit_size * 5.5
    z_pos = unit_height * 1
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 9
        width  = unit_size * 3
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * 10.5
    y_pos = unit_size * -5.5
    z_pos = unit_height * 1
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 9
        width  = unit_size * 3
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * -10.5
    y_pos = unit_size * 5.5
    z_pos = unit_height * 1
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 9
        width  = unit_size * 3
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * -10.5
    y_pos = unit_size * -5.5
    z_pos = unit_height * 1
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 9
        width  = unit_size * 3
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height, align=align)
    
    # Стойки для понижаек
    z_pos = unit_height
    points = [
        (-15, 10, z_pos),
        (-15, -10, z_pos),
        (-15, 10 + 39, z_pos),
        (-15, -10 - 39, z_pos),
        (-15 + 53, 10, z_pos),
        (-15 + 53, -10, z_pos),
        (-15 + 53, 10 + 39, z_pos),
        (-15 + 53, -10 - 39, z_pos),
        (-87, 39/2, z_pos),
        (-87, -39/2, z_pos),
        (-87 + 53, 39/2, z_pos),
        (-87 + 53, -39/2, z_pos),
    ]
    for point in points:
        with BuildPart(Location(point)):
            length = 8
            width  = 8
            height = unit_height
            align  = (Align.CENTER, Align.CENTER, Align.CENTER)
            Box(length, width, height, align=align)

    # Вырезы под сервоприводы
    x_pos = unit_size * 10.5
    y_pos = unit_size * 6
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = 42
        width  = unit_size * 2
        height = unit_height * 3
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * -10.5
    y_pos = unit_size * 6
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = 42
        width  = unit_size * 2
        height = unit_height * 3
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * 10.5
    y_pos = unit_size * -6
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = 42
        width  = unit_size * 2
        height = unit_height * 3
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * -10.5
    y_pos = unit_size * -6
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = 42
        width  = unit_size * 2
        height = unit_height * 3
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
        
    # Вырезы    
    x_pos = unit_size * 13.5
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = unit_size * 3
        width  = unit_size * 8
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * -13.5
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = unit_size * 3
        width  = unit_size * 8
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * 2.5
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = unit_size * 3
        width  = unit_size * 11
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * 1
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = unit_size * 4
        width  = unit_size * 5
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * -5.5
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = unit_size * 6
        width  = unit_size * 3
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * -7
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = unit_size * 4
        width  = unit_size * 6
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * 3.5
    y_pos = unit_size * 4
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = unit_size * 4.5
        width  = unit_size * 3
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * 3.5
    y_pos = unit_size * -4
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = unit_size * 4.5
        width  = unit_size * 3
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = unit_size * 7.5
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = unit_size * 2.5
        width  = unit_size * 4
        height = unit_height
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
        (unit_size * -9.5,               0,  0),
        (unit_size * 9.5,                0,  0),
        # Servo
        (unit_size * -10.5 + 24, unit_size * 6 + 4, 0),
        (unit_size * -10.5 + 24, unit_size * 6 - 4, 0),
        (unit_size * -10.5 - 24, unit_size * 6 + 4, 0),
        (unit_size * -10.5 - 24, unit_size * 6 - 4, 0),
        (unit_size * 10.5 + 24, unit_size * 6 + 4, 0),
        (unit_size * 10.5 + 24, unit_size * 6 - 4, 0),
        (unit_size * 10.5 - 24, unit_size * 6 + 4, 0),
        (unit_size * 10.5 - 24, unit_size * 6 - 4, 0),
        (unit_size * -10.5 + 24, unit_size * -6 + 4, 0),
        (unit_size * -10.5 + 24, unit_size * -6 - 4, 0),
        (unit_size * -10.5 - 24, unit_size * -6 + 4, 0),
        (unit_size * -10.5 - 24, unit_size * -6 - 4, 0),
        (unit_size * 10.5 + 24, unit_size * -6 + 4, 0),
        (unit_size * 10.5 + 24, unit_size * -6 - 4, 0),
        (unit_size * 10.5 - 24, unit_size * -6 + 4, 0),
        (unit_size * 10.5 - 24, unit_size * -6 - 4, 0),
        # DC-DC
        # 53, 39
        (-15, 10, 0),
        (-15, -10, 0),
        (-15, 10 + 39, 0),
        (-15, -10 - 39, 0),
        (-15 + 53, 10, 0),
        (-15 + 53, -10, 0),
        (-15 + 53, 10 + 39, 0),
        (-15 + 53, -10 - 39, 0),
        (-87, 39/2, 0),
        (-87, -39/2, 0),
        (-87 + 53, 39/2, 0),
        (-87 + 53, -39/2, 0),
        # Top
        (unit_size * -6.5, unit_size * 4.5, 0),
        (unit_size * -6.5, unit_size * -4.5, 0),
        (unit_size * 6.5, unit_size * 4.5, 0),
        (unit_size * 6.5, unit_size * -4.5, 0),
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
        (unit_size * -9.5,               0,  z_pos),
        (unit_size * 9.5,                0,  z_pos),
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
