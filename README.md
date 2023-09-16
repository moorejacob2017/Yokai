```
                                __   ___          __       _     ___   ___ 
                         \\    / / //   ) ) //   / /   // | |       / /    
                          \\  / / //   / / //__ / /   //__| |      / /     
                           \\/ / //   / / //__  /    / ___  |     / /      
                            / / //   / / //   \ \   //    | |    / /       
                           / / ((___/ / //     \ \ //     | | __/ /___  
  
    @ /@                                                                               @. @ 
   ,@   @@                                                                           @@   @ 
   ,@     @(                               @@@%%%@@&                               &@     @ 
    @      ,@                           @@           @@                          *@       @ 
    @         @&                     #@                .@,                     @@         @ 
    @            @@@&&&@@@@&/      (@*&@%             &@&.@.      #&@@@@&&&@@@            & 
    %@        ..*@@@@@@@@@@@,  *@@@@@@/   @*       &@   #@@@@@@   *@@@@@@@@@@@*..        @, 
     @@    ,*                  @&          @@     @%          @&                  *.     @  
     &@.@@                      @/ @@@@&%%@ @,   #@ &@@%@@@& &@                      @@ @/  
      @@(       @(@@@@@@&@@@&&&@@@@@@%     *&@   @&*    %@@@@@@@&&&@@@&@@@@@@/@@      @@@   
       @     #@*    &@%  ,@@ @.       *.@.  @.   .@  ..*        #@ @@.  @     @(@.    *@    
       @    @@ @       /@ @@&@,@          @@       @@         *@    & @.     @   @%   /@    
       @@   @  *@     (@*   &@@@           @@     @%          @@@    &@*  (@%    @   @/    
        @  .@   &&    *@      %@@.           @@@@%          @@@        @   @      @   @     
        &@  @    .@   @   @.   @@@@@@@@@@.@@@@@@#@@@@/@@@@@@@@@@ @   @@ .@@     .(@ @,     
         @# /@   @ @@@ , @  @  @    @    @     @     @    @    @@ @  *.%   @@ &&   @@      
          @# @%@&@     @ @   @ @    @    @     @     @    @   .@  @  @&     @@    @@       
           @@  .@    ./@  @   *%@@@.@@@@@@@@&@@@@&&@@@&@@@@.%*@   @ % @@,    @   @@%        
            #@ @   @@    @.@       (@    @     @     @    @.@     @%@&   @.   @ @@*         
              @  /@   @,   @&@,     @    @     @     @    @@    #@@@   #@  @   @&           
             @%@*           @* (&##@@#@@@@@@%%@%%@@@@@@/@@,#%( %@    @      *. &           
            @&  @/            %@@@@.                     ,@@@@/    @#     &@*  *@             
                  *@*        *      %@@    *@@@@@,    @@/      #@@      &@                 
                      @%                                               @@                   
                        @@                                           @@                     
                          *@/   @@@,                       (@@&   %@                        
                             &@.     &@@@@/        ./@@@@%     *@(                          
                                #@%                         @@*                             
                                    @@@.   *@@@@@@&,   *@@%                                 


```
#### **This project is licensed under the [GNU General Public License v3.0](LICENSE.txt) - see the [LICENSE](LICENSE.txt) file for details.**




Yokai is a light-weight Python module used to daemonize and automate your common tasks. It was made with the intent of being relatively simple and provides a solution for running repetitive tasks, enabling you to streamline your workflow and focus on more critical aspects of your projects. With Yokai, you can easily schedule and execute BASH commands or Python functions at specific times, on particular days, or during special periods. It simplifies the process of defining rules and conditions for task execution, giving you full control over when and how your tasks run.

The concept revolves around the creation of "yokai functions". Yokai functions are a class of functions used that automate a series of commands and functions. Think of them as special wrappers that turn a sequence of commands into a daemon.

At the heart of Yokai's innovation is the integration of a preprocessor, which is packaged with the module and accessible via the command line interface (CLI) using the `yokai` command. This preprocessor is pivotal in translating the extended Yokai syntax found in Python files into executable Python code, thus enabling the unique functionalities that Yokai offers.

