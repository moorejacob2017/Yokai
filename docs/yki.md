# `class YKI`

```python
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
```

## Attributes
- `commands` - An array of executed `BASH` and `PYTHON` objects
- `yokai_function` - The name of the yokai function tha produced the `YKI`
- `schedule` - The `ExecutionSecheduler` used by the yokai function that produced the `YKI`

## Functions
- `__init__` - Optionally take a copy of the `ExecutionScheduler` used or the yokai_function name
- `to_file` - Serializes a `YKI` to a file given a path
- `from_file` - Deserializes and imports a `YKI` from a file path
- `print` - Prints out the `YKI` to console