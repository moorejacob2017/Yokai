import sys
import os
import json
import pytz
import dateutil.parser
import pickle
import select
import subprocess
import signal
import fcntl
import errno
import logging
import string
import random
from io import StringIO
from datetime import datetime, time
from multiprocessing import Process, Manager
from time import sleep

#==========================================================================================================
class ExecutionScheduler:
    """
    ExecutionScheduler class to determine whether a command should be executed at a specific time.

    Attributes:
    - start_time: (datetime.time) The time of day at which the allowed execution period starts.
    - end_time: (datetime.time) The time of day at which the allowed execution period ends.
    - allowed_days: (list) The days of the week on which execution is allowed.
    - unlimited_days: (list) The days of the week on which execution is allowed at any time.
    - halt_days: (list) The days of the week on which execution is not allowed.
    - special_days: (list) A list of dictionaries that define special periods of time with either unlimited execution or no execution.
    - timezone: (str) The timezone to use when checking the current time.

    EXAMPLE:
    scheduler = ExecutionScheduler(
        start_time=time(8, 30), 
        end_time=time(17, 30),
        allowed_days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        unlimited_days=['Saturday'],
        halt_days=['Sunday'],
        special_days=[
            {
                'start': '2023-12-24', 
                'end': '2023-12-26', 
                'mode': 'halt'
            },
            {
                'start': '2024-01-01', 
                'end': '2024-01-01', 
                'mode': 'unlimited'
            }
        ]
    )
    """

    def __init__(self, 
                 start_time=time(0, 0), 
                 end_time=time(0, 0), 
                 allowed_days=[], 
                 unlimited_days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
                 halt_days=[], 
                 special_days=[],
                 timezone='UTC'):
        
        self.start_time = start_time
        self.end_time = end_time
        self.allowed_days = allowed_days
        self.unlimited_days = unlimited_days
        self.halt_days = halt_days
        self.special_days = special_days
        self.timezone = pytz.timezone(timezone)

    def _time_in_range(self, start, end, x):
        """
        Check whether a given time is within a range.

        Args:
        - start: (datetime.time) The start of the time range.
        - end: (datetime.time) The end of the time range.
        - x: (datetime.time) The time to check.

        Returns:
        - (bool) True if the time is within the range, False otherwise.
        """
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def _get_day_of_week(self, date):
        """
        Get the day of the week for a given date.

        Args:
        - date: (datetime.date) The date to check.

        Returns:
        - (str) The day of the week.
        """
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return days[date.weekday()]

    def can_execute(self):
        """
        Determine whether a command can be executed at the current time.

        Returns:
        - (bool) True if the command can be executed, False otherwise.
        """
        now = datetime.now(self.timezone)
        now_time = now.time()
        now_date = now.date()
        now_day = self._get_day_of_week(now)

        for special_day in self.special_days:
            if 'start' in special_day and 'end' in special_day:
                start = dateutil.parser.parse(special_day['start']).date()
                end = dateutil.parser.parse(special_day['end']).date()
                if start <= now_date <= end:
                    if special_day['mode'] == 'unlimited':
                        return True
                    elif special_day['mode'] == 'halt':
                        return False

        if now_day in self.unlimited_days:
            return True

        if now_day in self.halt_days:
            return False

        if now_day in self.allowed_days:
            return self._time_in_range(self.start_time, self.end_time, now_time)

        return False
    
    def to_dict(self):
        d = {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "allowed_days": self.allowed_days,
            "unlimited_days": self.unlimited_days,
            "halt_days": self.halt_days,
            "special_days": self.special_days,
            "timezone": self.timezone
        }
        return d
    
    def to_json(self):
        d = {
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "allowed_days": ', '.join(self.allowed_days),
            "unlimited_days": ', '.join(self.unlimited_days),
            "halt_days": ', '.join(self.halt_days),
            "special_days": self.special_days,
            "timezone": str(self.timezone)
        }
        return d

#==========================================================================================================

YOKAI_DIR = os.path.dirname(os.path.realpath(__file__))
os.environ["PATH"] = f"{os.getenv('PATH')}:{YOKAI_DIR}/bin"

