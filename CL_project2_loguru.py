#===============================================================================
# Author: Christian Liguori
# Date: 03/30/21
# Program Name: CL_project2_loguru.py
# This program creates a simulated web server that is both sending data and 
#   receiving requests that logs all of the activity using the loguru python 
#   library. It showcases how the loguru library can be used to easily create
#   logs and output them to both the console, using stderr and to a file with
#   automatic file rotation, deletion and compression. 
#===============================================================================


#===============================================================================
# Library Imports
#===============================================================================
# Handle an import error if the loguru library was not installed.
try:
    from loguru import logger
except ImportError:
    print(
        '''
        The Loguru library was not found. 
        Install the library by typing the following into your terminal: 
            pip install loguru
        '''
    )

    exit()

# These libraries are part of either the standard python libraries or 
#   included in the anaconda packages and are assumed to be installed.
import asyncio
import random
import sys
import time
#===============================================================================


#===============================================================================
# Setting up the logger
#===============================================================================
# This function is used to filter out log messages that are not of a specific 
#   level. It is used to further customize the terminal log messages.
def info_filter(record):
    if record['level'].name == 'INFO':
        return True
    else:
        return False

# This function is used to filter out log messages that are not of a specific 
#   level. It is used to further customize the terminal log messages.
def warning_filter(record):
    if record['level'].name == 'WARNING':
        return True
    else:
        return False        

# The logger.remove() method removes all previously defined handlers for the
#   log messages and in this case, it removes all of the default handlers.
logger.remove()

# Setting up a handler for logging to the console that styles log messages with
#   a level of INFO
logger.add(
    sys.stderr, 
    level='INFO', 
    format='<green>{time}</green> | <GREEN><black>{level}</black></GREEN>' + \
        '\n{message}', 
    filter=info_filter
    )

# Setting up a handler for logging to the console that styles log messages with
#   a level of WARNING
logger.add(
    sys.stderr, 
    level='WARNING', 
    format='<yellow>{time}</yellow> | <YELLOW><black>{level}</black></YELLOW>'+\
        '\n{message}', 
    filter=warning_filter
    )    

# Setting up a handler for logging to the console that styles log messages with
#   a level of CRITICAL
logger.add(
    sys.stderr, 
    level='CRITICAL', 
    format='<b><red>{time} | <RED><white>{level}</white></RED> ' + \
        '\n{message}</red></b>'
    )

# Setting up a handler for logging to a file that rotates, deletes and 
#   compresses files automatically.
logger.add(
    'web_server.log',
    level='INFO',
    format='{level} | {time} \n{message}',
    rotation='10 kb',
    retention='10 seconds',
    compression='zip'
)
#===============================================================================


#===============================================================================
# Connection class:
# The connection class holds the data for a connection and also generates that
#   data randomly.
#===============================================================================
class Connection:
    # constructor
    def __init__(self):
        # generate a random IP number
        self.ip = str(random.randint(20,250)) + \
            '.' + str(random.randint(5,250)) + \
            '.' + str(random.randint(20,250)) + \
            '.' + str(random.randint(20,250))

        # generate a random file that is being requested
        self.request = 'my_cool_website/' + random.choice([
            'home',
            'about',
            'forums',
            'events/picnic',
            'events',
            'events/pool_party',
            'events/programming_class'
        ]) + '.html'

        # generate some random user information
        self.user_agent = random.choice([
            'Mozilla',
            'Edge',
            'Chrome',
            'Safari'
        ])

        # generate a timestamp that represents when the request was received
        self.timestamp = time.time()
#===============================================================================


#===============================================================================
# Simulatied Server class:
# This class contains all of the methods for randomly creating server events and
# logging them using the Loguru python library.
#===============================================================================
class Simulated_Server:
    requests = [] # Used to store the requests that were received

    # constructor that sets the number of ticks to be performed before asking
    #   the user if they want to continue the simulation and starts the async
    #   loop for the simulated server.
    def __init__(self, ticks):
        self.ticks_remaining = ticks
        asyncio.run(self.tick())

    # Async function that generates random server events and loops until 
    #   user ends the simulation.
    async def tick(self):
        # If the timer has run out for the simulation prompt the user to 
        #   continue or quit.
        if self.ticks_remaining < 1:
            if input('Continue simulation for 20 more seconds? (Y or N): ')\
                .upper() == 'Y':
                
                self.ticks_remaining = 40
            else:
                print('Exiting simulation.')
                exit()

        # randomly generate a request being received
        if random.randint(1,4) == 1:
            self.request_received(Connection())

        # randomly generate a response being sent
        if random.randint(1,4) == 1:
            self.send_response()

        # randomly generate a warning event
        if random.randint(1,10) == 1:
            self.generate_warning()

        # randomly generate an error event
        if random.randint(1,15) == 1:
            self.generate_error()

        self.ticks_remaining -= 1 # decrease number of ticks remaining

        await asyncio.sleep(.5) # wait for half a second, async
        await self.tick() # call this tick method again to continue loop

    # function that simulates the processing of a request    
    def request_received(self, connection):
        self.log_request(connection) # log the request
        
        self.requests.append(connection) # add the request to the request list

    # function that simulates the processing of a response
    @logger.catch
    def send_response(self):
        # The code sets up a situation that may result in an error to showcase 
        #   more error handling messages.
        try:
            request = self.requests.pop(0) # get a request from the list
        except IndexError:
            logger.critical(
                '''
            ERROR: Tried to respond to a request that does not exist.
                '''
            )
            return False

        self.log_response(request) # log the response

    # function that generates a log message using a connection's data
    def log_request(self, connection):
        logger.info(
            '''
            Request Received:
            IP: {ip},
            Request: {req},
            User-Agent: {ua}
            '''.format(ip=connection.ip,req=connection.request, \
                ua=connection.user_agent)
        )

    # function that generates a log message using a connection's data
    def log_response(self, connection):
        logger.info(
            '''
            Response Sent:
            IP: {ip},
            Data: {req},
            Timestamp: {ts}
            '''.format(ip=connection.ip,req=connection.request, \
                ts=connection.timestamp)
        )

    # function that generates a warning message
    def generate_warning(self):
        logger.warning(
            '''
            WARNING: High volumes of traffic are being generated from this 
            ip: {} 
            '''.format(Connection().ip)
        )

    # function that generates a crital message
    def generate_error(self):
        logger.critical(
            '''
            CRITICAL: Lost connection to SQL server at this ip: {}
            '''.format(Connection().ip)
        )
#===============================================================================


#===============================================================================
# Setting up and starting the simulation
#===============================================================================
# Display a message to the user about the simulation.
print(
    '''
#===============================================================================
        Hello, this program simulates a server that is sending and 
        receiving data to and from various connections and uses the 
        Loguru library to log the activity, both in the terminal and in
        files. In the terminal, the messages have been formatted and 
        styled with different colors based on the severity of the 
        message. If you watch the location (folder) that this program is
        run in, you will see files being created, deleted and 
        compressed. The rates for these operations are much shorter than 
        normal to showcase the library. The sending and receiving of 
        data is completely random.
#===============================================================================
    '''
)

input('Press any key to continue:') # wait for user input to continue

# Explain how the simulation will progress
print(
    '''
    The server simulation will last about 20 seconds and then a prompt
    to continue the simulation will displayed.
    '''
    )

# Trigger to start the simulation
input('\nPress any key to start the simulation:')

Simulated_Server(40)

#===============================================================================