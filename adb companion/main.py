import os
from drawing import *
from drawing.colorpallet import colorpallet
from drawing.images import images
from connector import *
import connector.buttons as buttons
from drawing.texts import *

init_texts(screenSize)
phones = []
screen = 0
currentPhone = 0

def details(phone):
    if phone.textbox:
        pe.display.blit.rect(phone.textbox, (
            screenSize[0] / 2 - phone.textbox.get_width() / 2,
            screenSize[1] - screenSize[1] / 4 - phone.textbox.get_width() / 2,
        ))
def onlineCheck(ret=False):
    global screen
    temp = check_connections(ADB)
    if len(temp) < 1: temp = check_connections(FASTBOOT)
    if len(temp) < 1:
        if ret:
            return True
        screen = 0
    elif ret:
        return False

# Make folders
if not os.path.exists('user/'): os.mkdir('user/')
if not os.path.exists('user/flash/'): os.mkdir('user/flash/')
#

while True:
    for pe.event.c in pe.event.get():
        pe.event.quitcheckauto()
    pe.fill.full(colorpallet['background'])

    if screen == 0:
        centered_box(images['waitplug'].rect, colorpallet['foreground'], colorpallet['foreground-shadow'], 5)
        centered_image(images['waitplug'])
        phones = check_connections(ADB)
        if len(phones) < 1: phones = check_connections(FASTBOOT)
        if len(phones) > 0:
            for phone in phones:
                phone.texts = {}
                phone.texts['name'] = pe.text.make(phone.name, font, int(screenSize[0]/30), (0, 0), [colorpallet['text'], colorpallet['background']]).texto
                phone.texts['brand'] = pe.text.make(phone.brand, font, int(screenSize[0]/50), (0, 0), [colorpallet['text'], colorpallet['background']]).texto
                phone.texts['mode'] = pe.text.make(phone.mode, font, int(screenSize[0]/50), (0, 0), [colorpallet['text'], colorpallet['background']]).texto
            init_texts(screenSize, phones[currentPhone].id)
            if phones[currentPhone].mode in ADB_MODES:
                screen = 1
            elif phones[currentPhone].mode in FASTBOOT_MODES:
                screen = 2
    elif screen == 1 or screen == 2:
        phone = phones[currentPhone]

        maxX = max(phone.texts['name'].get_width(), phone.texts['brand'].get_width(), phone.texts['mode'].get_width())
        maxY = phone.texts['name'].get_height()+phone.texts['brand'].get_height()+phone.texts['mode'].get_height() + 15

        if not phone.textbox:
            surface = pe.pygame.Surface((maxX, maxY))
            surface.fill(colorpallet['background'])
            y = 0
            for text in list(phone.texts):
                x = surface.get_width()/2 - phone.texts[text].get_width()/2
                surface.blit(phone.texts[text], (x, y))
                y += phone.texts[text].get_height() + 5
            phone.textbox = surface
        if not os.path.exists(f'user/flash/{phone.id}'): os.mkdir(f'user/flash/{phone.id}')

        screen += 2
    elif screen == 3:
        phone = phones[currentPhone]

        centered_box(images['phone_adb'].rect, colorpallet['foreground'], colorpallet['foreground-shadow'], 5)
        centered_image(images['phone_adb'])

        x, y = 50, 50
        for item in list(buttons.adb):
            pe.button.rect((x, y, texts[item].get_width()+6, texts[item].get_height()+6), colorpallet['foreground'], colorpallet['foreground-active'], None, phone.command, buttons.adb[item])
            pe.display.blit.rect(texts[item], (x + 3, y + 3))
            y += texts[item].get_height()+8
        x, y = screenSize[0] - screenSize[0] / 3, 50
        for item in list(flashables):
            pe.button.rect((x, y, texts[f'push {item}'].get_width() + 6, texts[f'push {item}'].get_height() + 6), colorpallet['foreground'], colorpallet['foreground-active'], None, phone.command, f'push {flashables[item]} /sdcard/')
            pe.display.blit.rect(texts[f'push {item}'], (x + 3, y + 3))
            y += texts[f'push {item}'].get_height() + 8

        details(phone)
        onlineCheck()
    elif screen == 4:
        phone = phones[currentPhone]

        centered_box(images['phone_fastboot'].rect, colorpallet['foreground'], colorpallet['foreground-shadow'], 5)
        centered_image(images['phone_fastboot'])

        x, y = 50, 50
        for item in list(buttons.fastboot):
            pe.button.rect((x, y, texts[item].get_width() + 6, texts[item].get_height() + 6), colorpallet['foreground'], colorpallet['foreground-active'], None, phone.command, buttons.fastboot[item])
            pe.display.blit.rect(texts[item], (x + 3, y + 3))
            y += texts[item].get_height() + 8
        x, y = screenSize[0]-screenSize[0]/3, 50
        for item in list(bootables):
            pe.button.rect((x, y, texts[f'boot {item}'].get_width() + 6, texts[f'boot {item}'].get_height() + 6), colorpallet['foreground'], colorpallet['foreground-active'], None, phone.command, f'boot {bootables[item]}')
            pe.display.blit.rect(texts[f'boot {item}'], (x + 3, y + 3))
            y += texts[f'boot {item}'].get_height() + 8

        details(phone)
        onlineCheck()


    pe.display.update()