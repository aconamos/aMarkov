import os
from os import path

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

    # return exists

def accumulate(id):
    check_server(id)
    path = f'C:\\GitRepos\\aMarkov\\servers\\{id}'
    log = open(f'{path}/log.txt', 'a')
    jsonraw = open(f'{path}/config.json', 'a')
    return (log, jsonraw)