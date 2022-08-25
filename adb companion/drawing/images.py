import pygameextra as pe
from os import path

dir = 'resources'

def load(name):
    imagepath = path.join(dir, name)
    return pe.Image(imagepath)

images = {
    'waitplug': load('waitplug.png'),
    'phone_adb': load('phone_adb.png'),
    'phone_fastboot': load('phone_fastboot.png')
}