#==========================================================================================================
# BASH - Wrapper for storing Bash command information
# PARAMETERS
#   cmd - The Bash command as a string
# ATTRIBUTES
#   command - The command to run as a string
#   started_at - The date and time that the command was run
#   finished_at - The date and time that the command finished
#   stdout - The stdout of the command
#   stderr - The stderr of the command
# FUNCTIONS
#   to_dict - Format the command and attributes as a Python Dictionary
#   to_json - Format the command and attributes as a JSON
#----------------------------------------------------------------------------------------------------------
class BASH:
    def __init__(self, cmd):
        self.command = cmd
        self.started_at = datetime.strptime("1970-01-01 00:00:00.0", "%Y-%m-%d %H:%M:%S.%f")
        self.finished_at = datetime.strptime("1970-01-01 00:00:00.0", "%Y-%m-%d %H:%M:%S.%f")
        self.stdout = ''
        self.stderr = ''

    def to_dict(self):
        d = {
            "command": self.command,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }
        return d
    
    def to_json(self):
        d = {
            "command": self.command,
            "started_at": self.started_at.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "finished_at": self.finished_at.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "stdout": self.stdout,
            "stderr": self.stderr,
        }
        return d
#==========================================================================================================

#==========================================================================================================
# PYTHON - Wrapper for storing python function information
# PARAMETERS
#   func - The function object to be ran (not a string, but the actual <function> type)
#   *args - Any arguments that the function needs to be ran with
#   **kwargs - Any keyword arguments the function needs to be ran with
# ATTRIBUTES
#   function - The function object to be ran (not a string, but the actual <function> type)
#   arguments - Any arguments that the function needs to be ran with
#   kw_arguments - Any keyword arguments the function needs to be ran with
#   started_at - The date and time that the command was run
#   finished_at - The date and time that the command finished
#   returned - Any values or objects that the function returned
#   stdout - The stdout of the command
#   stderr - The stderr of the command
# FUNCTIONS
#   to_dict - Format the function and attributes as a Python Dictionary
#   to_json - Format the function and attributes as a JSON
#----------------------------------------------------------------------------------------------------------
class PYTHON:
    def __init__(self, func, *args, **kwargs):
        self.function = func
        self.arguments = args
        self.kw_arguments = kwargs

        self.started_at = datetime.strptime("1970-01-01 00:00:00.0", "%Y-%m-%d %H:%M:%S.%f")
        self.finished_at = datetime.strptime("1970-01-01 00:00:00.0", "%Y-%m-%d %H:%M:%S.%f")
        self.returned = False
        self.stdout = ''
        self.stderr = ''

    def to_dict(self):
        d = {
            "function": self.command,
            "arguments": self.arguments,
            "kw_arguments": self.kw_arguments,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "returned": self.returned,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }
        return d
    
    def to_json(self):
        d = {
            "function": self.function.__name__,
            "arguments": str(self.arguments),
            "kw_arguments": str(self.kw_arguments),
            "started_at": self.started_at.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "finished_at": self.finished_at.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "returned": str(self.returned),
            "stdout": self.stdout,
            "stderr": self.stderr,
        }
        return d
#==========================================================================================================

#==========================================================================================================
# YKI - A Wrapper class used to standardize the storage of a sequence of BASH and PYTHON objects as a file (.yki)
# PARAMETERS
#   yokai_function - And identifier for the Yokai Function that produced the YKI
# ATTRIBUTES
#   commands - A dictionary of the BASH and PYTHON objects executed, with their order of execution as their keys
#               eg. first command -> commands[0], second command -> commands[1], etc.
#   files - Any files that were stored after the execution of the sequence of BASH and PYTHON objects
#               eg. if a command is "echo 'abc' > my_output.txt" and my_output.txt were to be saved, it would be stored
#               in the object under files and then removed from disk, this keeps the files saved with their associated
#               execution sequences
# FUNCTIONS
#   to_file - Serialize the YKI with Pickle and save it to a file
#   from_file - Unserialize the YKI file with pickle for use in python
#   print - Print the content of the YKI to the screen
#
#----------------------------------------------------------------------------------------------------------
class YKI:
    def __init__(self, yokai_function=None, schedule=None):
        self.commands = []
        if yokai_function:
            self.yokai_function = yokai_function
        else:
            self.yokai_function = ''

        if not schedule:
            self.schedule = ExecutionScheduler().to_dict
        if isinstance(schedule, ExecutionScheduler):
            self.schedule = schedule.to_json()

    def to_file(self, file_name):
        pickle.dump(self, open(file_name, 'wb'))

    def from_file(self, file_name):
        self = pickle.load(open(file_name, 'rb'))
        return self
    
    def print(self):
        print("#==================================================")
        print(f"FUNCTION: {self.yokai_function}")
        print("#--------------------------------------------------")
        print(f"SCHEDULE:")
        print(json.dumps(self.schedule, indent=2))
        print("#--------------------------------------------------")
        for c in range(len(self.commands)):
            print(json.dumps(self.commands[c].to_json(), indent=2))
        print("#==================================================")
#==========================================================================================================

