import os
import pgerom as pe
from drawing.colorpallet import colorpallet

texts = {}
bootables = {}
font = 'freesansbold.ttf'

def init_texts(SS):
    texts['reboot'] = pe.text.make("Restart.", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).texto
    texts['bootloader'] = pe.text.make("Bootloader.", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).texto
    texts['recovery'] = pe.text.make("Recovery.", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).texto
    texts['unlockboot'] = pe.text.make("Unlock bootloader", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).texto
    texts['lockboot'] = pe.text.make("Relock bootloader", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).texto
    if not os.path.exists('user/flash/'): return

    phones = os.listdir('user/flash/')
    for phone in phones:
        for file in os.listdir(f'user/flash/{phone}/'):
            if not file.endswith('.img'): return
            #texts[f'flash {file}'] = pe.text.make(f"Flash {file}", font, int(SS[0] / 60), (0, 0), [colorpallet['text'], None]).texto
            texts[f'boot {file}'] = pe.text.make(f"Boot {file}", font, int(SS[0] / 60), (0, 0), [colorpallet['text'], None]).texto
            bootables[file] = f'user/flash/{phone}/{file}'