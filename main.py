#!/usr/bin/env python3
import os
import sys
from typing import List, Tuple

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
TODO_FOLDER = "todo"
TODO_FILENAME = "todo.md"
TODO_PATH = os.path.join(SCRIPT_PATH, TODO_FOLDER, TODO_FILENAME)
PREFIX = "-"

CONFIG_FILE_NAME = "todo.myconfig"
CONFIG_FILE_PATH = os.path.join(SCRIPT_PATH, CONFIG_FILE_NAME)

# TODO: What are those
KNOWN_WORDS = ("files", "current")

def get_register_path(register: str) -> str:
    """
        Returns the register path to read and write
    """
    register_path = os.path.join(SCRIPT_PATH, TODO_FOLDER, register + ".md")
    return register_path
def print_info(*text: str, sep=" ") -> None:
    """
        Print info *text seperate by sep
    """
    print("\033[34m[INFO]\033[0m " + sep.join([str(i) for i in text]))
def print_error(*text: str, sep=" ") -> None:
    """
        Print info *text seperate by sep
    """
    print("\033[31;1;4m[ERROR]\033[0m " + sep.join([str(i) for i in text]))

def remove_spaces_from_iter(iter_: tuple) -> tuple:
    """
        Remove spaces from iterables that contains strings
    """
    return tuple(map(str.strip, iter_))
def parse_file(file_content: str) -> tuple:
    """
        Takes the file_content and parses it into a tuple that contains
        ((FILE1, FILE2,...), CURRENT_FILE)
    """
    file_names: List[str] = list()
    current_file = None
    # Split the content to lines
    # Remove the rest of #(comments)
    # Add it to the file_contains list if it's not empty
    # Add it after remove whitespace (strip)
    file_contains_list = [splitted.lower().strip() for splitted in [i.split("#")[0] for i in file_content.split("\n")] if splitted]

    # print(file_contains_list)
    for container in file_contains_list:
        var_name, var_contains = remove_spaces_from_iter(tuple(container.split("=")))
        assert len(KNOWN_WORDS) == 2, "You forgot to process word"
        if var_name == "files":
            file_names.extend(remove_spaces_from_iter(var_contains.split(",")))
        elif var_name == "current":
            current_file = var_contains
        else:
            assert False, "Unknow config option"
    tuple_content = (tuple(file_names), current_file)
    assert len(tuple_content) == 2, "You probably forgot some data to process"
    return tuple_content

def check_if_file_exists_and_create(path: str) -> bool:
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("")
    return True
def create_file(tuple_content: tuple) -> bool:
    """
        Takes a tuple in the format of parse_file and writes it into config file
    """
    assert len(tuple_content) == 2, "You probably forgot some data to process"
    (file_names, current_file) = tuple_content
    if current_file not in file_names:
        assert False, "creating new registers not implemented"
    with open(CONFIG_FILE_PATH, "w") as f:
        f.write("FILES={}".format(",".join(file_names)))
        f.write("\n")
        f.write("CURRENT={}".format(current_file))
    current_file_path = os.path.join(SCRIPT_PATH, TODO_FOLDER, current_file + ".md")
    check_if_file_exists_and_create(current_file_path)
    return True

def read_and_parse_file() -> tuple:
    if not os.path.exists(CONFIG_FILE_PATH):
        print_error("Config file {}, doesn't exists".format(CONFIG_FILE_NAME))
        sys.exit(0)
    print_info(f"Reading the file {CONFIG_FILE_PATH}")

    with open(CONFIG_FILE_PATH, "r") as f:
        return parse_file(f.read())
"""
Usage: exif [OPTION...] file
  -v, --version                   Display software version
  -i, --ids                       Show IDs instead of tag names
  -t, --tag=tag                   Select tag
      --ifd=IFD                   Select IFD
  -l, --list-tags                 List all EXIF tags
  -|, --show-mnote                Show contents of tag MakerNote
      --remove                    Remove tag or ifd
  -s, --show-description          Show description of tag
  -e, --extract-thumbnail         Extract thumbnail
  -r, --remove-thumbnail          Remove thumbnail
  -n, --insert-thumbnail=FILE     Insert FILE as thumbnail
      --no-fixup                  Do not fix existing tags in files
  -o, --output=FILE               Write data to FILE
      --set-value=STRING          Value of tag
  -c, --create-exif               Create EXIF data if not existing
  -m, --machine-readable          Output in a machine-readable (tab delimited) format
  -w, --width=WIDTH               Width of output
  -x, --xml-output                Output in a XML format
  -d, --debug                     Show debugging messages

Help options:
  -?, --help                      Show this help message
      --usage                     Display brief usage message

"""