class Yokai:
    """
    Yokai is a base class for creating Yokai Functions, which are functions that run a series of commands, save the output,
    start/end time, and files in a neat format. Once a Yokai Function is defined, it can be called just like any other function.
    The `__setup__` method can have as many arguments as you want, and the Yokai Function will return a YKI (Yokai Information)
    object, which can be serialized and saved to a file.

    Subclasses of Yokai must implement the `__commands__` method, which should return a list of commands (BASH or PYTHON)
    to be executed.
    """

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj.scheduler = kwargs.get('scheduler', ExecutionScheduler())  # Get the 'scheduler' argument or set it to None
        obj.log = kwargs.get('log', True)  # Get the 'log' argument or set it to True
        obj.logger = obj.__create_logger__()

        if 'scheduler' in kwargs.keys():
            kwargs.pop('scheduler')
        if 'log' in kwargs.keys():
            kwargs.pop('log')

        r = obj.__execute__(*args, **kwargs)
        return r
    
    def __create_logger__(self):

        logger = logging.getLogger(''.join(random.choice(string.hexdigits[:-6]) for _ in range(32)))

        while(logger.hasHandlers()):
            logger = logging.getLogger(''.join(random.choice(string.hexdigits[:-6]) for _ in range(32)))
        
        if self.log:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.WARNING)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Create console handler and set level to INFO
        console_handler = logging.StreamHandler()
        if self.log:
            console_handler.setLevel(logging.INFO)
        else:
            console_handler.setLevel(logging.WARNING)
        
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def __execute__(self, *args, **kwargs):
        """
        Executes the commands returned by the __commands__ method and captures their outputs.

        Returns:
            YKI: A YKI (Yokai Information) object containing the executed commands and their associated information.
        """
        cmds = self.__commands__(*args, **kwargs)
        r = YKI(self.__class__.__name__, self.scheduler)
        for i, cmd in enumerate(cmds):
            if isinstance(cmd, BASH):
                r.commands.append(self.__run_bash_command__(cmd))
            elif isinstance(cmd, PYTHON):
                r.commands.append(self.__run_python_function__(cmd))
        return r

    def __commands__(self, *args, **kwargs):
        """
        Subclasses must implement this method to return a list of commands (BASH or PYTHON) to be executed.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.

        Returns:
            list: A list of commands to be executed.
        """
        #raise NotImplementedError("Subclasses must implement __commands__ method.")
        return

    def __run_bash_command__(self, cmd):
        """
        Executes a BASH command and captures its output.

        Args:
            cmd (BASH): The BASH object representing the command.

        Returns:
            BASH: The updated BASH object with captured output.
        """

        def set_fd_nonblocking(fd):
            flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        def read_nonblocking(fd, block_size):
            try:
                return os.read(fd.fileno(), block_size)
            except OSError as e:
                if e.errno != errno.EAGAIN:
                    raise
                return b''
        
        self.logger.info(f"BASH command: {cmd.command}")
        if not self.scheduler.can_execute():
            self.logger.info(f"\tWaiting to start at {datetime.now(self.scheduler.timezone)} {self.scheduler.timezone}")
            while not self.scheduler.can_execute():
                sleep(10)
        
        cmd.started_at = datetime.now()
        self.logger.info(f"\tStarted at {cmd.started_at} {self.scheduler.timezone}")

        p = subprocess.Popen(cmd.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        set_fd_nonblocking(p.stdout)
        set_fd_nonblocking(p.stderr)

        # BLOCK_SIZE: Size of read buffer in to memory
        # The larger this is, the faster the command runs
        BLOCK_SIZE = 1048576
        executing = True
        sleep_time = 1 # Used for incremental sleeps to allow long runners better performance

        p.poll()
        while (p.returncode is None):
            if self.scheduler.can_execute() and not executing:
                try:
                    os.kill(p.pid, signal.SIGCONT) # Send the SIGSTOP signal to the process
                    self.logger.info(f"\tContinuted (SIGCONT) at {datetime.now(self.scheduler.timezone)} {self.scheduler.timezone}")
                except:
                    pass
                executing = True
                
            elif not self.scheduler.can_execute() and executing:
                try:
                    os.kill(p.pid, signal.SIGSTOP)
                    self.logger.info(f"\tStopped (SIGSTOP) at {datetime.now(self.scheduler.timezone)} {self.scheduler.timezone}")
                except:
                    pass
                executing = False

            elif executing:
                stdout_data = read_nonblocking(p.stdout, BLOCK_SIZE)
                stderr_data = read_nonblocking(p.stderr, BLOCK_SIZE)

                if stdout_data:
                    cmd.stdout += stdout_data.decode('utf-8')

                if stderr_data:
                    cmd.stderr += stderr_data.decode('utf-8')

            p.poll()

            if executing and p.returncode is None:
                sleep(sleep_time) # Give extra time to send to stdout/stderr for long runners
                if sleep_time < 60:
                    sleep_time += 1
            else:
                sleep(1)
            
        while True:
            stdout_data = read_nonblocking(p.stdout, BLOCK_SIZE)
            stderr_data = read_nonblocking(p.stderr, BLOCK_SIZE)

            if not stdout_data and not stderr_data:
                break

            if stdout_data:
                cmd.stdout += stdout_data.decode('utf-8', 'ignore')

            if stderr_data:
                cmd.stderr += stderr_data.decode('utf-8', 'ignore')


        cmd.finished_at = datetime.now()
        self.logger.info(f"\tFinished at {cmd.finished_at} {self.scheduler.timezone}")
        
        return cmd

    def __run_python_function__(self, func):
        """
        Executes a PYTHON function and captures its output.

        Args:
            func (PYTHON): The PYTHON object representing the function.

        Returns:
            PYTHON: The updated PYTHON object with captured output.
        """
        
        # Wrapper Function that goes around the passed in function
        def proc_function(_func, _q_stdout, _q_stderr, _q_return, _executed_event):
            old_stdout = sys.stdout
            sys.stdout = str_buffer = StringIO()

            try:
                ret = _func.function(*_func.arguments, **_func.kw_arguments)
                err = None
            except Exception as e:
                err = str(e)
                ret = None

            sys.stdout = old_stdout

            _executed_event.set()

            _q_stderr.put(err)
            _q_return.put(ret)
            _q_stdout.put(str_buffer.getvalue())

            return 0

        self.logger.info(f"PYTHON function: {func.function.__name__} ")

        if not self.scheduler.can_execute():
            self.logger.info(f"\tWaiting to start at {datetime.now(self.scheduler.timezone)} {self.scheduler.timezone}")
            while not self.scheduler.can_execute():
                sleep(10)

        func.started_at = datetime.now(self.scheduler.timezone)
        self.logger.info(f"\tStarted at {func.started_at} {self.scheduler.timezone}")

        with Manager() as manager:
            q_stdout = manager.Queue()
            q_stderr = manager.Queue()
            q_return = manager.Queue()
            
            executed_event = manager.Event() 
            # The executed_event acts as a watch dog to prevent deadlocks on
            # the managed queues. Theoretically, there should not be any
            # deadlocks, but rare and unexplained deadlocks have occured with
            # unmanaged queues. The executed_event signifies that the main
            # purpose (the passed in python function) has finished and that
            # the only thing left to do is to transfer outputs to the queues
            # (one of the suspected areas where mystery deadlocks occured).
            # After the func is executed, there is a 5 second gap to transfer
            # the outputs to the queues before the run python_function exits.
            # The other suspected spot of deadlock was the func itself. Originally
            # the func was not passed in as an arg to proc_function, which could have
            # caused a rare race condition to deadlock.
            # Either way, in one situation where deadlock was consistantly occuring,
            # the changes seem to have resolved it.
            # In the event that the proc_function does not exit fully, and the
            # __run_python_function__ exits prematurly, making the child process
            # daemonic will cause it to also terminate when the main python process has
            # terminated. Probably wont be an issue, even on long running yokai, but
            # is something to make a note of.

            # Create a new process
            p = Process(target=proc_function, args=(func, q_stdout, q_stderr, q_return, executed_event), daemon=True)
            p.start() # Start the process

            executing = True
            while p.is_alive() and not executed_event.is_set():
                if self.scheduler.can_execute() and not executing:
                    os.kill(p.pid, signal.SIGCONT) # Send the SIGCONT signal to the process
                    executing = True
                    self.logger.info(f"\tContinuted (SIGCONT) at {datetime.now(self.scheduler.timezone)} {self.scheduler.timezone}")
                elif not self.scheduler.can_execute() and executing:
                    os.kill(p.pid, signal.SIGSTOP)
                    executing = False
                    self.logger.info(f"\tStopped (SIGSTOP) at {datetime.now(self.scheduler.timezone)} {self.scheduler.timezone}")
                sleep(1)

            sleep(5)
            while not q_stdout.empty():
                func.stdout = q_stdout.get()
            while not q_stderr.empty():
                func.stderr = q_stderr.get()
            while not q_return.empty():
                func.returned = q_return.get()

            p.join() # Wait for the process to complete

        func.finished_at = datetime.now(self.scheduler.timezone)
        self.logger.info(f"\tFinished at {func.finished_at} {self.scheduler.timezone}")

        return func