#make sure python is set in the environmental variables in powershell this will prevent 
#make sure three files are present from a list (queue, lock, and log.txt)
#way to send message from one process to another??????????
import os
import re#used in appkiller
import ctypes#is this used for anything?
import datetime
import time
import sys
import configparser
from pygame import mixer
import zc.lockfile
import logging

def logger():
    """A tool for logging events in the program to alter the log reporting change the level: logging.INFO, logging.DEBUG, logging.ERROR"""
    logging.basicConfig(filename='./app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
    logging.error(f'===Instance of app started {datetime.datetime.now()}===')

#lets have the file checker... but have a default flag for input such as p or something... anyway...
    #when it runs and that default flag is there just run a loop for all the three files, otherwise if input.. say lock... just run it for that one file.
def q_maker():
    file = './queue'
    if (os.path.isfile(file))!=True:
        with open(file, 'w') as file:
            logging.error('No queue file found, so queue created in current dir')
            file.write('')
            
def instance_check():
    """Make sure a lock file is present. Ensure that another instance of this program is not already running."""
    file = './lock'
    if (os.path.isfile(file))!=True:
        with open(file, 'w') as file:
            logging.error('No lock file found, so lockfile created in current dir')
            file.write('')
    try:
        lock = zc.lockfile.LockFile(file) #make it so if no file, it will be created
    except zc.lockfile.LockError:
        logging.error('An instance of this program is already running!')
        sys.exit(0)

def int_block_list():
    """An internal list of stuff to block"""
    block = ['steam','blizzard','epic','minecraft','gog','galaxy','battle.net.exe','fortnite','roblox','origin','uplay']
    return '|'.join(block)

def get_block_list():
    """DEPRECATED: Reads the black (Blacklist) file, strips the whitespace and newline, appends to list,
        then joins list as 'a|b|c' for the taskkill program"""
    file = './data/black'
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
    """This grabs the PID if it finds the name from the blocklist"""
    logging.debug(f'Using PID {pid} to get the APP name')
    data = os.popen(f'tasklist /svc /FI "PID eq {pid}"')
    for i in data:
        if pid in i:
            return (i.split()[0])
        
def app_killer():
    """Using terms from the black file, identifies programs it needs to kill, and terminates them"""
    logging.debug('Running the taskkiller')
    kill_list = []
    tasklist=os.popen('tasklist').readlines()
    targets = int_block_list()#changed to internal from the function which gets an external block list named get_block_list
    search = '.{0,}(' + targets + ')+.{0,}'
    row_search = re.compile(search, re.IGNORECASE)
    logging.debug(f'Searching using this re search query {row_search}')
    pid_search = re.compile('\s{1}\d{4,}\s{1}', re.IGNORECASE)
    for i in tasklist:
        if row_search.match(i)!=None:
            target_pid = pid_search.search(i)
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
    """return the date, time and state of the data file, for the namedvalue x"""
    default = {'date':datetime.date.today(),'play_time':'0','state':'OFF','start_time':'10:00','end_time':'20:30','queue_time':'0'}

    #here is where problems... so just set everything to 0 if no file found for config lets have a default dict that returns... date today, time 0, 
    config = configparser.ConfigParser()
    config.sections()
    try:
        config.read('./data/config')
        logging.info(f'Trying to read the value {x} from the config file')
        return(config['DATA'][x])
    except KeyError:
        logging.error('The config file or an entry in it cannot be found')
        return default[x]

def play_audio(x):
    """Runs the audio output to inform the kids of times etcetera"""
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
        #ADD a sound for turning off
def cutoff_warning(t):
    if t == 60:
        play_audio('./audio/60cutoff.mp3')
    elif t == 45:
        play_audio('./audio/45cutoff.mp3')
    elif t == 30:
        play_audio('./audio/30cutoff.mp3')
    elif t == 15:
        play_audio('./audio/15cutoff.mp3')
  
def alter_data(key,value):
    """alters the value for a specific key in the config and info files"""
    #data files don't exist what do we do then????
    files = ['./data/config','./data/info']
    for path in files:
        config =  configparser.ConfigParser()
        try:
            config.read(path)
            config['DATA'][key] = value
            with open(path, 'w') as configfile:
                logging.debug(f'Writing {key} {value} to {path}')
                config.write(configfile)
        except KeyError:
            logging.error(f'The config file {path} an entry in it cannot be found')

def erase():
    """Deletes the data in the queue file"""
    file = './queue'
    try:
        open(file, 'w')
        alter_data('QUEUE_TIME',str(os.path.getmtime('./data/queue')))
        b.queue_time = str(os.path.getmtime('./data/queue'))
    except FileNotFoundError:
        logging.error(f'The queue file cannot be found')
    
def q_switch(n):
    if n[0]=='1':
        alter_data('state','ON')
        b.state = 'ON'
    elif n[0]=='2':
        alter_data('state','OFF')
        b.state = 'OFF'
    elif n[0]=='3':
        add = int(n.split('=')[1])
        new_time = str(int(b.play_time)+add)
        alter_data('play_time',new_time)
        b.play_time = new_time
    elif n[0]=='4':
        time = n.split('=')[1]
        alter_data('end_time',time)
        b.end_time = time
    elif n[0]=='5':
        alter_data('date',str(datetime.date.today()))
        b.date = str(datetime.date.today())
        alter_data('play_time','240')
        b.play_time = '240'
        alter_data('state','OFF')
        b.state = 'OFF'
        alter_data('end_time','20:30')
        b.end_time = '20:30'
            
def queue_reader():
    """reads the data in the cue, the closes it and erases the data in the file"""
    #if there is not queue file set data to 0
    file = './queue'
    try:
        read_file = open(file,'r')
        file_data = read_file.readlines()
        for i in file_data:
            if len(i)>1:
                q_switch(i)
        read_file.close()
        erase()
    except FileNotFoundError:
        logging.error(f'The queue file cannot be found')
        q_maker()
        
def check_queue(saved_timestamp):
    #if no timestamp coz no file
    """Checks to see if the timestamp has changed in the file"""
    try:
        file_timestamp = str(os.path.getmtime('./queue'))
        logging.info(f'The saved timestamp is {saved_timestamp} and the files time stamp is {file_timestamp}')
        if file_timestamp != saved_timestamp:
            logging.info('A difference in the timestamps was found!')
            queue_reader()
        else:
            return
    except FileNotFoundError:
        logging.error(f'The queue file cannot be found')
        q_maker()
        
def check_time(start_time,end_time):
    """Get the current time and make sure it is after the start time, but before the end time"""
    current_time = ((((str(time.ctime())).split())[3])[0:5])
    if start_time<current_time and current_time<end_time:
        return True
    else:
        return False


class monitor:
    """creates the class which runs a monitor system"""
    def __init__(self):
        self.date = read_data('date')#change to read config
        if self.date == str(datetime.date.today()):
            self.play_time = int(read_data('play_time'))
        else:
            self.play_time = 0
        self.state = 'OFF'
        #self.state = 'OFF' #should also set time to off
        self.startup_time = read_data('start_time')
        self.end_time = read_data('end_time')
        self.queue_time = read_data('queue_time')
        self.on_counter = 0
        #wipe the log... on startup
        #don't need to update unless a) queue file change or b) startup
        
    def activate(self):
        """switches the state to on"""
        logging.debug('Turning the state to "ON"')
        self.state = 'ON'
        self.on_counter = 0
        
    def deactivate(self):
        """switches the state to off"""
        logging.debug('Turning the state to "OFF"')
        self.state = 'OFF'
        
    def mins_end_time(self):
        difference_hour = ((int(self.end_time[0:2]))-int(time.ctime()[11:13]))*60
        difference_min = ((int(self.end_time[3:5]))-int(time.ctime()[14:16]))
        countdown = difference_hour + difference_min
        logging.info(f'The amount of minutes untill the cut-off (end_time) is {countdown}')
        if countdown in [15,30,45,60]:
            logging.debug(f'Issuing a warning about the approaching end time: {self.end_time} which is {countdown} minutes away')
            coutoff_warning(countdown)

    def mins_play_time(self):
        if self.play_time in ['180','150','120','90','60','45','30','15','5']:
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

    def program_killer(self):
        try:
            logging.info(f'---app kill file created, app terminated at {datetime.datetime.now()}---')
            read_file = open('kill','r')
            sys.exit()
        except Exception:
            logging.info('No kill file found')
        
    def get_state(self):
        check_queue(self.queue_time)
        self.program_killer()
        if self.state=='ON':
            if self.date==str(datetime.date.today()):
                logging.info("The config file and today's date match")
                if check_time(self.startup_time, self.end_time):
                    logging.info(f'The time is between the startup time {self.startup_time} and end time {self.end_time}')
                    if int(self.play_time)>0:
                        logging.info(f'The play time is {self.play_time} which is larger than 0')
                        self.on()
        else:
            self.off()
            #play a sound here, or call on the audio thingee
logger()
instance_check()    
b = monitor()

def main_loop():
    q_switch('2')
    while True: #always on
        b.get_state()
        time.sleep(9)
        logging.info('An iteration of the main loop is running')
    
if __name__=="__main__":
    main_loop()


