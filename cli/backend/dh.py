from .document_db import DocumentDatabase
import re


class DevHelper():
    commands = [
            'list', 
            'add', 
            'run', 
            'config', 
            'switch', 
            'ask'
        ]
    
    def __init__(self, cli_args) -> None: 
        self.cmd = cli_args.cmd[0]
        self.cli_args = cli_args


    def execute(self):
        if self.cmd == self.commands[0]:
            if self.list_input_is_valid(self.cli_args.path):
                result = self.db.get(self.cli_args.path, self.cli_args.filter)
                self.format_query_result(result)
    
    def list_input_is_valid(self, input):
        if "." in input:
            is_valid = re.match(r'^[a-z]+\.[a-z]+$', input)
            return is_valid is not None
        is_valid = re.match(r'^[a-z]+$', input)
        return is_valid
    
    def new_cmd_input_is_valid(self, project_name, cmd_name):
        is_valid_project_name = re.match(r'^[a-z]+$', project_name)
        is_valid_command_name = re.match(r'^[a-z]+$', cmd_name)
        return is_valid_project_name and is_valid_command_name

    def format_query_result(self, result:list[dict]):
        for d in result:
            if isinstance(d, dict):
                keys = list(d.keys())
                values = list(d.values())
                for i in range(len(keys)):
                    print(
                    f"{keys[i].replace('_', ' ').upper()}: {values[i]}")
                print("------------------------------")
    