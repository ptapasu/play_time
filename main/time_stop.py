import os
queue = './queue'

def set_queue(n):
        if (os.path.isfile(queue))!=True:
                create_file(queue)
        f = open(queue,'a+')
        f.write(f'{n}\n')
        f.close()

set_queue(2)
print('Your time is set to off')
input()
