#!/usr/bin/env python3
import os
import sys
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
TODO_FOLDER = "todo"
TODO_FILENAME = "todo.md"
TODO_PATH = os.path.join(SCRIPT_PATH, TODO_FOLDER, TODO_FILENAME)
PREFIX = "-"

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

def usage() -> bool:
    """
        Prints the usage and returns
    """
    print("Usage:" + __file__ + " [OPTIONS] <todo>")
    print(" -h,     --help        " + "    Shows this help")
    print(" -a,     --add         " + "    Adds <todo> into todo list")
    print(" -l,     --list        " + "    Lists todo list")
    print(" -l -e,  --list --enum " + "    Lists todo list with enumeration")
    print(" -l -c,  --list --check" + "    Lists todo list with checked")
    print(" --restart             " + "    Removes everything")
    print(" -r, --remove <index>  " + "    Removes <index> from list")
    print(" -c, --check  <index>  " + "    Checks  <index> from list")
    return True
def print_info(*text: str, sep=" ") -> None:
    """
        Print info *text seperate by sep
    """
    print("[INFO]" + sep.join([str(i) for i in text]))
def write_to_todo(text: list) -> bool:
    """
        Write given list element to do TODO_PATH
    """
    with open(TODO_PATH, "a+") as f:
        f.write(PREFIX + " " + str(" ".join(text)) + "\n")
    return True

def list_todo(enum=False, checked=False) -> bool:
    """
        List the elements of the list if enum is true list it with enumeration
    """
    to_print = ""
    with open(TODO_PATH, "r") as f:
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
def remove_todo_list() -> bool:
    """
        Fully remove TODO_PATH
    """
    answer = input("Type `yes` and enter if you want to remove list: ")
    if answer == "yes":
        with open(TODO_PATH, "w") as f:
            f.write("")
    print_info("List removed")
    return True

def remove_indexes_from_list(to_remove: list) -> bool:
    """
        Removes all the indexes inside of to_remove
    """
    # If to_remove is empty and it's a list(there shouldn't be any other type like None, "", ()...) don't do anything
    if not to_remove and isinstance(to_remove, list): return True
    print_info("Removing", *to_remove)
    int_to_remove = list(map(int, to_remove))
    # print(int_to_remove, to_remove)
    old_todo_list = None
    with open(TODO_PATH, "r") as f:
        old_todo_list = f.read()
    todo_list = [i for i in old_todo_list.split("\n") if i]
    todo_list_len = len(todo_list)
    # print("Todo list length", todo_list_len)
    # print(int_to_remove, max(int_to_remove))
    if not todo_list_len:
        print("There is nothing to remove")
        usage()
        return False
    assert todo_list_len > max(int_to_remove), "Cannot remove out of bounds"
    with open(TODO_PATH, "w") as f:
        for index, todo in enumerate(todo_list):
            if not(index in int_to_remove):
                f.write(todo + "\n")
    return True
def check_indexes_from_list(to_check: list) -> bool:
    """
        Check all the indexes inside of to_check
    """
    print_info("Checking: ", *to_check)
    int_to_check = list(map(int, to_check))
    # print(int_to_check, to_check)
    old_todo_list = None
    with open(TODO_PATH, "r") as f:
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
    with open(TODO_PATH, "w") as f:
        for index, todo in enumerate(todo_list):
            if index in int_to_check:
                f.write(todo + "/+" + "\n")
            else:
                f.write(todo + "\n")

    return True

def remove_checked_from_list() -> bool:
    list_of_indexes = []
    with open(TODO_PATH, "r") as f:
        for index, line in enumerate(f.read().split("\n")):
            if line and line[-1] == "+":
                list_of_indexes.append(index)
    return remove_indexes_from_list(list_of_indexes)

def parse_args() -> bool:
    arguments = sys.argv
    script_name, *arguments = arguments
    if "--help" in arguments or "-h" in arguments:
        return usage()
    if "-a" in arguments or "--add" in arguments:
        add, *arguments = arguments
        return write_to_todo(arguments)
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
        return list_todo(enum, checked)
    elif "--restart" in arguments:
        return remove_todo_list()
    elif "-r" in arguments or "--remove" in arguments:
        remove, *to_remove = arguments
        print(to_remove)
        # At least one arguments must be in the to_remove
        if not to_remove:
            usage()
            return False
        # Type check
        if not all(map(lambda x: x.isdigit(), to_remove)):
            raise ValueError("Index must be an integer")
        return remove_indexes_from_list(to_remove)
    elif "-c" in arguments or "--check" in arguments:
        option, *to_check = arguments
        # At least one arguments must be in the to_check
        if not to_check:
            usage()
            return False
        # Type check
        if not all(map(lambda x: x.isdigit(), to_check)):
            raise ValueError("Index must be an integer")
        return check_indexes_from_list(to_check)
    elif "-rc" in arguments or "--remove-checked" in arguments:
        option, *arguments = arguments
        assert len(arguments) == 0, f"There shouldn't be a argument after `{option}`"
        return remove_checked_from_list()
    else:
        return usage()



def main():
    sys.exit(parse_args())


if __name__ == "__main__":
    main()

