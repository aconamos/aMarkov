import os


# TODO Make path relative
def check_server(id):
    path = f'C:\\GitRepos\\aMarkov\\servers\\{id}'
    exists = {'dir': True, 'log': False, 'config': False}
    if not os.path.isdir(path):
        os.mkdir(path)
    if os.path.isfile(f'{path}/log.txt'):
        exists['log'] = True
    if os.path.isfile(f'{path}/config.json'):
        exists['config'] = True

    return exists


def accumulate(id):
    # File checking done, should probably move this to check_server but whatever
    exists = check_server(id)
    path = f'C:\\GitRepos\\aMarkov\\servers\\{id}'
    if not exists['log']:
        with open(f'{path}\\log.txt', 'w+') as l:
            l.close()
    if not exists['config'] or os.stat(f'{path}\\config.json').st_size <= 0:
        with open(f'{path}\\config.json', 'w+') as j:
            j.write("""{
    "channel": 123,
    "probability": 5,
    "on": false,
    "mentions": true,
    "equal_chance": true
}""")
            j.close()
    log = FileInterface(id, True)
    json_wrapper = FileInterface(id)
    return (log, json_wrapper)


class FileInterface:
    def __init__(self, id, log=False):
        # oh god what did i do
        self.id = id
        if not log:
            self.path = f'C:\\GitRepos\\aMarkov\\servers\\{id}\\config.json'
        else:
            self.path = f'C:\\GitRepos\\aMarkov\\servers\\{id}\\log.txt'
        self.file = None 


    def readable(self):
        if self.file is not None:
            self.close()
        self.file = open(self.path, 'r')
        return self.file

    def writable(self):
        if self.file is not None:
            self.close()
        self.file = open(self.path, 'w')
        return self.file

    def read(self):
        string = self.readable().read()
        self.close()
        return string
    
    def write(self, string):
        file = self.writable()
        file.write(string)
        self.close()

    def close(self):
        self.file.close()
        self.file = None