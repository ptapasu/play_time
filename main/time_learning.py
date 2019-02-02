import random
import statistics
import os
import sys
import configparser
import datetime
import zc.lockfile
try:
    lock = zc.lockfile.LockFile('./lock/aux_lock')
except zc.lockfile.LockError:
    sys.exit(0)
    
file = './config'
queue = './queue'
score = 0
correct = 0
incorrect = []
indent = ' '*20
question = 30

def msg_switch(n):
        if n==1:
                return('Learning Tool')
        elif n==2:
                return(f'Correct:{correct}|Incorrect:{str(len(incorrect))}|Score:{score}')
        elif n==3:
                return('Congratulations 120 minutes of playtime allocated')
        
def main_menu(n):
        msg=msg_switch(n)
        os.system('cls')
        print('')
        print(indent+'+'+ '-'*58 +'+')
        print(indent+'|'+' '*58+'|')
        print(indent+'|'+ msg.center(58,' ')+'|')
        print(indent+'|'+' '*58+'|')
        print(indent+'+'+ '-'*58 +'+')
        print('')
        print('')


def input_cleaner(i):
    while True:
        main_menu(2)
        print(f'{indent}{i}')
        print(f'{indent}Please enter a digit')
        print('')
        user = input(f'{indent}:')
        try:
            user = float(user)
            return user
        except ValueError:
            continue

def negative(n):
    if random.choice([True,True,True,True,True,True,False])==False:
        return n*-1
    else:
        return n

def buff_confirm():
            print('')
            print('')
            msg = ('--Press any key to continue--')         
            input(indent+msg.center(60,' '))
            
def multiplication():
        global score
        global correct
        global incorrect
        a = negative(random.randint(1,12))
        b = negative(random.randint(3,16))
        c = a * b
        problem = str(a) + ' x ' + str(b) + ' = ?'
        answer = str(a) + ' x ' + str(b) + ' = ' + str(c)
        i = input_cleaner(problem)
        if int(i)==c:
            main_menu(2)
            print(f'{indent}Correct ' + answer)
            buff_confirm()
            score += 1
            correct += 1
        else:
            main_menu(2)
            print(f'{indent}Incorrect! the answer for ' + problem + ' is ' + str(c))
            buff_confirm()
            incorrect.append([problem, answer, i])

              
def simple_algebra():
        global score
        global correct
        global incorrect
        main_menu(2)
        a = negative(random.randint(1,25))
        b = negative(random.randint(1,25))
        c = random.choice(['+','-','*'])#removed / for now
        d = 0
        if c=='+':
            d = a + b
        elif c=='-':
            d = a - b
        elif c=='/':
            d = a / b
        else:
            d = a * b
        d = round(d, 2)
        answer = str(a) + str(c) + str(b) + ' = ' + str(d)
        e = random.choice(['a','b','c','d'])
        if e=='a':
            problem = 'A ' + str(c) + str(b) + ' = ' + str(d)
            i = input_cleaner(problem)
            if int(i) == a:
                main_menu(2)
                print(f'{indent}Correct ' + answer)
                buff_confirm()
                score += 2
                correct += 1
            else:
                main_menu(2)
                print(f'{indent}Incorrect! the answer for ' + problem + ' is ' + str(a))
                buff_confirm()
                incorrect.append([problem, answer, i])
        if e=='b':
            problem = str(a) + str(c) + 'A' + ' = ' + str(d)
            i = input_cleaner(problem)
            if int(i) == b:
                main_menu(2)
                print(f'{indent}Correct ' + answer)
                buff_confirm()
                score += 2
                correct += 1
            else:
                main_menu(2)
                print(f'{indent}Incorrect! the answer for ' + problem + ' is ' + str(b))
                buff_confirm()
                incorrect.append([problem, answer, i])
        else:
            problem = str(a) + str(c) + str(b) + ' = ' + 'A'
            i = input_cleaner(problem)
            if int(i) == d:
                main_menu(2)
                print(f'{indent}Correct ' + answer)
                buff_confirm()
                score += 2
                correct += 1

            else:
                main_menu(2)
                print(f'{indent}Incorrect! the answer for ' + problem + ' is ' + str(d))
                buff_confirm()
                incorrect.append([problem, answer, i])
        

def comp_cleaner(i):
    while True:
        main_menu(2)
        print(f'{indent}Please enter <, >, or =')
        print(f'{indent}{i}')
        user = input(f'{indent}:')
        if user in ['<','>','=']:
            return user

