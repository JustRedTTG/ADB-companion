import os
import pygameextra as pe
from drawing.colorpallet import colorpallet

texts = {}
bootables = {}
flashables = {}
font = 'freesansbold.ttf'

def remove_ext(file:str, repl:str = ''):
    dots = file.split('.')
    ext = '.' + dots[len(dots)-1]
    return file.replace(ext, repl)

def init_texts(SS, using_id=None):
    texts.clear()
    bootables.clear()
    flashables.clear()
    texts['reboot'] = pe.text.make("Restart.", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).texto
    texts['bootloader'] = pe.text.make("Bootloader.", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).texto
    texts['recovery'] = pe.text.make("Recovery.", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).texto
    texts['unlockboot'] = pe.text.make("Unlock bootloader", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).texto
    texts['lockboot'] = pe.text.make("Relock bootloader", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).texto
    if not os.path.exists('user/flash/'): return

    phones = os.listdir('user/flash/')
    for phone in phones:
        if using_id and phone != using_id: continue
        for file in os.listdir(f'user/flash/{phone}/'):
            if file.endswith('.zip'):
                texts[f'push {file}'] = pe.text.make(f"Push {remove_ext(file)}", font, int(SS[0] / 60), (0, 0), [colorpallet['text'], None]).texto
                flashables[file] = f'"user/flash/{phone}/{file}"'
                continue
            elif not file.endswith('.img'): continue
            #texts[f'flash {file}'] = pe.text.make(f"Flash {file}", font, int(SS[0] / 60), (0, 0), [colorpallet['text'], None]).texto
            texts[f'boot {file}'] = pe.text.make(f"Boot {remove_ext(file)}", font, int(SS[0] / 60), (0, 0), [colorpallet['text'], None]).texto
            bootables[file] = f'"user/flash/{phone}/{file}"'