def print_registers(register: str, file_names: tuple) -> bool:
    print_info("Registers are {}".format("\n\t".join(file_names)))
    print_info(f"Current register is {register}")
    return True
def create_new_register(new_register: str, file_names: tuple) -> bool:
    print_info(f"Creating {new_register}")
    tuple_content = (file_names + (new_register,), new_register)
    assert len(tuple_content) == 2, "You probably forgot some data to process"
    create_file(tuple_content)
def create_register(new_register: str, file_names) -> bool:
    if  new_register not in file_names:
        print_info("This register doesn't exist do you want to create it.")
        answer = input("[Y]es/[N]o")
        if answer.lower() == "yes" or answer.lower() == "y":
            return create_new_register(new_register, file_names)
        sys.exit(1)
    path = get_register_path(new_register)
    if not os.path.exists(path):
        with open(path, "w") as f: pass # Create the file
    assert os.path.exists(path), f"There's something wrong file {new_register}.md should've been already exist: {path}"
    tuple_content = (file_names, new_register)
    assert len(tuple_content) == 2, "You probably forgot processing new data"
    return create_file(tuple_content)
def usage() -> bool:
    """
        Prints the usage and returns
    """
    print("Usage:" + __file__ + " [OPTIONS] <todo>")
    print(" -h,     --help          " + "    Shows this help")
    print(" -a,     --add           " + "    Adds <todo> into todo list")
    print(" -l,     --list          " + "    Lists todo list")
    print(" -l -e,  --list --enum   " + "    Lists todo list with enumeration")
    print(" -l -c,  --list --check  " + "    Lists todo list with checked")
    print(" --restart               " + "    Removes everything")
    print(" -r, --remove    <index> " + "    Removes <index> from list")
    print(" -r -c                   " + "    Removes checked from list")
    print(" -c                      " + "    Lists todo list with checked")
    print(" -c, --check     <index> " + "    Checks  <index> from list")
    print(" -g, --register          " + "    Print registers and current register")
    print(" -g, --register  <regis> " + "    Change register to regis")
    return True
def write_to_todo(register: str, text: list) -> bool:
    """
        Write given list element to do TODO_PATH
    """
    # path = os.path.join(TODO_FOLDER, register + ".md")
    register_path = get_register_path(register)
    with open(register_path, "a+") as f:
        f.write(PREFIX + " " + str(" ".join(text)) + "\n")
    return True

def list_todo(register: str, enum=False, checked=False) -> bool:
    """
        List the elements of the list if enum is true list it with enumeration
    """
    to_print = ""
    register_path = get_register_path(register)
    with open(register_path , "r") as f:
        to_print = f.read()
    if enum:
        for index, item in enumerate(to_print.split("\n")):
            if item: print(str(index) + item)
        return True
    elif checked:
        for index, item in enumerate(to_print.split("\n")):
            # last_item = item[-1]
            # checking = item[-1] if item[-1] == "-" else " "
            if item: print("[{}]".format(item[-1] if item[-1] == "+" else " ") + item)
        return True
    print("\n".join([i for i in to_print.split("\n") if i]))
    return True
def remove_todo_list(register: str) -> bool:
    """
        Fully remove TODO_PATH
    """
    answer = input("Type `yes` and enter if you want to remove list: ")
    if answer == "yes":
        # register_path = os.path.join(TODO_FOLDER, register + ".md")
        register_path = get_register_path(register)
        with open(register_path, "w") as f:
            f.write("")
    print_info("List removed")
    return True

