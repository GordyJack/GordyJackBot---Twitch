import json
import datetime


def load_command_data():
    with open('command_data.json') as f:
        return json.load(f)


def get_command_property(command, property_key="enabled"):
    command_data = load_command_data()
    return command_data[command][property_key]


def get_all_commands_with_property_value(property_key, property_value):
    command_data = load_command_data()
    command_list = []
    for command, properties in command_data.items():
        if properties[property_key] == property_value:
            command_list.append(command)
    return command_list


def get_date_format():
    return "%Y-%m-%d|%H:%M:%S"


def save_command_property(command, property_key, property_value):
    command_data = load_command_data()
    command_data[command][property_key] = property_value
    save_command_data(command_data)


def save_command_data(command_data):
    with open('command_data.json', 'w') as f:
        json.dump(command_data, f, indent=4)


def update_disabled_commands(commands, disabled_commands=None):
    command_data = {command: {"enabled": True, "last_used": "never"} for command in commands}
    if disabled_commands:
        for command in disabled_commands:
            command_data[command]["enabled"] = False
    save_command_data(command_data)


def update_last_used(command_name):
    save_command_property(command_name, "last_used", datetime.datetime.now().strftime(get_date_format()))
