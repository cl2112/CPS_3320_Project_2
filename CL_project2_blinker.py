#===============================================================================
# Author: Christian Liguori
# Date: 03/30/21
# Program Name: CL_project2_blinker.py
# This program simulates users chatting with one another and uses the 
#   blinker library to send and receive messages between user objects. It
#   showcases using the blinker library as a way to pass messages between
#   objects and as a way to coordinate function calls.
#===============================================================================


#===============================================================================
# Library Imports
#===============================================================================
# Handle an import error if the blinker library was not installed.
try:
    from blinker import signal
except ImportError:
    print(
        '''
        The Blinker library was not found. 
        Install the library by typing the following into your terminal: \
            pip install blinker
        '''
    )

    exit()

# These libraries are part of either the standard python libraries or 
#   included in the anaconda packages and are assumed to be installed.
import time
import asyncio
import random
#===============================================================================


#===============================================================================
# Tick_Manager class:
# The tick manager is used to coordinate all of the simulated chat 
#   events between the users. It sends out a message about every
#   second that the user bots will use to determine when to send a message.
#===============================================================================
class Tick_Manager:
    tick_signal = signal('tick') # Create instance of the tick signal

    data = {'ticks_remaining': 0, 'users': []} # used to store any data needed

    # constructor that sets the number of ticks to be performed before asking
    #   the user if they want to continue the simulation and starts the async
    #   loop for the simulated server.
    def __init__(self):
        self.data['ticks_remaining'] = 30
        asyncio.run(self.tick())

    # an async function that emits a pulse that other functions can listen for.
    #   The pulse happens about once every second. It will also randomly
    #   create a new user. It also will loop forever.
    async def tick(self):
        # send a tick signal and this object as data. 
        self.tick_signal.send(self)
        
        # If the timer has run out for the simulation prompt the user to 
        #   continue or quit.
        if self.data['ticks_remaining'] < 1:
            if input('Continue simulation for 30 more seconds? (Y or N): ')\
                .upper() == 'Y':
                
                self.data['ticks_remaining'] = 30
            else:
                print('Exiting simulation.')
                exit()
        
        # Randomly create a new user, simulates a new user logging in to
        #   chat room.
        if random.randint(1,20) == 1:
            self.data['users'].append(User(random.choice([
                'Ann',
                'Jeff',
                'Mary',
                'Jose',
                'Felix',
                'Becca',
                'Heather'
            ])))

        self.data['ticks_remaining'] -= 1 # decrease number of ticks remaining

        await asyncio.sleep(1) # wait for a second, async
        await self.tick() # call this tick method again to continue loop
#===============================================================================

#===============================================================================
# User class:
# The user class simulates all of the chat messages created by users.
#===============================================================================
class User:
    # create instances of all of the signals needed
    tick = signal('tick')
    chat_msg = signal('chat_msg')
    logon = signal('logon')
    logon_msg = signal('logon_msg')

    # tick check is used to randomize the time between chat messages
    tick_check = random.randint(1,10)

    # num_msg_sent is used to determine when to send certain messages
    num_msg_sent = 0

    # constructor that sets the name field, connects to the tick and
    #   logon signals, and sends a logon message
    def __init__(self, name):
        self.name = name
        self.tick.connect(self.handle_tick)
        self.logon_msg.send('{} HAS LOGGED ON.'.format(self.name.upper()))
        self.logon.send(self.name)
        self.logon.connect(self.handle_logon)

    # function that acts after each tick event is received and determines if
    #   the user should send a chat message.
    def handle_tick(self, data):
        if self.tick_check < 1:
            self.send_msg()
            self.tick_check = random.randint(1,5)
        else:
            self.tick_check -= 1

    # function that sends a random chat message based on how many messages have
    #   been sent by the user so far.
    def send_msg(self):
        if self.num_msg_sent == 0:
            self.chat_msg.send('{}: '.format(self.name) + random.choice([
                'Hello, how is everyone?',
                'Hey guys, how\'s it going?',
                'Yoooooo',
                'hey people',
                'Did you hear what happened to Jim?'
            ]))
        elif self.num_msg_sent > 10:
            self.chat_msg.send('{}: '.format(self.name) + random.choice([
                'I gotta go, talk to you later.',
                'later guys',
                'Alright, I\'m out',
                'I\'ll be on later.'
            ]))
            self.logoff(self)
        else:
            self.chat_msg.send('{}: '.format(self.name) + random.choice([
                'cool, cool',
                'I did hear about it. And it is crazy.',
                'Did any one see that movie I recommended last time?',
                'no',
                'Nope',
                'nah',
                'yep',
                'yeah',
                'Dude, I finally beat that damn boss.',
                'nice',
                'congrats',
                'Nice day today.',
                'Did you ever find that book I lent you?',
                'and...'
            ]))

        self.num_msg_sent += 1 # increase the number of messages sent

    # function called by the user to simulate a user logging off from chat.
    def logoff(self, data):
        self.chat_msg.send('{} HAS LOGGED OFF.'.format(self.name.upper()))
        self.tick.disconnect(self.handle_tick)
        self.logon.disconnect(self.handle_logon)

    # function called by the user when a logon message is received to 
    #   simulate users greeting a new user that has joined the chat.
    def handle_logon(self, name):
        time.sleep(1)
        self.chat_msg.send('{}: '.format(self.name) + random.choice([
            'hey ',
            'howdy ',
            'ayyy, sup '
        ]) + '{}'.format(name))
#===============================================================================


#===============================================================================
# Setting up and starting the simulation:
#===============================================================================
# Display a message to the user about the simulation.
print(
    '''
#===============================================================================
        Hello, this program simulates a chat app with multiple users. It 
    showcases some uses of the blinker python library. Using the blinker 
    library makes it easy for functions to be called in response to an 
    event or signal and for data to be passed between objects without the
    sender or receiver of the data needing to know anything about the other.
#===============================================================================
    '''
)

input('Press any key to continue:') # wait for user input to continue

# Explain how the simulation will progress
print(
    '''
    The chat app simulation will last about 30 seconds and then a prompt
    to continue the simulation will displayed.
    '''
    )

# trigger to start the simulation
input('Press any key to start the simulation.')

# This function serves as a chat window that displays the messages between
#   the users and any events.
def print_chat_msg(msg):
    print(msg)

# Create and subscribe to the chat_msg signal and logon signal
chat_msg = signal('chat_msg').connect(print_chat_msg)
logon_msg = signal('logon_msg').connect(print_chat_msg)

# Create initial simulated users
Chris = User('Chris')
Doug = User('Doug')
Jess = User('Jess')

# Start the instance of the tick manager
Tick_Manager()

#===============================================================================