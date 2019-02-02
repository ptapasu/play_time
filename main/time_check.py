import configparser

config_file = './config'

def get_state(value):
    config = configparser.ConfigParser()
    config.sections()
    config.read(config_file)
    status = config['DATA'][value]
    return status
a = get_state('play_time')
b = get_state('state')
c = get_state('end_time')
print(f'You have {a} minutes of play time remaining')
print(f'Your time is currently {b}')
print(f'Your time will finish at {c}')
input()
