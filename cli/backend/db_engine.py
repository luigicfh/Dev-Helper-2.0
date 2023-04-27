import json
import os
import datetime

class DocumentDb():

    def __init__(self) -> None:
        self.path_parts = ["commands", "asked"]
        self.db_path = os.path.join(os.getcwd(), "backend", 'db.json')
        self.db = self._open_db()
        self.struct_attrs = [
            "name", 
            "description", 
            "command", 
            "last_change", 
            "question", 
            "answer", 
            "created"
        ]
        self.comparison_operators = [
            "==",
            "!="
        ]
        self.membership_operator = [
            "like"
        ]

    def _open_db(self):
        with open(self.db_path) as document:
            db = json.loads(document.read())
        return db
    
    def add_cmd(self, project, name, description, command):
        existing_projects = [project["project"] for project in self.db]
        if project in existing_projects:
            updated_db = self.db.copy()
            project_index = existing_projects.index(project)
            existing_project = updated_db[project_index]
            commands = existing_project["commands"]
            existing_command_names = [cmd["name"] for cmd in commands] if len(commands) > 0 else []
            if name in existing_command_names:
                raise ValueError("Command names must be unique.")
            new_command = self.generate_new_cmd(name, description, command)
            commands.append(new_command)
            existing_project["commands"] = commands
            updated_db[project_index] = existing_project
            self.save(updated_db)
        else:
            updated_db = self.db.copy()
            existing_project = self.generate_project(project)
            commands = existing_project["commands"]
            existing_command_names = [cmd["name"] for cmd in commands] if len(commands) > 0 else []
            if name in existing_command_names:
                raise ValueError("Command names must be unique.")
            new_command = self.generate_new_cmd(name, description, command)
            commands.append(new_command)
            existing_project["commands"] = commands
            updated_db[-1] = existing_project
            self.save(updated_db)
        return new_command
    
    def generate_new_cmd(self, name, description, command):
        return {
            "name": name,
            "description": description,
            "command": command,
            "last_change": datetime.datetime.now().isoformat()
        }
    
    def generate_project(self, project_name):
        return {
            "project": project_name,
            "commands": [],
            "asked": []
        }
    
    def save(self, db):
        with open(self.db_path, "w") as document:
            document.write(json.dumps(db, indent=4))

    def get(self, path: str, filter:str|None=None):
        path_parts = path.split(".")
        if len(path_parts) > 2:
            raise Exception("Invalid path structure")
        if len(path_parts) == 1 and path_parts[0] != '':
            project = [project for project in self.db if project['project'] == path_parts[0]]
            return project
        if len(path_parts) == 1 and path_parts[0] == '':
            return [project['project'] for project in self.db]
        if len(path_parts) == 2:
            if path_parts[1] not in self.path_parts:
                raise KeyError(
                    f"Invalid key {path_parts[1]}, use one of the following: {' or '.join(self.path_parts)}")
            project = [project for project in self.db if project['project'] == path_parts[0]]
            if filter is None:
                return project[0][path_parts[1]]
            return self._filter(
                path_parts[1], project[0][path_parts[1]], filter)
    
    def _filter(self, attr:str, structs:list, filter:str):
        parsed_filter = filter.split(" ")
        if len(parsed_filter) != 3:
            raise ValueError("Invalid filter expression.")
        key = parsed_filter[0]
        operator = parsed_filter[1]
        value = parsed_filter[2]
        if key not in self.struct_attrs:
            raise KeyError(f"Invalid key {key}.")
        if operator not in self.comparison_operators:
            if operator not in self.membership_operator:
                raise ValueError(f"Invalid operator {operator}")
        if attr == 'commands':
            return self._get_filtered_results(
                structs, operator, key, value)
        if attr == 'asked':
            return self._get_filtered_results(
                structs, operator, key, value)
        
    def _get_filtered_results(self, structs:list[dict], operator:str, key:str, value:str):
        filtered_struct = []
        if operator in self.comparison_operators:
            for obj in structs:
                if eval(f'"{obj[key]}" {operator} "{value}"'):
                    filtered_struct.append(obj)
        if operator in self.membership_operator:
            for obj in structs:
                if value in obj[key]:
                    filtered_struct.append(obj)
        return filtered_struct
        