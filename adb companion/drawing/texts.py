import os
import pygameextra as pe
from drawing.colorpallet import colorpallet

texts = {}
bootables = {}
flashables = {}
installables = {}
font = 'freesansbold.ttf'

def remove_ext(file:str, repl:str = ''):
    dots = file.split('.')
    ext = '.' + dots[len(dots)-1]
    return file.replace(ext, repl)

def init_texts(SS, using_id=None):
    texts.clear()
    bootables.clear()
    flashables.clear()
    installables.clear()
    texts['reboot'] = pe.text.Text("Restart.", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).obj
    texts['bootloader'] = pe.text.Text("Bootloader.", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).obj
    texts['recovery'] = pe.text.Text("Recovery.", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).obj
    texts['unlockboot'] = pe.text.Text("Unlock bootloader", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).obj
    texts['lockboot'] = pe.text.Text("Relock bootloader", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).obj
    
    texts['SDUNIT_/'] = pe.text.Text("ROOT", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).obj
    texts['SDUNIT_/SD'] = pe.text.Text("SDCARD", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).obj
    
    if not os.path.exists('user/flash/'): return

    phones = os.listdir('user/flash/')
    for phone in phones:
        if using_id and phone != using_id: continue
        for file in os.listdir(f'user/flash/{phone}/'):
            if file.endswith('.zip'):
                texts[f'push {file}'] = pe.text.Text(f"Push {remove_ext(file)}", font, int(SS[0] / 60), (0, 0), [colorpallet['text'], None]).obj
                flashables[file] = f'"user/flash/{phone}/{file}"'
                continue
            elif file.endswith('.apk'):
                texts[f'install {file}'] = pe.text.Text(f"Install {remove_ext(file)}", font, int(SS[0] / 60), (0, 0), [colorpallet['text'], None]).obj
                installables[file] = f'"user/flash/{phone}/{file}"'
                continue
            elif not file.endswith('.img'): continue
            #texts[f'flash {file}'] = pe.text.Text(f"Flash {file}", font, int(SS[0] / 60), (0, 0), [colorpallet['text'], None]).obj
            texts[f'boot {file}'] = pe.text.Text(f"Boot {remove_ext(file)}", font, int(SS[0] / 60), (0, 0), [colorpallet['text'], None]).obj
            bootables[file] = f'"user/flash/{phone}/{file}"'
