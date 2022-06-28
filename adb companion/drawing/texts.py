import pgerom as pe
from drawing.colorpallet import colorpallet
texts = {}
font = 'freesansbold.ttf'

def init_texts(SS):
    texts['bootloader'] = pe.text.make("Bootloader.", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).texto
    texts['recovery'] = pe.text.make("Recovery.", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).texto
    texts['unlockboot'] = pe.text.make("Unlock bootloader", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).texto
    texts['lockboot'] = pe.text.make("Relock bootloader", font, int(SS[0]/60), (0, 0), [colorpallet['text'], None]).texto