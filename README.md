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




Yokai is a light-weight script used to daemonize and automate your common tasks. It was made with the intent of being relatively simple and provides a solution for running repetitive tasks, enabling you to streamline your workflow and focus on more critical aspects of your projects. With Yokai, you can easily schedule and execute BASH commands or Python functions at specific times, on particular days, or during special periods. It simplifies the process of defining rules and conditions for task execution, giving you full control over when and how your tasks run.

The extent of Yokai's usage is only limited to the tools you use and the commands you give it. So feel free to get creative with it!

## How It Works

The concept revolves around the creation of "Yokai Functions". Yokai Functions are a class of functions used that automate a series of commands/functions. Think of them as special wrappers that turn a playlist of commands into a daemon.

## Key Features

- **Yokai Base Class**: `Yokai` simplifies the creation of Yokai Functions. Subclass the base class and implement the `__commands__` method to define the tasks you want to execute. Yokai takes care of the rest, including task execution and capturing command outputs. You can also define the `__execute__` method for fine-tuned execution control, or the `__setup__` and `__clean__` methods to customize pre and post execution instructions.
- **YKI (Yokai Information) Class**: Utilize the `YKI` class to standardize the storage of executed commands and functions. Serialize YKI objects, save them to files, and effortlessly retrieve execution information for analysis and auditing purposes.
- **BASH and PYTHON Wrappers**: Capture crucial information during command and function execution with Yokai's wrappers. Track start and finish times, stdout, stderr, and returned values for each executed task.
- **ExecutionScheduler**: Yokai's `ExecutionScheduler` class empowers you to create sophisticated task execution schedules. Define rules for daily, weekly, or special date-based execution periods, and even specify periods with unlimited execution or no execution at all. If a command/function is already running when time changes to a no execution time, the `ExecutionScheduler` has the `Yokai` send a `SIGSTOP` to the process, halting the execution flow. When time switches back to allowed execution, the Yokai will send a `SIGCONT` to let the process continue where it left off.

### WARNING: A Note on Security
Because the YKI is deserialized with Pickle, there is **INSECURE DESERIALIZATION**. Do not load YKI you do not trust. Also, if you are passing arguments into you're Yokai Function and aren't providing input validation, you **WILL** end up with **OS COMMAND INJECTIONS**. This script is what you make of it and acts more as an extension of the capabilities of python. But this is not something that you should be using to prop up a prod server or just let loose to run for months at a time unchecked. You can do a lot with Yokai, but use it safely and responsibly.

To quote the Python mindset, "We are all consenting adults here."

## How to Install
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

## General `Yokai` Usage Example with `nmap`, `xsltproc`, and `searchsploit`
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
            BASH(f"nmap -Pn -sU --top-ports 1000 -vvv -d --reason --max-retries 2 -T3 --min-rate 500 -oA {outputdir}/{basename}_nmap_udp_1000 {target}"),
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


