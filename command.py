class Command:
    def __init__(self, name, func, num_args):
        self.name = name
        self.func = func
        self.num_args = num_args

class CommandSystem:
    def __init__(self):
        self.commands = {}

    def add_command(self, name, func, num_args=None, help_msg=None):
        self.commands[name] = {'func': func, 'num_args': num_args, 'help_msg': help_msg}

    def remove_command(self, name):
        del self.commands[name]

    def list_commands(self):
        for name, data in self.commands.items():
            help_msg = f": {data['help_msg']}" if data['help_msg'] is not None else ""
            print(f"{name}{help_msg}")

    def execute_command(self, input_str):
        # Split input into command name and arguments
        parts = input_str.split()
        name = parts[0]
        args = parts[1:]

        # Check if command exists
        if name not in self.commands:
            raise ValueError(f"Unknown command '{name}'")

        # Check number of arguments
        num_args = self.commands[name]['num_args']
        if num_args is not None and len(args) != num_args:
            raise ValueError(f"Wrong number of arguments for command '{name}'")

        # Call the command function with arguments
        self.commands[name]['func'](*args)

    def help(self, *args):
        if len(args) > 0:
            name = args[0]
            if name not in self.commands:
                print(f"Unknown command '{name}'")
                return
            data = self.commands[name]
            help_msg = f": {data['help_msg']}" if data['help_msg'] is not None else ""
            print(f"{name}{help_msg}")
        else:
            print("Available commands:")
            self.list_commands()