def remove_indexes_from_list(register: str, to_remove: list) -> bool:
    """
        Removes all the indexes inside of to_remove
    """
    # If to_remove is empty and it's a list(there shouldn't be any other type like None, "", ()...) don't do anything
    if not to_remove and isinstance(to_remove, list): return True
    print_info("Removing", *to_remove)
    int_to_remove = list(map(int, to_remove))
    # print(int_to_remove, to_remove)
    old_todo_list = None
    # register_path = os.path.join(TODO_FOLDER, register + ".md")
    register_path = get_register_path(register)
    with open(register_path, "r") as f:
        old_todo_list = f.read()
    todo_list = [i for i in old_todo_list.split("\n") if i]
    todo_list_len = len(todo_list)
    # print("Todo list length", todo_list_len)
    # print(int_to_remove, max(int_to_remove))
    if not todo_list_len:
        print_error("There is nothing to remove")
        usage()
        return False
    assert todo_list_len > max(int_to_remove), "Cannot remove out of bounds"
    # register_path = os.path.join(TODO_FOLDER, register + ".md")
    register_path = get_register_path(register)
    with open(register_path, "w") as f:
        for index, todo in enumerate(todo_list):
            if not(index in int_to_remove):
                f.write(todo + "\n")
    return True
def check_indexes_from_list(register: str, to_check: list) -> bool:
    """
        Check all the indexes inside of to_check
    """
    print_info("Checking: ", *to_check)
    int_to_check = list(map(int, to_check))
    # print(int_to_check, to_check)
    old_todo_list = None
    # register_path = os.path.join(TODO_FOLDER, register + ".md")
    register_path = get_register_path(register)
    with open(register_path, "r") as f:
        old_todo_list = f.read()
    todo_list = [i for i in old_todo_list.split("\n") if i]
    todo_list_len = len(todo_list)
    # print("Todo list length", todo_list_len)
    # print(int_to_check, max(int_to_check))
    if not todo_list_len:
        print("There is nothing to check")
        usage()
        return False
    assert todo_list_len > max(int_to_check), "Cannot check out of bounds"
    # register_path = os.path.join(TODO_FOLDER, register + ".md")
    register_path = get_register_path(register)
    with open(register_path , "w") as f:
        for index, todo in enumerate(todo_list):
            if index in int_to_check:
                f.write(todo + "/+" + "\n")
            else:
                f.write(todo + "\n")

    return True

def remove_checked_from_list(register: str) -> bool:
    list_of_indexes = []
    # register_path = os.path.join(TODO_FOLDER, register + ".md")
    register_path = get_register_path(register)
    with open(register_path, "r") as f:
        for index, line in enumerate(f.read().split("\n")):
            if line and line[-1] == "+":
                list_of_indexes.append(index)
    return remove_indexes_from_list(register, list_of_indexes)

def parse_args(config: tuple) -> bool:
    arguments = sys.argv
    script_name, *arguments = arguments
    file_names, register = config
    print_info("Register is '{}'".format(register))
    if "--help" in arguments or "-h" in arguments:
        return usage()
    if "-a" in arguments or "--add" in arguments:
        add, *arguments = arguments
        return write_to_todo(register, arguments)
    elif "-l" in arguments or "--list" in arguments:
        operation, *arguments = arguments
        enum = False
        checked = False
        if "-e" in arguments or "--enum" in arguments:
            assert len(arguments) != 0, f"There no option `{arguments}` after -l"
            enum = True
        if "-c" in arguments or "--check" in arguments:
            assert len(arguments) != 0, f"There no option `{arguments}` after -l"
            checked = True
        return list_todo(register, enum, checked)
    elif "--restart" in arguments:
        return remove_todo_list(register)
    elif "-r" in arguments or "--remove" in arguments:
        remove, *to_remove = arguments
        print(to_remove)
        # At least one arguments must be in the to_remove
        if "-c" in to_remove:
            return remove_checked_from_list(register)
        if not to_remove:
            usage()
            return False
        # Type check
        if not all(map(lambda x: x.isdigit(), to_remove)):
            raise ValueError("Index must be an integer")
        return remove_indexes_from_list(register, to_remove)
    elif "-c" in arguments or "--check" in arguments:
        option, *to_check = arguments
        # At least one arguments must be in the to_check
        if not to_check:
            return list_todo(register, False, True)
        # Type check
        if not all(map(lambda x: x.isdigit(), to_check)):
            raise ValueError("Index must be an integer")
        return check_indexes_from_list(register, to_check)
    elif "-g" in arguments or "--register" in arguments:
        option, *arguments = arguments
        assert len(arguments) == 0 or len(arguments) == 1, "No more than 1 argument"
        if len(arguments) == 0:
            print(file_names)
            return print_registers(register, file_names)
        else:
            new_register, *arguments = arguments
            return create_register(new_register, file_names)
    else:
        return usage()



def main():
    config = read_and_parse_file()
    sys.exit(parse_args(config))


if __name__ == "__main__":
    sys.exit(main())

