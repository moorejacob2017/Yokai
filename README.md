# YOKAI

Yokai is a light-weight script used to daemonize and automate your common tasks. It was made with the intent of being "brain-dead simple" and provides a solution for running repetitive tasks, enabling you to streamline your workflow and focus on more critical aspects of your projects. With Yokai, you can easily schedule and execute BASH commands or Python functions at specific times, on particular days, or during special periods. It simplifies the process of defining rules and conditions for task execution, giving you full control over when and how your tasks run.

The extent of Yokai's usage is only limited to the tools you use and the commands you give it. So feel free to get creative with it!

## How It Works

The concept revolves around the creation of "Yokai Functions". Yokai Functions are a class of functions used that automate a series of commands/functions. Think of them as special wrappers that turn a playlist of commands into a daemon.

## Key Features

- **Yokai Base Class**: `Yokai` simplifies the creation of Yokai Functions. Subclass the base class and implement the `__commands__` method to define the tasks you want to execute. Yokai takes care of the rest, including task execution and capturing command outputs. You can also define the `__setup__` and `__clean__` methods to customize pre and post execution instructions.
- **YKI (Yokai Information) Class**: Utilize the `YKI` class to standardize the storage of executed commands and functions. Serialize YKI objects, save them to files, and effortlessly retrieve execution information for analysis and auditing purposes.
- **BASH and PYTHON Wrappers**: Capture crucial information during command and function execution with Yokai's wrappers. Track start and finish times, stdout, stderr, and returned values for each executed task.
- **ExecutionScheduler**: Yokai's `ExecutionScheduler` class empowers you to create sophisticated task execution schedules. Define rules for daily, weekly, or special date-based execution periods, and even specify periods with unlimited execution or no execution at all. If a command/function is already running when time changes to a no execution time, the `ExecutionScheduler` has the `Yokai` send a `SIGSTOP` to the process, halting the execution flow. When time switches back to allowed execution, the Yokai will send a `SIGCONT` to let the process continue where it left off.

## How to Use
To keep it as simple and light-weight as possible, just save the `yokai.py` to your working directory and import it into any python file you want to make a yokai in. That's it!

## Simple `Yokai` Usage Example
### Usage
```python
from yokai import *

# Create a Yokai Function
class my_yokai_function(Yokai):
    def __commands__(self): # Define the commands/functions to run in this method
        return [
            BASH("echo 'Hello, Yokai Function!'"), # Wrap BASH commands with the BASH wrapper
            PYTHON(print, "Hello, Python Function", end='!\n') # Wrap Python funcs with the PYTHON wrapper
        ] # Return the commands/functions as an array

# While it is technically a Class object, use Yokai Functions just like a normal Python Function
# Yokai Functions return YKI, which can be serialized with `.to_file()` and deserialized with `.from_file()`
yki_results = my_yokai_function()

# Print the YKI to the console
yki_results.print()

# Note: Logging is turned on by default so that
#   it can be used with tools like `tee` and `nohup`
#   Pass the the kwarg `log=False` on the call
#   to turn it off, eg. `my_yokai_function(log=False)`
```

### Output
```
2023-07-21 03:53:31,056 - INFO - BASH command: echo 'Hello, Yokai Function!'
2023-07-21 03:53:31,056 - INFO -        Started at 2023-07-21 03:53:31.056499 UTC
2023-07-21 03:53:31,059 - INFO -        Finished at 2023-07-21 03:53:31.059251 UTC
2023-07-21 03:53:31,059 - INFO - PYTHON function: print 
2023-07-21 03:53:31,059 - INFO -        Started at 2023-07-21 08:53:31.059525+00:00 UTC
2023-07-21 03:53:32,066 - INFO -        Finished at 2023-07-21 08:53:32.066011+00:00 UTC
#==================================================
FUNCTION: my_yokai_function
#--------------------------------------------------
SCHEDULE:
{
  "start_time": "00:00:00",
  "end_time": "00:00:00",
  "allowed_days": "",
  "unlimited_days": "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday",
  "halt_days": "",
  "special_days": [],
  "timezone": "UTC"
}
#--------------------------------------------------
{
  "command": "echo 'Hello, Yokai Function!'",
  "started_at": "2023-07-21 03:53:31.056499",
  "finished_at": "2023-07-21 03:53:31.059251",
  "stdout": "Hello, Yokai Function!\n",
  "stderr": ""
}
{
  "function": "print",
  "arguments": "('Hello, Python Function',)",
  "kw_arguments": "{'end': '!\\n'}",
  "started_at": "2023-07-21 08:53:31.059525",
  "finished_at": "2023-07-21 08:53:32.066011",
  "returned": "None",
  "stdout": "Hello, Python Function!\n",
  "stderr": ""
}
#==================================================
```

