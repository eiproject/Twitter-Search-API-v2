from .secret import my_bearer, my_bearer2

bearer_file = 'bearer_secret'
bearer = my_bearer
with open(bearer_file, 'w') as t:
    t.write(bearer)


def switch_bearer():
    '''Switching Bearer'''
    print('Switching Bearer..')
    with open(bearer_file, 'r') as t:
        bearer = t.readline()
        if bearer == my_bearer:
            bearer = my_bearer2
        else:
            bearer = my_bearer
        
        with open(bearer_file, 'w') as w:
            w.write(bearer)