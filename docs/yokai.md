# `class Yokai`

```python
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
```