Leveraging the preprocessor, Yokai introduces three pivotal keywords to the Python syntax — `yokai`, `bash`, and `python`, each serving to facilitate different aspects of task automation.


## Table of Contents
- [How It Works](#how-it-works)
- [How to Install](#how-to-install)
- [Usage](#usage)
- [`yokai` Keyword](#yokai-keyword)
- [`bash` Keyword](#bash-keyword)
- [`python` Keyword](#python-keyword)
- [Simple `Yokai` Usage Example](#simple-yokai-usage-example)
- [`ExecutionScheduler` Usage Example](executionScheduler-usage-example)
- [General `Yokai` Usage Example with `nmap`, `xsltproc`, and `searchsploit`](#general-yokai-usage-example-with-nmap-xsltproc-and-searchsploit)
- [Advanced `Yokai` Usage Example for HTB Recon](#advanced-yokai-usage-example-for-htb-recon)
- Other
  - [`class BASH`](docs/bash.md)
  - [`class PYTHON`](docs/python.md)
  - [`class YKI`](docs/yki.md)

## How It Works

- **`yokai` Keyword**: The yokai keyword is utilized to simplify the definition of Yokai functions in Python, serving a role analogous to the `def` keyword used in standard function definitions. It is designed to streamline the creation of Yokai functions, facilitating a more straightforward syntax.

- **`bash` and `python` Keywords**: The bash and python keywords work alongside the `yokai` keyword to aid in defining Yokai managed Bash commands and Python functions, respectively. These keywords are implemented to offer a simpler, more efficient way to define functions and commands in a Yokai environment, promoting cleaner and more readable code.

- **YKI (Yokai Information) Class**: Utilize the `YKI` class to standardize the storage of executed commands and functions. Serialize YKI objects, save them to files, and effortlessly retrieve execution information for analysis and auditing purposes. Track start and finish times, stdout, stderr, and returned values for each executed task.

- **ExecutionScheduler Class**: Yokai's `ExecutionScheduler` class empowers you to create sophisticated task execution schedules. Define rules for daily, weekly, or special date-based execution periods, and even specify periods with unlimited execution or no execution at all. If a command/function is already running when time changes to a no execution time, the `ExecutionScheduler` has the `Yokai` send a `SIGSTOP` to the process, halting the execution flow. When time switches back to allowed execution, the Yokai will send a `SIGCONT` to let the process continue where it left off.

__A Note on Security__:
Because the YKI is deserialized with Pickle, there is **INSECURE DESERIALIZATION**. Do not load YKI you do not trust. Also, if you are passing arguments into you're Yokai Function and aren't providing input validation, you **WILL** end up with **OS COMMAND INJECTIONS**. This script is what you make of it and acts more as an extension of the capabilities of python. But this is not something that you should be using to prop up a prod server or just let loose to run for months at a time unchecked. You can do a lot with Yokai, but use it safely and responsibly.

To quote the Python mindset, "We are all consenting adults here."

## How to Install
Download the latest WHL file from the releases page and install it with `pip`. It's that easy!

<!-- Build CMD: python setup.py bdist_wheel -->

## Usage

Yokai introduces three new keywords into the Python language: `yokai`, `bash`, and `python`. These keywords are designed to facilitate a more streamlined interaction between Python and Bash commands while promoting a cleaner and more efficient way to define and track Python function executions. 

Import the `yokai` module and use the built-in `yokai` preprocessor CLI utility to execute any file that contains yokai syntax, like so: `yokai my_yokai_file.py`. Be mindful that the `yokai` CLI utility will be installed in the users `/home/<user>/.local/bin` folder by default. If said directory is not already included in the user's `PATH` environment variable, the CLI utility will not be found.

Below, we delve into the specifics and usage of each keyword, illustrating their functionalities through examples.

___

### `yokai` Keyword

The `yokai` keyword functions similarly to the `def` keyword, which is traditionally used to define Python functions. However, the `yokai` keyword is used to define a special kind of function known as a yokai function. When defining a yokai function, it is imperative know that one cannot return objects directly from the yokai function. Instead, yokai function are more procedural in nature and will return a YKI object when execution is finished. If it is desired for a yokai function to finish execution prematurely, a `return` statement may be used to exit the yokai function. Please remember that any objects following the return statement will be ignored in favor of the YKI that describes the yokai execution.

#### Syntax
```python
yokai function_name(arguments):
    # Function body
    ...
```

#### Example
```python
import yokai
yokai function_name(name):
    print(f"Hello, {name}")
```

___

### `bash` Keyword

Exclusive to yokai functions, the `bash` keyword permits the execution of Bash commands within a yokai function. This keyword follows a specific syntax where it precedes a colon and a string containing the bash command to be executed. It is important to note that the `bash` keyword is case-sensitive and allows only a single bash command per keyword instance.

#### Syntax
```python
bash: "bash_command_as_string"
```

#### Example
```python
import yokai
yokai function_name(name):
    bash: f"echo Hello, {name}"
    bash: "echo This is a bash command"
```

___

### `python` Keyword

Also exclusive to yokai functions, the `python` keyword enables the execution of Python functions within a yokai function. The `python` keyword acts somewhat like the `bash` keyword in that it proceeds a colon, but instead of a string, it is followed by a Python function call. This keyword supports assignment, allowing the user to assign the return value of the function to a variable. The `python` keyword is case-sensitive and permits only a single Python function call per keyword instance. Note that while any Python function can be called within a yokai function without utilizing the `python` keyword, such functions will be executed in the main process and their executions will not be tracked by the yokai function.

#### Syntax
```python
python: python_function_call
```

#### Example
```python
import yokai
yokai function_name(name):
    python: print(f'Hello, {name}')
    python: print("This is a python function")
```

#### Exampe w/ Assignment
```python
import yokai

def my_func(x):
    return x * x

yokai function_name():
    num = 4
    python: result = my_func(num)
    print(result) # This print is executed, but not tracked by yokai
    # Prints 16 to screen
```

___


## Usage Cases and Examples

### Simple `Yokai` Usage Example
```python
import yokai

# Create a Yokai Function
yokai my_yokai_function():
    bash: "echo 'Hello, Yokai Function!'"
    python: print("Hello, Python Function", end='!\n')

# Yokai Functions return YKI, which can be serialized with `.to_file()` and deserialized with `.from_file()`
yki_results = my_yokai_function()

# Print the YKI to the console
yki_results.print()
```

__Note__: Logging is turned on by default so that yokai can be used with tools like `tee` and `nohup`. Pass the the kwarg `log=False` on the call to turn it off, eg. `my_yokai_function(log=False)`

#### Output
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

___

### `ExecutionScheduler` Usage Example
```python
import yokai

my_scheduler = yokai.ExecutionScheduler(
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
yokai my_yokai_function():
    bash: "echo 'Hello, Yokai Function!'"
    python: print("Hello, Python Function", end='!\n')

# Give the yokai function the ExecutionScheduler on the function call
# If no scheduler is given, then execute at any time
yki_results = my_yokai_function(scheduler=my_scheduler)

yki_results.print()
```

___

### General `Yokai` Usage Example with `nmap`, `xsltproc`, and `searchsploit`
```python
import yokai
import os

# Custom nmap yokai that can be easily imported and reused
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

yokai nmap_yokia(target, basename, outputdir):
    if not os.path.exists(outputdir): # Make outputdir if it does not already exist
        os.makedirs(outputdir, exist_ok=True)

    bash: f"nmap -Pn -sS -p- --open -vvv -d -T3 --min-rate 500 -oA {outputdir}/{basename}_nmap_tcp_all {target}"
    bash: f"nmap -Pn -sU --top-ports 1000 -vvv -d --reason --max-retries 2 -T3 --min-rate 500 -oA {outputdir}/{basename}_nmap_udp_1000 {target}"
    bash: f"nmap -Pn -vvv -d --reason -O -sV --version-all -T4 --min-rate 1000 -oA {outputdir}/{basename}_versioning {target}"
    bash: f"nmap -Pn -vvv -d --reason -O -sV --script=banner -T4 --min-rate 1000 -oA {outputdir}/{basename}_banners {target}"
    bash: f"xsltproc {outputdir}/{basename}_nmap_tcp_all.xml -o {outputdir}/{basename}_nmap_tcp_all.html"
    bash: f"xsltproc {outputdir}/{basename}_nmap_udp_100.xml -o {outputdir}/{basename}_nmap_udp_1000.html"
    bash: f"xsltproc {outputdir}/{basename}_versioning.xml -o {outputdir}/{basename}_versioning.html"
    bash: f"xsltproc {outputdir}/{basename}_banners.xml -o {outputdir}/{basename}_banners.html"
    bash: f"searchsploit -u"
    bash: f"searchsploit --nmap {outputdir}/{basename}_versioning.xml > {outputdir}/{basename}_v_searchsploit.txt"
    bash: f"searchsploit --nmap {outputdir}/{basename}_banners.xml > {outputdir}/{basename}_b_searchsploit.txt"


# If you'd like to put a yokai function in a seperate file, you can
# import it like so...
# from my_nmap_yokai import *

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

___

### Advanced `Yokai` Usage Example for HTB Recon
This is a complex Yokai example that is great for kicking of a box on Hack the Box and automates some basic recon.
__WORDLISTS NOT INCLUDED!__
```python
#============================================================================
# Imports 
import yokai

import os
import re
import requests
import urllib3

requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#============================================================================
# Utility Functions

# General utility functions to keep the Yokai clean
# Don't worry too much about these, feel free to skip
# They are here for completeness

#----------------------------------------------------------------------------
# Parses an Nmap file to get the TCP Ports
def parse_nmap_tcp_ports(nmap_prefix):
    with open(f"{nmap_prefix}.nmap") as file:
        nmap_output = file.read()
    tcp_ports = []
    tcp_re = re.compile(r'^([0-9]+)\/tcp\s+(open|filtered)\s+.*$', re.MULTILINE) # Regular expressions to match discovered ports
    tcp_match = tcp_re.findall(nmap_output) # Search for discovered TCP ports
    if tcp_match:
        tcp_ports = [int(p[0]) for p in tcp_match]
    all_ports = [f"T:{p}" for p in list(set(tcp_ports))]
    return all_ports
#----------------------------------------------------------------------------
# Parses an Nmap file to get the UDP Ports
def parse_nmap_udp_ports(nmap_prefix):
    with open(f"{nmap_prefix}.nmap") as file:
        nmap_output = file.read()
    udp_ports = []
    udp_re = re.compile(r'^([0-9]+)\/udp\s+(open)\s+.*$', re.MULTILINE) # Regular expressions to match discovered ports
    udp_match = udp_re.findall(nmap_output) # Search for discovered UDP ports
    if udp_match:
        udp_ports = [int(p[0]) for p in udp_match]
    all_ports = [f"U:{p}" for p in list(set(udp_ports))]
    return all_ports
#----------------------------------------------------------------------------
# Parses an Nmap file to get the Live Hosts
def parse_nmap_live(nmap_prefix):
    file_path = f"{nmap_prefix}.nmap"
    live_ips = []
    with open(file_path, 'r') as nmap_file:
        lines = nmap_file.readlines()
    for line in lines:
        if "Nmap scan report for" in line:
            ip_address = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', line)
            if ip_address:
                live_ips.append(ip_address[0])
    unique_live_ips = list(set(live_ips))
    return unique_live_ips
#----------------------------------------------------------------------------
# Check a specific port to see if it uses HTTP/S
def check_ports_for_http(target, live_ports):
    # Takes nmap ports strings ("T:80,T:443")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    ports = [x[2:] for x in live_ports.split(',')]
    alive = []
    for port in ports:
        http_url = f"http://{target}:{port}/"
        https_url = f"https://{target}:{port}/"
        try:
            response = requests.get(http_url, headers=headers, verify=False, timeout=10)
            alive.append(http_url)
        except Exception as e:
            pass
        try:
            response = requests.get(https_url, headers=headers, verify=False, timeout=10)
            alive.append(https_url)
        except Exception as e:
            pass
    return alive

#============================================================================
# COMMANDS (Run as root!):
# 1.  nmap TCP all ports
# 2.  convert nmap TCP xml to clean html
# 3.  nmap UDP top 1000 ports
# 4.  convert nmap UDP xml to clean html
# 5.  Parse TCP results to get specific ports
# 6.  Parse UDP results to get specific ports
# 7.  Get live hosts from TCP results
# 8.  Get live hosts from UDP results
# 9.  nmap versioning open ports
# 10. Convert nmap versioning xml to clean html
# 11. nmap banners open ports
# 12. Convert nmap banner xml to clean html
# 13. nmap nse open ports
# 14. convert nmap banner xml to clean html
# 15. Send nmap versioning results through searchsploit and redirect to txt
# 16. Send nmap banner results through searchsploit and redirect to txt
# 17. Send nmap nse results through searchsploit and redirect to txt
# 18. Check for any ports that support HTTP/S
# 19. Run whatweb against live urls
# 20. Run vhost enum against live urls
# 21. Run dirbust with 3 different wordlists and ffuf against live urls
# 22. Parse out the ffuf json to csv


# Definition of the yokai function that takes three arguments: target IP or hostname, base name for the output files, and output directory path
yokai HTB_Recon_yokai(target, basename, outputdir):
    WORDLIST_DIR = '/opt/wordlists'
    
    # Check if the output directory exists; if not, it creates it
    if not os.path.exists(outputdir):
        os.makedirs(outputdir, exist_ok=True)

    # TCP scan with nmap to find open ports and save the output in various formats including XML and HTML
    bash: f"nmap -Pn -sS -p- --open -vvv -d -T4 --min-rate 1000 -oA {outputdir}/{basename}_nmap_tcp_all {target}"
    bash: f"xsltproc {outputdir}/{basename}_nmap_tcp_all.xml -o {outputdir}/{basename}_nmap_tcp_all.html"

    # Similar to the above but for UDP scan targeting top 1000 UDP ports
    bash: f"nmap -Pn -sU --top-ports 1000 -vvv -d --reason --max-retries 2 -T4 --min-rate 1000 -oA {outputdir}/{basename}_nmap_udp_1000 {target}"
    bash: f"xsltproc {outputdir}/{basename}_nmap_udp_1000.xml -o {outputdir}/{basename}_nmap_udp_1000.html"

    # Calling Python functions to parse TCP and UDP ports from the nmap output
    python: tcp_ports = parse_nmap_tcp_ports(f"{outputdir}/{basename}_nmap_tcp_all")
    python: udp_ports = parse_nmap_udp_ports(f"{outputdir}/{basename}_nmap_udp_1000")

    # Getting the list of live hosts from TCP and UDP scan results
    python: tcp_live = parse_nmap_live(f"{outputdir}/{basename}_nmap_tcp_all")
    python: udp_live = parse_nmap_live(f"{outputdir}/{basename}_nmap_udp_1000")
    
    # Combining the results of live hosts and open ports from both TCP and UDP scans to avoid duplicates
    live_hosts_arr = list(set(tcp_live + udp_live))
    live_ports_arr = tcp_ports + udp_ports

    # If there are no live hosts, the function returns and stops further execution
    if live_hosts_arr == []:
        return r # Edit here

    # Creating a string of live hosts and ports to be used in subsequent nmap scans
    live_hosts = ' '.join(live_hosts_arr)
    live_ports = ','.join(live_ports_arr)

    # Performing more detailed nmap scans using the previously found live hosts and open ports
    # The following commands perform version scanning, banner grabbing, and running various NSE scripts on the targets
    bash: f"nmap -Pn -sS -sU -vvv -d --reason -O -sV --version-all -T4 --min-rate 1000 -p {live_ports} -oA {outputdir}/{basename}_versioning {live_hosts}"
    bash: f"xsltproc {outputdir}/{basename}_versioning.xml -o {outputdir}/{basename}_versioning.html"
    bash: f"nmap -Pn -sS -sU -vvv -d --reason -O -sV --script=banner -T4 --min-rate 1000 -p {live_ports} -oA {outputdir}/{basename}_banners {live_hosts}"
    bash: f"xsltproc {outputdir}/{basename}_banners.xml -o {outputdir}/{basename}_banners.html"

    # Run an overly complex Nmap NSE scan that you definitely don't want to type twice
    bash: f"nmap --traceroute -sV -O --script \"all and not (dos or external or ssh-brute or broadcast or http-enum or http-wordpress-* or dns-* or ssl-* or http-vhosts or http-iis-short-name-brute or http-slowloris-check or http-phpmyadmin-dir-traversal)\" --script-args http.useragent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' -Pn -sS -sU -p {live_ports} -T4 --randomize-hosts --min-rate 1000 --max-retries 2 -vvv --open --reason -d --script-timeout 1m -oA {outputdir}/{basename}_nmap_nse {live_hosts}"
    bash: f"xsltproc {outputdir}/{basename}_nmap_nse.xml -o {outputdir}/{basename}_nmap_nse.html"

    # Using searchsploit to find potential vulnerabilities based on the nmap scan results
    bash: f"searchsploit --nmap {outputdir}/{basename}_versioning.xml > {outputdir}/{basename}_versioning_searchsploit.txt"
    bash: f"searchsploit --nmap {outputdir}/{basename}_banners.xml > {outputdir}/{basename}_banners_searchsploit.txt"
    bash: f"searchsploit --nmap {outputdir}/{basename}_nmap_nse.xml > {outputdir}/{basename}_nmap_nse_searchsploit.txt"

    # Checking which ports support HTTP/HTTPS and storing the URLs
    python: urls = check_ports_for_http(target, live_ports)

    if urls == []:
        return r

    # Running a series of further reconnaissance tasks on the URLs found to support HTTP/HTTPS
    # These include running whatweb for web application fingerprinting, gobuster for virtual host enumeration, and ffuf for directory/file brute-forcing
    # ... (the following lines loop over each URL and run the aforementioned tools, saving the results in various formats)
    for i in range(len(urls)):
        port = urls[i].split(':')[-1][:-1]
        bash: f"whatweb -v -a 3 --user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' --log-verbose={outputdir}/{basename}_whatweb_{port}.txt --log-json={outputdir}/{basename}_whatweb_{port}.json {urls[i]}"
    
    for i in range(len(urls)):
        port = urls[i].split(':')[-1][:-1]
        postfix = f"_vhost_enum_{port}"
        bash: f"gobuster vhost -w {WORDLIST_DIR}/wordlists/combined_subdomains.txt -u {urls[i]} --append-domain -r -k --useragent 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' -t 40 -o {outputdir}/{basename}{postfix}.log"
    
    for i in range(len(urls)):
        port = urls[i].split(':')[-1][:-1]
        postfix = f"_cd_{port}"

        bash: f"ffuf -w {WORDLIST_DIR}/wordlists/combined_dir.txt -u {urls[i][:-1]}FUZZ -mc 200,204,301,302,307,401,403,405,500 -r -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' -t 40 -of json -o {outputdir}/{basename}{postfix}.json -debug-log {outputdir}/{basename}{postfix}_debug.log"
        bash: f"jq -r '.results[] | [.url, .status] | @csv' {outputdir}/{basename}{postfix}.json > {outputdir}/{basename}{postfix}.csv"
    
    for i in range(len(urls)):
        port = urls[i].split(':')[-1][:-1]
        postfix = f"_common_{port}"
        bash: f"ffuf -w {WORDLIST_DIR}/wordlists/common.txt -u {urls[i][:-1]}/FUZZ -mc 200,204,301,302,307,401,403,405,500 -r -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' -t 40 -of json -o {outputdir}/{basename}{postfix}.json -debug-log {outputdir}/{basename}{postfix}_debug.log"
        bash: f"jq -r '.results[] | [.url, .status] | @csv' {outputdir}/{basename}{postfix}.json > {outputdir}/{basename}{postfix}.csv"
    
    for i in range(len(urls)):
        port = urls[i].split(':')[-1][:-1]
        postfix = f"_dlm_{port}"
        bash: f"ffuf -w {WORDLIST_DIR}/wordlists/directory-list-2.3-medium.txt -u {urls[i][:-1]}/FUZZ -mc 200,204,301,302,307,401,403,405,500 -r -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' -t 40 -of json -o {outputdir}/{basename}{postfix}.json -debug-log {outputdir}/{basename}{postfix}_debug.log"
        bash: f"jq -r '.results[] | [.url, .status] | @csv' {outputdir}/{basename}{postfix}.json > {outputdir}/{basename}{postfix}.csv"

#============================================================================

```

