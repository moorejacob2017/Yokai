
# `class BASH`

```python
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
```

## Attributes
- `command` - The bash command as a string
- `started_at` - a `datetime.datetime.strptime` of when the bash command started execution (year-month-day hour:minute:second)
- `finished_at` - a `datetime.datetime.strptime` of when the bash command stopped execution (year-month-day hour:minute:second)
- `stdout` - The console standard output of the command as a string
- `stderr` - The console standard error output of the command as a string

## Functions
- `__init__` Takes the bash command as a string, initializes dates to epoch 0
- `to_dict` - Converts the `BASH` into a subscribable python dictionary object
- `to_json` - Converts the `BASH` into a json friendly/serializable object