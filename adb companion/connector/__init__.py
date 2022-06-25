from subprocess import Popen, PIPE

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
        return text.splitlines()[0]
    return text
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
        if self.mode in ADB_MODES:
            self.getInfo()
            self.brand = self.info['ro.product.brand']
            try:
                self.name = self.info['ro.build.product']
                if self.brand not in self.name:
                    return 1/0
            except:
                try:
                    self.name = self.info['ro.product.model']
                except:
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
    def command(self, text:str):
        return fixformat(self.commandw(*text.split(' ')), 2)
    def getInfo(self):
        preinfo = self.command('shell getprop').splitlines()
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



def check_connections(mode=ADB):
    if mode == ADB:
        items = adb('devices').splitlines()
        del items[0]
    elif mode == FASTBOOT:
        items = fastboot('devices').splitlines()
    del items[len(items)-1]
    phones = []
    for phone in items:
        phones.append(Phone(fixformat(phone)))
    return phones