## Advanced `Yokai` Usage Example for HTB Recon
This is a complex Yokai example that is great for kicking of a box on Hack the Box and automates some basic recon.
#### WORDLISTS NOT INCLUDED!
```python
#============================================================================
# Imports 
from yokai import *

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

class HTB_Recon_yokai(Yokai):
    def __setup__(self, target, basename='yokai', outputdir=f"{YOKAI_DIR}/output"):
        if not os.path.exists(outputdir):
            os.makedirs(outputdir, exist_ok=True)
    
    # This will be passed over in favor of redefining the __execute__ method for 
    # greater control
    def __commands__(self, target, basename='yokai', outputdir=f"{YOKAI_DIR}/output"):
        pass


    # By default, the __execute__ method is predefined for easier usage. However,
    # you can redefine it for a tighter control of the execution flow.
    # Use with caution, as redefining the __execute__ method requires the manual
    # collection of information as well as manual excution calls, rather than it
    # being handled automatically
    def __execute__(self, target, basename='yokai', outputdir=f"{YOKAI_DIR}/output"):

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


        # `r` is the results YKI that will collect execution info
        # and will be returned upon completion.
        # The YKI here takes 2 arguments
        #   - The name of the Yokai Function as a string (self.__class__.__name__)
        #   - The scheduler that is being used (self.scheduler)
        r = YKI(self.__class__.__name__, self.scheduler)


        ### `r.commands[x]`
        # The commmands attribute of the YKI is a dict used to store the
        # execution info and order. The key is a number (Execution order)
        # and the object is the executed BASH/PYTHON object

        ### self.__run_bash_command__
        # This a method of every Yokai function used to execute BASH objects,
        # As expected it takes a BASH object, the same way it was defined in the 
        # General Usage example

        ### self.__run_python_function__
        # This a method of every Yokai function used to execute PYTHON objects,
        # As expected it takes a PYTHON object, the same way it was defined in the 
        # General Usage example


        # Run Nmap TCP scan
        r.commands[0] = self.__run_bash_command__(BASH(f"nmap -Pn -sS -p- --open -vvv -d -T4 --min-rate 1000 -oA {outputdir}/{basename}_nmap_tcp_all {target}"))

        # Convert results to HTML for easier reading
        r.commands[1] = self.__run_bash_command__(BASH(f"xsltproc {outputdir}/{basename}_nmap_tcp_all.xml -o {outputdir}/{basename}_nmap_tcp_all.html"))

        # Run Nmap UDP scan
        r.commands[2] = self.__run_bash_command__(BASH(f"nmap -Pn -sU --top-ports 1000 -vvv -d --reason --max-retries 2 -T4 --min-rate 1000 -oA {outputdir}/{basename}_nmap_udp_1000 {target}"))

        # Convert results to HTML for easier reading
        r.commands[3] = self.__run_bash_command__(BASH(f"xsltproc {outputdir}/{basename}_nmap_udp_1000.xml -o {outputdir}/{basename}_nmap_udp_1000.html"))
        
        # Parse out the TCP Ports
        r.commands[4] = self.__run_python_function__(PYTHON(parse_nmap_tcp_ports, f"{outputdir}/{basename}_nmap_tcp_all"))
        tcp_ports = r.commands[4].returned # Put TCP Ports into a variable
        
        # Parse out the UDP Ports
        r.commands[5] = self.__run_python_function__(PYTHON(parse_nmap_udp_ports, f"{outputdir}/{basename}_nmap_udp_1000"))
        udp_ports = r.commands[5].returned # Put UDP Ports into a varialbe
        
        # Parse out the live hosts from TCP
        r.commands[6] = self.__run_python_function__(PYTHON(parse_nmap_live, f"{outputdir}/{basename}_nmap_tcp_all"))
        tcp_live = r.commands[6].returned # Put live TCP hosts into a variable
        
        # Parse out the live hosts from UDP
        r.commands[7] = self.__run_python_function__(PYTHON(parse_nmap_live, f"{outputdir}/{basename}_nmap_udp_1000"))
        udp_live = r.commands[7].returned # Put live UDP hosts into a variable
        
        # Combine unique live hosts list and combine TCP and UDP ports lists
        live_hosts_arr = list(set(tcp_live + udp_live))
        live_ports_arr = tcp_ports + udp_ports

        # If no live hosts, just return and do not continue
        if live_hosts_arr == []:
            return r

        # Join the live hosts and live ports arrays into an Nmap string
        live_hosts = ' '.join(live_hosts_arr)
        live_ports = ','.join(live_ports_arr)

        # Run versioning Nmap scan
        r.commands[8] = self.__run_bash_command__(BASH(f"nmap -Pn -sS -sU -vvv -d --reason -O -sV --version-all -T4 --min-rate 1000 -p {live_ports} -oA {outputdir}/{basename}_versioning {live_hosts}"))
        
        # Convert results to HTML for easier reading
        r.commands[9] = self.__run_bash_command__(BASH(f"xsltproc {outputdir}/{basename}_versioning.xml -o {outputdir}/{basename}_versioning.html"))

        # Run banner Nmap scan
        r.commands[10] = self.__run_bash_command__(BASH(f"nmap -Pn -sS -sU -vvv -d --reason -O -sV --script=banner -T4 --min-rate 1000 -p {live_ports} -oA {outputdir}/{basename}_banners {live_hosts}"))

        # Convert results to HTML for easier reading
        r.commands[11] = self.__run_bash_command__(BASH(f"xsltproc {outputdir}/{basename}_banners.xml -o {outputdir}/{basename}_banners.html"))

        # Run an overly complex Nmap NSE scan that you definitely don't want to type twice
        r.commands[12] = self.__run_bash_command__(BASH(f"nmap --traceroute -sV -O --script \"all and not (dos or external or ssh-brute or broadcast or http-enum or http-wordpress-* or dns-* or ssl-* or http-vhosts or http-iis-short-name-brute or http-slowloris-check or http-phpmyadmin-dir-traversal)\" --script-args http.useragent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' -Pn -sS -sU -p {live_ports} -T4 --randomize-hosts --min-rate 1000 --max-retries 2 -vvv --open --reason -d --script-timeout 1m -oA {outputdir}/{basename}_nmap_nse {live_hosts}"))

        # Convert results to HTML for easier reading
        r.commands[13] = self.__run_bash_command__(BASH(f"xsltproc {outputdir}/{basename}_nmap_nse.xml -o {outputdir}/{basename}_nmap_nse.html"))

        # Search for exploits based on versioning
        r.commands[14] = self.__run_bash_command__(BASH(f"searchsploit --nmap {outputdir}/{basename}_versioning.xml > {outputdir}/{basename}_versioning_searchsploit.txt"))
        
        # Search for exploits based on banners
        r.commands[15] = self.__run_bash_command__(BASH(f"searchsploit --nmap {outputdir}/{basename}_banners.xml > {outputdir}/{basename}_banners_searchsploit.txt"))

        # Search for exploits based on NSE
        r.commands[16] = self.__run_bash_command__(BASH(f"searchsploit --nmap {outputdir}/{basename}_nmap_nse.xml > {outputdir}/{basename}_nmap_nse_searchsploit.txt"))

        # Check for which ports support HTTP/S
        r.commands[17] = self.__run_python_function__(PYTHON(check_ports_for_http, target, live_ports))
        urls = r.commands[17].returned # Add the returned URLs that support HTTP/S to a variable

        # If no ports support HTTP/S, just return and do not continue
        if urls == []:
            return r

        # Keep track of the command count as a var from hear on out
        cmd_count = 17 

        # Run whatweb against each url to determine the technologies used
        for i in range(len(urls)):
            port = urls[i].split(':')[-1][:-1]
            cmd_count += 1

            # Run whatweb against url
            r.commands[cmd_count] = self.__run_bash_command__(BASH(f"whatweb -v -a 3 --user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' --log-verbose={outputdir}/{basename}_whatweb_{port}.txt --log-json={outputdir}/{basename}_whatweb_{port}.json {urls[i]}"))
       
        # Run a VHOST enumeration with gobuster against each url
        for i in range(len(urls)):
            port = urls[i].split(':')[-1][:-1]
            postfix = f"_vhost_enum_{port}"
            cmd_count += 1

            # Run VHOST enum against url
            r.commands[cmd_count] = self.__run_bash_command__(BASH(f"gobuster vhost -w {YOKAI_DIR}/wordlists/combined_subdomains.txt -u {urls[i]} --append-domain -r -k --useragent 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' -t 40 -o {outputdir}/{basename}{postfix}.log"))
        
        # Run a dirbust against each url with a specific list with ffuf
        for i in range(len(urls)):
            port = urls[i].split(':')[-1][:-1]
            postfix = f"_cd_{port}"
            cmd_count += 1

            # Run the dirbust with FFUF
            r.commands[cmd_count] = self.__run_bash_command__(BASH(f"ffuf -w {YOKAI_DIR}/wordlists/combined_dir.txt -u {urls[i][:-1]}FUZZ -mc 200,204,301,302,307,401,403,405,500 -r -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' -t 40 -of json -o {outputdir}/{basename}{postfix}.json -debug-log {outputdir}/{basename}{postfix}_debug.log"))
            
            cmd_count += 1
            # Parse out the ffuf results with jq
            r.commands[cmd_count] = self.__run_bash_command__(BASH(f"jq -r '.results[] | [.url, .status] | @csv' {outputdir}/{basename}{postfix}.json > {outputdir}/{basename}{postfix}.csv"))
        
        # Run a dirbust against each url with another list with ffuf
        for i in range(len(urls)):
            port = urls[i].split(':')[-1][:-1]
            postfix = f"_common_{port}"
            cmd_count += 1

            # Run the dirbust with ffuf
            r.commands[cmd_count] = self.__run_bash_command__(BASH(f"ffuf -w {YOKAI_DIR}/wordlists/common.txt -u {urls[i][:-1]}/FUZZ -mc 200,204,301,302,307,401,403,405,500 -r -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' -t 40 -of json -o {outputdir}/{basename}{postfix}.json -debug-log {outputdir}/{basename}{postfix}_debug.log"))
            
            cmd_count += 1
            # Parse out the ffuf results with jq
            r.commands[cmd_count] = self.__run_bash_command__(BASH(f"jq -r '.results[] | [.url, .status] | @csv' {outputdir}/{basename}{postfix}.json > {outputdir}/{basename}{postfix}.csv"))
        
        # Run yet another dirbust against each url with another list with ffuf
        for i in range(len(urls)):
            port = urls[i].split(':')[-1][:-1]
            postfix = f"_dlm_{port}"
            cmd_count += 1

            # Run the dirbust with ffuf
            r.commands[cmd_count] = self.__run_bash_command__(BASH(f"ffuf -w {YOKAI_DIR}/wordlists/directory-list-2.3-medium.txt -u {urls[i][:-1]}/FUZZ -mc 200,204,301,302,307,401,403,405,500 -r -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' -t 40 -of json -o {outputdir}/{basename}{postfix}.json -debug-log {outputdir}/{basename}{postfix}_debug.log"))
            
            cmd_count += 1
            # Parse out the ffuf results with jq
            r.commands[cmd_count] = self.__run_bash_command__(BASH(f"jq -r '.results[] | [.url, .status] | @csv' {outputdir}/{basename}{postfix}.json > {outputdir}/{basename}{postfix}.csv"))
        

        # Finsihed
        # Return the final YKI or
        # go ahead and write the YKI to file with...
        # r.to_file(f"{outputdir}/{basename}.yki")
        return r
#============================================================================

```

