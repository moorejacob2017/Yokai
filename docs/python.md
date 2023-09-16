# `class PYTHON`
```python
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
```

## Attributes
- `function` - The python function as an object
- `arguments` - The python argument objects in a tuple
- `kw_arguments` - They python keyword arguments and their objects in a dictionary
- `started_at` - a `datetime.datetime.strptime` of when the python function started execution (year-month-day hour:minute:second)
- `finished_at` - a `datetime.datetime.strptime` of when the python function stopped execution (year-month-day hour:minute:second)
- `returned` - The object returned by the python function
- `stdout` - The standard output of the python function as a string
- `stderr` - The python error formatted as a string

## Functions
- `__init__` Takes the python function, python function args, and python function kw_args, and sets the dates to epoch 0, and the returned object to `False`
- `to_dict` - Converts the `PYTHON` into a subscribable python dictionary object
- `to_json` - Converts the `PYTHON` into a json friendly/serializable object

