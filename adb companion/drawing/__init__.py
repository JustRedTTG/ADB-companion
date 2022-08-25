import pygameextra as pe
pe.init()

try:
    pe.__version__
except:
    pe.__version__ = 'null'

if pe.__version__ != '1.6.5.2':
    print("Sorry, but the software isn't compatible with your pygameextra version.")
    exit()

screenSize = (800, 600)
pe.display.make(screenSize, "ADB companion")


def centered_image(image:pe.image):
    center = pe.math.center((0, 0, *screenSize))
    image.size = image.rect
    image.position = (center[0]-image.size[0]/2, center[1]-image.size[1]/2)
    image.rect = (*image.position, *image.size)

    image.display()
    return image.rect
def outline(color, rect, outpost):
    outpost2 = outpost/2
    rect = (rect[0], rect[1], rect[0]+rect[2], rect[1]+rect[3])
    pe.draw.line(color, (rect[0]-outpost2, rect[1]), (rect[2]+outpost2, rect[1]), outpost)
    pe.draw.line(color, (rect[2], rect[1]), (rect[2], rect[3]), outpost)
    pe.draw.line(color, (rect[2]+outpost2, rect[3]), (rect[0]-outpost2, rect[3]), outpost)
    pe.draw.line(color, (rect[0], rect[3]), (rect[0], rect[1]), outpost)
def centered_box(rect, color, shade, outpost):
    outline(shade, rect, outpost + 4)
    pe.draw.rect(color, rect, 0)
    outline(color, rect, outpost)
