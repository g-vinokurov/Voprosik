
from build123d import *
from ocp_vscode import show

with BuildPart() as part:
    radius = 160
    height = 60
    Cylinder(radius, height)

    roundable_edges = part.edges().filter_by(GeomType.CIRCLE)
    fillet(roundable_edges, radius=29)

    x = 0
    y = 0
    z = -15
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        length = 320
        width  = 320
        height = 50
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x = 0
    y = -80
    z = 0
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        length = 320
        width  = 220
        height = 60
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x = -150
    y = 0
    z = 0
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        length = 160
        width  = 320
        height = 60
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x = 0
    y = -50
    z = 0
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        radius = 160
        height = 60
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Cylinder(radius, height)
    
    x = 60
    y = 25
    z = -30
    with BuildPart(Location((x, y, z)), mode=Mode.INTERSECT):
        radius = 150
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Sphere(radius)
    
    x = 0
    y = 100
    z = 15
    with BuildPart(Location((x, y, z))):
        length = 60
        width  = 30
        height = 10
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x = 0
    y = -20
    z = -90
    with BuildPart(Location((x, y, z)), mode=Mode.INTERSECT):
        radius = 180
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Sphere(radius)
    
    x = 0
    y = 0
    z = -15
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        length = 320
        width  = 320
        height = 50
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    x = 0
    y = 95
    z = 15
    with BuildPart(Location((x, y, z)), mode=Mode.SUBTRACT):
        length = 42
        width  = 22
        height = 10
        align  = (Align.CENTER, Align.CENTER, Align.CENTER)
        Box(length, width, height)
    
    # Отверстия под крепежные винты 3 mm
    points = [
        (24, 100, 15),
        (24, 90, 15),
        (-24, 100, 15),
        (-24, 90, 15),
    ]
    for point in points:
        with BuildPart(Location(point), mode=Mode.SUBTRACT):
            radius = 1.5
            height = 10
            align  = (Align.CENTER, Align.CENTER, Align.CENTER)
            Cylinder(radius, height, align=align)
    
    roundable_edges = part.edges().filter_by(Axis.Z)
    fillet(roundable_edges, radius=1)


filename = f'{__file__[:-3]}'

show(part.part, names=[filename])
export_stl(part.part, f'{filename}.stl')