def comparison():
    global score
    global correct
    global incorrect
    a = random.randint(3,25)
    b = random.randint(1,a-1)
    c = random.randint(3,25)
    d = random.randint(1,c-1)
    e = f"""
{indent}{str(b)}    {str(d)}
{indent}---  ---
{indent}{str(a)}    {str(c)}
"""
    answer = ''
    ba = b/a
    print('c')
    dc = d/c
    if ba>dc:
        answer = '>'
    elif ba<dc:
        answer = '<'
    else:
        answer = '='
    problem = e
    i = comp_cleaner(problem)
    if i==answer:
        main_menu(2)
        print(f'{indent}Correct the answer to \n' + problem + f'\n{indent}is ' + answer)
        buff_confirm()
        score += 3
        correct += 1
    else:
        main_menu(2)
        print(f'{indent}Incorrect! the answer for \n' + problem + f'\n{indent}is ' + answer)
        buff_confirm()
        incorrect.append([problem, answer])

def input_choice(i):
    while True:
        main_menu(2)
        print(f'{indent}Are you happy with your input? [yes or no]')
        print(f'{indent}{i}')
        print('')
        user = input(f'{indent}:')
        if len(user) ==0:
            continue
        elif user.upper()[0]=='Y':
            return True
        elif user.upper()[0]=='N':
            return False


def input_avg(sample):
    while True:
        main_menu(2)
        s=[]
        for i in sample:
            s.append(str(i))
        s=','.join(s)
        mean = input_cleaner(f'Please enter the mean for ' + s)
        median = input_cleaner(f'Please enter the median for ' + s)
        mode = input_cleaner(f'Please enter the mode for ' + s)
        ranged = input_cleaner(f'Please enter the range for ' + s)
        i=(f'Mean ' + str(mean) + ', Median ' + str(median) + ', Mode ' + str(mode) + ', Range ' + str(ranged))
        if input_choice(i)==True:
            return [mean,median,mode,ranged]
        else:
            continue
        
def average():
    global score
    global correct
    global incorrect
    s = random.randint(1,50)
    sample = []
    for i in range(random.randint(4,6)):
        sample.append(s+random.randint(-5,10))
    if negative(1)>0:
        sample = sorted(sample)
    avg = round(statistics.mean(sample),2)
    try:
        mode = statistics.mode(sample)
    except statistics.StatisticsError:
        mode = 0
    try:
        median = statistics.median(sample)
    except statistics.StatisticsError as e:
        median = 0
    ranged = max(sample)-min(sample)
    i=(input_avg(sample))
    answer=[avg, median, mode, ranged]
    str_answer = []
    str_sample = []
    for x in answer:
       str_answer.append(str(x))
    for y in sample:
        str_sample.append(str(y))
    str_answer = ','.join(str_answer)
    str_sample = ','.join(str_sample)
    for n in range(0,3):
        if i[n]==answer[n]:
            continue
        else:
            main_menu(2)
            print(f'{indent}Incorrect! the answer for ' + str_sample + f'\n{indent}The correct answer is a mean, median, mode, and range of ' + str_answer)
            buff_confirm()
            incorrect.append([sample, answer,i])
            return
    else:
        main_menu(2)
        print(f'{indent}Correct, your answer for ' + str_sample + f'\n{indent}Is correct with a mean, median, mode, range of ' + str_answer)
        buff_confirm()
        score += 8
        correct += 1
        return
    
def problem_choser(score):
    if score < question-4:
        random.choice([multiplication,simple_algebra,comparison,average])()
    elif score < question-3:
        random.choice([multiplication,simple_algebra,comparison])()
    elif score < question-2:
        random.choice([multiplication,simple_algebra])()
    else:
        multiplication()

def set_queue():
        if (os.path.isfile(queue))!=True:
                create_file(queue)
        f = open(queue,'a+')
        f.write('5\n')
        f.close()
        
def allocate_time():
        main_menu(3)
        set_queue()
        buff_confirm()
        
def daily_problems():
    while score < question:#try 40 or 30 problems
        problem_choser(score)
    else:
        allocate_time()


def menu_items():
        menu = ['[1] Complete your daily problems','[2] Quit']
        for i in menu:
                print(' '*30+i)
                
def getdate():
        config =  configparser.ConfigParser()
        config.read(file)
        data = config['DATA']['DATE']
        return data

def attempted():
        date = getdate()
        today = datetime.date.today()
        message1 = 'You have already completed todays problem.'
        if date!=str(today):
                daily_problems()
        else:
                main_menu(1)
                print(indent + message1.center(60,' '))
                buff_confirm()
                
def choser(options):
        while True:
                print('')
                print('')
                print('')
                choice = input(f'{indent}')
                if choice not in options:
                        return None
                else:
                        return choice

    
def exit_prog():
    main_menu(1)
    message1=('Exiting the program.')
    print(indent + message1.center(60,' '))
    buff_confirm()
    sys.exit(0)


def main():
    while True:
        main_menu(1)
        menu_items()
        choice = choser(['1','2'])
        if choice!=None:
            if choice == '1':
                attempted()
            elif choice == '2':
                exit_prog()
        else:
            continue
        
main()
