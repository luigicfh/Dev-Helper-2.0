import argparse
import re
from backend.document_db import DocumentDatabase
import os
import yaml

cwd = os.getcwd()
document_db_path = os.path.join(cwd, "backend", "db.json")

def validate_list_input(namespace:str) -> list:
    if namespace == "default":
        return []
    if "." not in namespace:
        return [namespace]
    if re.match(r'^[a-z]+\.[a-z]+$', namespace) is not None:
        return namespace.split(".")
    return []

def validate_add_input(project:str, name:str):
    if not project.islower() and not project.isalpha(): 
        return False, """Project names must be lowercase 
        and only include alphabetical characters.""",
    if len(project) > 8:
        return False, """Project names can't exceed 8 
        characters in length."""
    if not name.islower() and not name.isalpha():
        return False, """Shortcut command names must be 
        lowercase and only include alphabetical characters."""
    return True, "Valid inputs."

def validate_delete_input(project:str):
    if project is None:
        raise ValueError("Provide a project name to delete.")
    return True

def validate_update_input(project:str, name:str, command:str):
    if project is None and name is None and command is None:
        raise ValueError(
        "Please provide the project and shortcut to update")
    return True

def validate_run_input(name:str):
    if name is None:
        raise ValueError(
        "Please provide a shortcut name.")
    return

def generate_new_command(name: str, desc:str, command:str):
    return {
        "name": name,
        "description": desc,
        "command": command
    }

def parse():
    commands = [
            'list', 
            'add',
            'delete',
            'update',
            'run', 
            'config', 
            'switch', 
            'ask'
        ]
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", 
        choices=commands,
    )
    parser.add_argument('-namespace', '-n', type=str, default="default")
    # Adding filters later
    # parser.add_argument('-filter', '-f', type=str)
    parser.add_argument('-project', '-pr', type=str, default=None)
    parser.add_argument('-description', '-d', type=str)
    parser.add_argument('-command', '-c', type=str, default=None)
    parser.add_argument('-ask', '-a', type=str)
    parser.add_argument("-shortcut", "-s", type=str, default=None)
    args = parser.parse_args()
    db = DocumentDatabase(document_db_path)

    if args.cmd == commands[0]:
        namespace = validate_list_input(args.namespace)
        if len(namespace) == 0:
            print(yaml.dump(db.data))
        elif len(namespace) == 1:
            project = db.get_document(namespace[0])
            print(yaml.dump(project))
        else:
            project = db.get_document(namespace[0])
            if project is None:
                return
            sub_section = project.get(namespace[1])
            print(yaml.dump(sub_section))
        return

    if args.cmd == commands[1]:
        input_valid = validate_add_input(args.project, args.shortcut)
        if not input_valid[0]:
            raise Exception(input_valid[1])
        project = db.get_document(args.project)
        new_command = generate_new_command(args.shortcut, args.description, args.command)
        if project is None:
            commands = {
                "commands": [new_command]
            }
            db.add_document(args.project, commands)
            db.save()
            print(
            f"New command {args.shortcut} added successfuly.")
            return
        commands = project.get("commands")
        existing_command_names = [cmd["name"] for cmd in commands]
        if new_command["name"] in existing_command_names:
            raise ValueError(
            """Command names must be unique in the project namespace""")
        commands.append(new_command)
        project['commands'] = commands
        db.update_document(args.project, project)
        db.save()
        print(
        f"New command {args.shortcut} added successfuly.")
        return

    if args.cmd == commands[2]:
        validate_delete_input(args.project)
        if args.shortcut is None:
            db.delete_document(args.project)
            db.save()
            print(f"Project {args.project} deleted successfuly.")
            return
        project = db.get_document(args.project)
        commands = project.get("commands")
        existing_command_names = [cmd["name"] for cmd in commands]
        if args.shortcut not in existing_command_names:
            raise ValueError(
            f"Command shortcut {args.shortcut} does not exist.")
        index_of_command = existing_command_names.index(args.shortcut)
        del commands[index_of_command]
        project["commands"] = commands
        db.update_document(args.project, project)
        db.save()
        print(
        f"Command {args.shortcut} deleted successfuly.")
        return
    
    if args.cmd == commands[3]:
        validate_update_input(
        args.project, args.shortcut, args.command)
        project = db.get_document(args.project)
        commands = project.get("commands")
        existing_command_names = [cmd["name"] for cmd in commands]
        if args.shortcut not in existing_command_names:
            raise ValueError(
            f"Command shortcut {args.shortcut} does not exist.")
        index_of_command = existing_command_names.index(args.shortcut)
        command = commands[index_of_command]
        if args.description is not None:
            command["description"] = args.description
        command["command"] = args.command
        commands[index_of_command] = command
        project["commands"] = commands
        db.update_document(args.project, project)
        db.save()
        print(
        f"Command {args.shortcut} updated successfuly.")
        return
    
    if args.cmd == commands[4]:
        validate_run_input(args.shortcut)
        active_config = db.data.get("activeConfig")
        if "project" not in active_config.keys():
            print("It seems that you have not activated a project.")
            project = input(
            f"Please provide the project name of the command {args.shortcut}: ")
            if project is None:
                raise ValueError("Please provide a valid project name.")
            if project not in db.data.keys():
                raise ValueError(f"Project {project} does not exist.")
            db.update_document("activeConfig", {"project": project})
            db.save()
        active_project = active_config.get("project")
        project = db.get_document(active_project)
        commands = project.get("commands")
        existing_command_names = [cmd["name"] for cmd in commands]
        index_of_command = existing_command_names.index(args.shortcut)
        command = commands[index_of_command].get("command")
        os.system(command)

if __name__ == '__main__':
    parse()