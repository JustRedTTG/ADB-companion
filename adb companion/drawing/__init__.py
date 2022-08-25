import pygameextra as pe
pe.init()

screenSize = (800, 600)
pe.display.make(screenSize, "ADB companion")


def centered_image(image: pe.Image):
    center = pe.math.center((0, 0, *screenSize))
    image.display((center[0]-image.size[0]*.5, center[1]-image.size[1]*.5))
    return center[0]-image.size[0]*.5, center[1]-image.size[1]*.5, *image.size


def outline(color, rect, outpost):
    outpost2 = outpost/2
    rect = (rect[0], rect[1], rect[0]+rect[2], rect[1]+rect[3])
    pe.draw.line(color, (rect[0]-outpost2, rect[1]), (rect[2]+outpost2, rect[1]), outpost)
    pe.draw.line(color, (rect[2], rect[1]), (rect[2], rect[3]), outpost)
    pe.draw.line(color, (rect[2]+outpost2, rect[3]), (rect[0]-outpost2, rect[3]), outpost)
    pe.draw.line(color, (rect[0], rect[3]), (rect[0], rect[1]), outpost)


def centered_box(size, color, shade, outpost):
    center = pe.math.center((0, 0, *screenSize))
    rect = (
        center[0] - size[0]*.5,
        center[1] - size[1]*.5,
        *size
    )
    outline(shade, rect, outpost + 4)
    pe.draw.rect(color, rect, 0)
    outline(color, rect, outpost)
