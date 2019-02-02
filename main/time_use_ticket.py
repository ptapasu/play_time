import os
import configparser
import datetime
import hashlib
queue = './queue'

def menu_layout(x):
    os.system('cls')
    indent = ' '*20
    print('')
    print(indent+'+'+ '-'*58 +'+')
    print(indent+'|'+' '*58+'|')
    print(indent+'|'+ x.center(58,' ')+'|')
    print(indent+'|'+' '*58+'|')
    print(indent+'+'+ '-'*58 +'+')
    print('')
    print('')

def set_queue(n):
        if (os.path.isfile(queue))!=True:
                create_file(queue)
        f = open(queue,'a+')
        f.write(f'{n}\n')
        f.close()
        
def get_user():
        config = configparser.ConfigParser()
        config.sections()
        config.read('./agent')
        info = config['DATA']['AGENT']
        return info
    
def check_use(ticket):
    file = './record'
    read_file = open(file,'r')
    fdata = read_file.readlines()
    for i in fdata:
        if i.strip('\n')==ticket:
            return True
    else:
        return False
    
def write_record(ticket):
        file = './record'
        if (os.path.isfile(file))!=True:
                create_file(file)
        f = open(file,'a+')
        f.write(f'{ticket}\n')
        f.close()

def use_tix():
    menu_layout('Use Ticket')
    print('')
    print('')
    print(20*' '+'Please enter your Ticket')
    a =  input(' '*20)
    data = a.split('.')
    e = str(datetime.date.today())
    to_encode_hashk = '.'.join([e,data[0],data[1],data[2]])
    hashk = hashlib.blake2b(to_encode_hashk.encode('utf-8'), digest_size = 4).hexdigest() # this produces the hash
    #check if the ticket has been used
    if check_use(a)==True:
        print(f'The Ticket {a} has already been used')
        input()
        return
    #check that user is different
    if (hashk.upper())==data[3]:
        print(data)
        if data[0][0]=='1' and get_user()!=data[0][1]:
            set_queue(f'3={data[1]}')
            print(f'{data[1]} minutes of extra play time added')
            write_record(a)
            input()
        elif data[0][0]=='2' and get_user()!=data[0][1]:
            set_queue(f'4={data[1]}')
            print(f'Cut-off time changed to {data[1]}')
            write_record(a)
            input()
    else:
        print('This ticket is invalid')
        input()
    #check that the user... is equal someone else
    #then split the action, and add action : and value to the ... queue


use_tix()
