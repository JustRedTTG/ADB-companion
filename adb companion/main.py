from drawing import *
from drawing.colorpallet import colorpallet
from drawing.images import images
from connector import *

phones = []
screen = 0

while True:
    for pe.event.c in pe.event.get():
        pe.event.quitcheckauto()
    pe.fill.full(colorpallet['background'])

    if screen == 0:
        centered_box(images['waitplug'].rect, colorpallet['foreground'], colorpallet['foreground-shadow'], 5)
        centered_image(images['waitplug'])
        phones = check_connections(ADB)
        if len(phones) > 0:
            screen = 1
    elif screen == 1:
        centered_box(images['phone'].rect, colorpallet['foreground'], colorpallet['foreground-shadow'], 5)
        centered_image(images['phone'])


    pe.display.update()