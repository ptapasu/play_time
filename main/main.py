import os
import re
import ctypes
import datetime
import time
import configparser
from pygame import mixer
import zc.lockfile
import logging
logging.basicConfig(filename='./app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
#info... whats happening... debug... check for bad stuff (use with variables?) error... exceptioins.


"""Ensure that the program is not running on startup"""
try:
    lock = zc.lockfile.LockFile('./lock/main_lock')
except zc.lockfile.LockError:
    logging.error('An instance of this program is already running!')
    sys.exit(0)

def get_block_list():
    """Reads the black (Blacklist) file, strips the whitespace and newline, appends to list,
        then joins list as 'a|b|c' for the taskkill program"""
    logging.debug('Getting the blocked app list')
    file = './black'
    block = []
    try:
        read_file = open(file,'r')
    except:
        logging.error(f'The {file} path is missing.')
    data = read_file.readlines()
    for i in data:
            block.append(i.strip())
    read_file.close()  
    block = '|'.join(block)
    return (block)

def get_app (pid):
    logging.debug(f'Using PID {pid} to get the APP name')
    data = os.popen(f'tasklist /svc /FI "PID eq {pid}"')
    for i in data:
        if pid in i:
            return (i.split()[0])
        
def app_killer():
    """Using the list from the black file, identifies programs it needs to kill, and terminates them"""
    logging.debug('Running the appkiller')
    kill_list = []
    tasklist=os.popen('tasklist').readlines()
    targets = get_block_list()
    search = '.{0,}(' + targets + ')+.{0,}'
    row_search = re.compile(search, re.IGNORECASE)
    logging.debug(f'Searching using this re search query {row_search}')
    pid_search = re.compile('\s{1}\d{4,}\s{1}', re.IGNORECASE)
    for i in tasklist:
        if row_search.match(i)!=None:
            target_pid = pid_search.search(i)
            logging.debug(f'Found a match with the PID number {target_pid.group().strip()}')
            if target_pid!=None:
                kill_list.append(target_pid.group().strip())
    for i in kill_list:
        try:
            os.kill(int(i), 15)
        except OSError:
            app_name = get_app(i)
            logging.debug(f'Could not kill the file {app_name} with PID number {i}')
            continue
        
def read_data(x):
    """return the date, time and state of the data file"""
    logging.debug('Running the read_data function')
    config = configparser.ConfigParser()
    config.sections()
    try:
        config.read('./config')
        logging.info(f'Trying to read the value {x} from the config file')
        return(config['DATA'][x])
    except KeyError:
        logging.error('The config file or an entry in it cannot be found')


def play_audio(x):
    logging.debug('Running the play_audio function')
    try:
        mixer.init()
        mixer.music.load(x)
        mixer.music.play()
        logging.debug(f'User recieved audio warning {x}')
    except:
        logging.error(f'Problem finding or playing the file {x}')

def audio_warning(t):
    if t == 180:
        play_audio('./audio/3h.mp3')
    elif t == 150:
        play_audio('./audio/2.5h.mp3')
    elif t == 120:
        play_audio('./audio/2h.mp3')
    elif t == 90:
        play_audio('./audio/1.5h.mp3')
    elif t == 60:
        play_audio('./audio/1h.mp3')
    elif t == 45:
        play_audio('./audio/45m.mp3')
    elif t == 30:
        play_audio('./audio/30m.mp3')
    elif t == 15:
        play_audio('./audio/15m.mp3')
    elif t == 5:
        play_audio('./audio/5m.mp3')
    elif t == 1:
        play_audio('./audio/finished.mp3')
            
def cutoff_warning(t):
    if t == 60:
        play_audio('./audio/60cutoff.mp3')
    elif t == 45:
        play_audio('./audio/45cutoff.mp3')
    elif t == 30:
        play_audio('./audio/30cutoff.mp3')
    elif t == 15:
        play_audio('./audio/15cutoff.mp3')
    elif t == 1:
        play_audio('./audio/finished.mp3')
        
def alter_data(key,value):
    logging.debug('Writing to the config and info files')
    files = ['./config']
    for path in files:
        config =  configparser.ConfigParser()
        config.read(path)
        config['DATA'][key] = value
        with open(path, 'w') as configfile:
            logging.debug(f'Writing {key} {value} to {path}')
            config.write(configfile)

def erase():
    """Deletes the data in the queue file"""
    logging.debug('Erasing the data in the queue file')
    file = './queue'
    open(file, 'w')
    alter_data('QUEUE_TIME',str(os.path.getmtime('./queue')))
    b.queue_time = str(os.path.getmtime('./queue'))

def reset_log():
    """Deletes the data in the queue file"""
    logging.debug('Erasing the data in the log file')
    file = './app.log'
    open(file, 'w')
    
def q_switch(n):
    if n[0]=='1':
        logging.debug('Setting the state to on')
        alter_data('state','ON')
        b.state = 'ON'
    elif n[0]=='2':
        logging.debug('Setting the state to off')
        alter_data('state','OFF')
        b.state = 'OFF'
    elif n[0]=='3':
        logging.debug(f'Increasing the playtime')
        add = int(n.split('=')[1])
        new_time = str(int(b.play_time)+add)
        alter_data('play_time',new_time)
        b.play_time = new_time
    elif n[0]=='4':
        logging.debug('Changing the end time')
        time = n.split('=')[1]
        alter_data('end_time',time)
        b.end_time = time
    elif n[0]=='5':
        logging.debug('Setting the state to on')
        alter_data('date',str(datetime.date.today()))
        b.date = str(datetime.date.today())
        alter_data('play_time','120')
        b.play_time = '120'
        alter_data('state','OFF')
        b.state = 'OFF'
        alter_data('end_time','23:00')
        b.end_time = '23:00'
            
def queue_reader():
    logging.debug(f'Reading the queue file')
    file = './queue'
    read_file = open(file,'r')
    file_data = read_file.readlines()
    for i in file_data:
        if len(i)>1:
            q_switch(i)
    read_file.close()
    erase()
            
def check_queue(saved_timestamp):
    """Checks to see if the queuefile has changed"""
    file_timestamp = str(os.path.getmtime('./queue'))
    logging.info(f'The saved timestamp is {saved_timestamp} and the files time stamp is {file_timestamp}')
    if file_timestamp != saved_timestamp:
        logging.debug('A difference in the timestamps was found!')
        queue_reader()
    else:
        return

def check_time(start_time,end_time):
    """Get the current time and make sure it is after the start time, but before the end time"""
    current_time = ((((str(time.ctime())).split())[3])[0:5])
    if start_time<current_time and current_time<end_time:
        return True
    else:
        return False


class monitor:
    def __init__(self):
        self.date = read_data('date')#change to read config
        if self.date == str(datetime.date.today()):
            self.play_time = int(read_data('play_time'))
        else:
            self.play_time = '0'
        self.state = 'OFF'
        self.startup_time = read_data('start_time')
        self.end_time = read_data('end_time')
        self.queue_time = read_data('queue_time')
        self.on_counter = 0
        
    def activate(self):
        logging.debug('Turning the state to "ON"')
        self.state = 'ON'
        self.on_counter = 0
        
    def deactivate(self):
        logging.debug('Turning the state to "OFF"')
        self.state = 'OFF'
        
    def mins_end_time(self):
        difference_hour = ((int(self.end_time[0:2]))-int(time.ctime()[11:13]))*60
        difference_min = ((int(self.end_time[3:5]))-int(time.ctime()[14:16]))
        countdown = difference_hour + difference_min
        logging.debug(f'The amount of minutes untill the cut-off (end_time) is {countdown}')
        if countdown in [1,15,30,45,60]:
            logging.debug(f'Issuing a warning about the approaching end time: {self.end_time} which is {countdown} minutes away')
            coutoff_warning(countdown)

    def mins_play_time(self):
        if self.play_time in ['180','150','120','90','60','45','30','15','5','1']:
            logging.debug(f'Playing warning as a milestone has been reached when counting down playtime: {self.play_time}')
            audio_warning(int(self.play_time))
            
    def counter(self):
        self.on_counter +=1
        logging.debug(f'The current count is {self.on_counter}')
        if int(str(self.on_counter/6).split('.')[1]) == 0:
            logging.debug('Sixty seconds have passed.')
            q_switch('3=-1')
            self.mins_end_time()
            self.mins_play_time()
            
    def on(self):
        logging.debug('State is on')
        self.counter()
        
    def off(self):
        logging.debug('State is off')
        app_killer()

    def get_state(self):
        check_queue(self.queue_time)
        if self.state=='ON':
            if check_time(self.startup_time, self.end_time):
                logging.debug(f'The time is between the startup time {self.startup_time} and end time {self.end_time}')
                if int(self.play_time)>0:
                    logging.debug(f'The play time is {self.play_time} which is larger than 0')
                    self.on()
        else:
            self.off()
        
b = monitor()

def main_loop():
    reset_log()#erase log file
    q_switch('2')#initialize off
    while True:
        b.get_state()
        time.sleep(10)
        logging.debug('Main loop interation')
    
if __name__=="__main__":
    main_loop()


