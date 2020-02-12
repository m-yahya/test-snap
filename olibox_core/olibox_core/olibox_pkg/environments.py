import os

import toml

if os.path.isfile('config.toml'):
    f = toml.load('config.toml')

    items = f.keys()
    unique_dict = {}
    for item in items:
        if type(f[item]) is not str:
            for i in f[item].keys():
                unique_dict[i] = f[item][i]
        else:
            unique_dict[item] = f[item]

    locals().update(unique_dict)

    # for key, val in new_dict.items():
    #     exec(key + '=val')

else:
    print('file not found')
