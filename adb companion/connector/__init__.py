import os
from subprocess import Popen, PIPE
import connector.buttons as buttons
from drawing.CDP import Halt
ADB = 0
FASTBOOT = 1

ADB_MODES = [
    'device', 'recovery'
]
FASTBOOT_MODES = [
    'fastboot'
]

FIXES = {

}

def fixformat(text:bytes, maxFIX:bool = False):
    text = text.decode('utf-8')
    for item in list(FIXES):
        text.replace(item, FIXES[item])
    if maxFIX:
        lines = text.splitlines()
        final = ''
        for line in lines:
            final += line + '\n'
        if len(final) > 1:
            return final[0:len(final)-1]
        try: return text.splitlines()[0]
        except: return text
    return text

def get_args(value:str):
    args = []
    arg = ''
    string_mode = False
    for letter in value:
        if letter == '"': string_mode = not string_mode
        elif string_mode: arg += letter
        elif not string_mode and letter == ' ':
            args.append(arg)
            arg = ''
        else: arg += letter
    args.append(arg)
    return args

def fixvalue(value:str):
    try:
        return int(value)
    except:
        try:
            return float(value)
        except:
            if value == 'true':
                return True
            elif value == 'false':
                return False
            return value

def adb(*args):
    cmd = Popen(["adb", *args], stdout=PIPE)
    return cmd.communicate()[0]

def fastboot(*args):
    cmd = Popen(["fastboot", *args], stdout=PIPE)
    return cmd.communicate()[0]

class Phone:
    def __init__(self, info):
        self.id, self.mode = info.split('	')
        self.textbox = None
        if self.mode in ADB_MODES:
            try:
                self.getInfo()
                self.brand = self.info['ro.product.brand']
                try:
                    self.name = self.info['ro.build.product']
                    if self.brand not in self.name: return 1/0
                except:
                    try: self.name = self.info['ro.product.model']
                    except: self.name = self.id
            except:
                self.info = None
                self.brand = 'Unknown'
                self.name = self.id
        else:
            self.info = None
            self.brand = 'Unknown'
            self.name = self.id
    def commandw(self, *args):
        if self.mode in ADB_MODES:
            return adb('-s', self.id, *args)
        elif self.mode in FASTBOOT_MODES:
            return fastboot('-s', self.id, *args)
        else:
            return 'ERROR'
    def command(self, text:str, user:bool=True):
        if user:
            program = Halt(text)
            program.run()
        ret = fixformat(self.commandw(*get_args(text)), 2)
        if user:
            program.stop()
        return ret
    def getInfo(self):
        preinfo = self.command('shell getprop', False).splitlines()
        self.info = {}
        key, value = '', []
        point = 0
        for line in preinfo:
            if point == 0: # Reading key
                key = line.split(']')[0]
                key = key[1:]
                point = 1
            if point == 1:
                if ': ' in line:
                    line = line.split(': ')[1]
                    line = line[1:]
                values = line.split(',')
                for v in values:
                    if ']' in v:
                        v = v[:-1]
                        point = 2
                    value.append(fixvalue(v))
            if point == 2:
                if len(value)==1:
                    self.info[key] = value[0]
                else:
                    self.info[key] = value
                value = []
                point = 0
    def debugInfo(phone):
        for item in list(phone.info):
            print(f'{item} : {phone.info[item]}')
    def ls(self, directory, user:bool=True):
        result = self.command(f'shell ls -1 -S -p -r {directory}', user).splitlines()
        for i in range(len(result)): result[i] = result[i].replace('\\', '')

        return result
    def list_files(self, directory, user:bool=True):
        result = self.ls(directory, user)
        final = []
        for item in result:
            if not item.endswith('/'): final.append(os.path.join(directory, item))
        return final
    def list_directories(self, directory, user:bool=True):
        result = self.ls(directory, user)
        final = []
        for item in result:
            if item.endswith('/'): final.append(os.path.join(directory, item))
        return final
    def delete_file(self, file, user:bool=True):
        self.command(f'shell rm {file}', user)



def check_connections(mode=ADB):
    if mode == ADB:
        items = adb('devices').splitlines()
        del items[0]
        del items[len(items) - 1]
    elif mode == FASTBOOT:
        items = fastboot('devices').splitlines()
    phones = []
    for phone in items:
        phones.append(Phone(fixformat(phone)))
    return phones