## `ExecutionScheduler` Usage Example
### Usage
```python
from yokai import *

my_scheduler = ExecutionScheduler(
    start_time=time(6, 0), # Allow execution between 6:00am...
    end_time=time(17, 30), # ...and 5:30pm (Can also use the reversed, eg. start at 17:30 and end at 6:00 for execution on the off-hours)
    timezone='US/Central', # pytz CST Timezone (Default is UTC)
    allowed_days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], # Allow execution with time constraintes on weekdays
    unlimited_days=['Saturday'], # Allow execution without time constraints on Saturdays
    halt_days=['Sunday'], # Do not allow any execution on Sundays
    special_days=[
        {   # Do not allow any execution on December 24, 25, or 26, 2023
            'start': '2023-12-24', 
            'end': '2023-12-26', 
            'mode': 'halt'
        },
        {   # Allow execution without time constraints on January 01, 2024
            'start': '2024-01-01', 
            'end': '2024-01-01', 
            'mode': 'unlimited'
        }
    ]
)

# An example Yokai Function
class my_yokai_function(Yokai):
    def __commands__(self):
        return [
            BASH("echo 'Hello, Yokai Function!'"),
            PYTHON(print, "Hello, Python Function", end='!\n')
        ]

# Give the yokai function the ExecutionScheduler on the function call
# If no scheduler is given, then execute at any time
yki_results = my_yokai_function(scheduler=my_scheduler)

yki_results.print()
```

## Advanced `Yokai` Usage Case with `nmap`, `xsltproc`, and `searchsploit`
### my_nmap_yokai.py
```python
from yokai import *
import os

# Custom nmap yokai that can be easily imported and reused
class nmap_yokia(Yokai):
    def __setup__(self, target, basename='yokai', outputdir=f"{YOKAI_DIR}/output"):
        if not os.path.exists(outputdir): # Make outputdir if it does not already exist
            os.makedirs(outputdir, exist_ok=True)

    def __commands__(self, target, basename='yokai', outputdir=f"{YOKAI_DIR}/output"):
        # COMMANDS (Run as root!):
        # 1.  nmap TCP all ports
        # 2.  nmap UDP top 1000 ports
        # 3.  nmap versioning all ports
        # 4.  nmap banners all ports
        # 5.  convert nmap TCP xml to clean html
        # 6.  convert nmap UDP xml to clean html
        # 7.  convert nmap versioning xml to clean html
        # 8.  convert nmap banner xml to clean html
        # 9.  Update searchsploit
        # 10. Send nmap versioning results through searchsploit and redirect to txt
        # 11. Send nmap banner results through searchsploit and redirect to txt
        return [
            BASH(f"nmap -Pn -sS -p- --open -vvv -d -T3 --min-rate 500 -oA {outputdir}/{basename}_nmap_tcp_all {target}"),
            BASH(f"nmap -Pn -sU --top-ports 1000 -vvv -d --reason --max-retries 2 -T3 --min-rate 500 -oA {outputdir}/{basename}_nmap_udp_100 {target}"),
            BASH(f"nmap -Pn -vvv -d --reason -O -sV --version-all -T4 --min-rate 1000 -oA {outputdir}/{basename}_versioning {target}"),
            BASH(f"nmap -Pn -vvv -d --reason -O -sV --script=banner -T4 --min-rate 1000 -oA {outputdir}/{basename}_banners {target}"),
            BASH(f"xsltproc {outputdir}/{basename}_nmap_tcp_all.xml -o {outputdir}/{basename}_nmap_tcp_all.html"),
            BASH(f"xsltproc {outputdir}/{basename}_nmap_udp_100.xml -o {outputdir}/{basename}_nmap_udp_1000.html"),
            BASH(f"xsltproc {outputdir}/{basename}_versioning.xml -o {outputdir}/{basename}_versioning.html"),
            BASH(f"xsltproc {outputdir}/{basename}_banners.xml -o {outputdir}/{basename}_banners.html"),
            BASH(f"searchsploit -u"),
            BASH(f"searchsploit --nmap {outputdir}/{basename}_versioning.xml > {outputdir}/{basename}_v_searchsploit.txt"),
            BASH(f"searchsploit --nmap {outputdir}/{basename}_banners.xml > {outputdir}/{basename}_b_searchsploit.txt"),
        ]
```
### main.py
```python
from my_nmap_yokai import * # Import the custom nmap yokai

if __name__ == "__main__":
    # Call the custom nmap yokai with a target, base file name, and an output directory
    # Define scheduler if desired
    nmap_yokai_results = nmap_yokia(
        target='metasploitable.ms2',
        basename='ms2_scan',
        outputdir='./ms2_scan_dir',
        # Add scheduler here if desired
    )
    # Save the returned YKI to file for auditing purposes
    nmap_yokai_results.to_file('./ms2_scan_dir/ms2_scan.yki')

```



# 
