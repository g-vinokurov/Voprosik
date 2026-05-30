# Код позаимствован из проекта робота T-1337
# Форма АКБ вписывается в отсек для АКБ того проекта
# Лишние элементы были удалены

from build123d import *
from ocp_vscode import show

unit_size           = 8.0 # lego unit size
unit_height         = 9.6 # lego brick height


with BuildPart() as part:
    # База
    length = unit_size * 10
    width  = unit_size * 14
    height = unit_height
    Box(length, width, height)

    # Вырез
    x_pos = -5
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = 12
        width  = 80
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = -5
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = 20
        width  = 72
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = 18.5
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = 13
        width  = 62
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = 18.5
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = 27
        width  = 50
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x_pos = -23.5
    y_pos = 0
    z_pos = 0
    with BuildPart(Location((x_pos, y_pos, z_pos)), mode=Mode.SUBTRACT):
        length = 17
        width  = 72
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    # Стойки
    x_pos = unit_size * -4.5
    y_pos = unit_size * -6
    z_pos = unit_height * 2.5
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 1
        width  = unit_size * 2
        height = unit_height * 4
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height, align=align)
    
    x_pos = unit_size * 4.5
    y_pos = unit_size * -6
    z_pos = unit_height * 2.5
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 1
        width  = unit_size * 2
        height = unit_height * 4
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height, align=align)
    
    x_pos = unit_size * -4.5
    y_pos = unit_size * 6
    z_pos = unit_height * 2.5
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 1
        width  = unit_size * 2
        height = unit_height * 4
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height, align=align)
    
    x_pos = unit_size * 4.5
    y_pos = unit_size * 6
    z_pos = unit_height * 2.5
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 1
        width  = unit_size * 2
        height = unit_height * 4
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height, align=align)
    
    # Мостики    
    x_pos = unit_size * -4.5
    y_pos = 0
    z_pos = unit_height * 2.5
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 1
        width  = unit_size * 14
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height, align=align)
    
    x_pos = unit_size * 4.5
    y_pos = 0
    z_pos = unit_height * 2.5
    with BuildPart(Location((x_pos, y_pos, z_pos))):
        length = unit_size * 1
        width  = unit_size * 14
        height = unit_height
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height, align=align)
    
    # Стойки   
    points = [
        # Top
        (unit_size * -4.5, unit_size * 6, 0),
        (unit_size * -4.5, unit_size * -6, 0),
        (unit_size * 4.5, unit_size * 6, 0),
        (unit_size * 4.5, unit_size * -6, 0),
    ]
    
    # Отверстия под крепежные винты
    for point in points:
        with BuildPart(Location(point), mode=Mode.SUBTRACT):
            radius = 1.5
            height = unit_height * 10
            align  = (Align.CENTER, Align.CENTER, Align.CENTER)
            Cylinder(radius, height, align=align)
    
    # Крепление плат
    points = [
        # Плата развода питания
        (-13, -38, 0),
        (-13, 38, 0),
        (3, -38, 0),
        (3, 38, 0),
        # ШИМ-расширитель
        (9, -28, 0),
        (9, 28, 0),
        (28, -28, 0),
        (28, 28, 0),
    ]
    
    # Отверстия под крепежные винты
    for point in points:
        with BuildPart(Location(point), mode=Mode.SUBTRACT):
            radius = 1
            height = unit_height * 10
            align  = (Align.CENTER, Align.CENTER, Align.CENTER)
            Cylinder(radius, height, align=align)

    roundable_edges = part.edges().filter_by(Axis.Z)
    fillet(roundable_edges, radius=1)

filename = f'{__file__.rstrip('.py')}'

show(part.part, names=[filename])
export_stl(part.part, f'{filename}.stl')
