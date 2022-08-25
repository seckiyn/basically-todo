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

def usage():
    print("Usage:" + __file__ + " [OPTIONS] <todo>")
    print(" -a,  --add            " + "    Adds <todo> into todo list")
    print(" -l,  --list           " + "    Lists todo list")
    print(" -l -e,  --list --enum " + "    Lists todo list with enumeration")
def print_info(text):
    print("[INFO]" + text)
def write_to_todo(text: list) -> None:
    with open(TODO_PATH, "a+") as f:
        f.write(PREFIX + " " + str(" ".join(text)))

def list_todo(enum=0):
    to_print = ""
    with open(TODO_PATH, "r") as f:
        to_print = f.read()
    if enum:
        for index, item in enumerate(to_print.split("\n")):
            print(str(index) + item)
        return enum
    print(to_print)
    return enum
def remove_todo_list():
    answer = input("Type `yes` and enter if you want to remove list: ")
    if answer == "yes":
        with open(TODO_PATH, "w") as f:
            f.write("")
    print_info("List removed")
def parse_args():
    arguments = sys.argv
    script_name, *arguments = arguments
    if "-a" in arguments or "--add" in arguments:
        add, *arguments = arguments
        write_to_todo(arguments)
    elif "-l" in arguments or "--list" in arguments:
        listing, *arguments = arguments
        enum = False
        if "-e" in arguments or "--enum" in arguments:
            enum = True
        list_todo(enum)
    elif "--remove" in arguments:
        remove_todo_list()
    else:
        usage()






def main():
    parse_args()


if __name__ == "__main__":
    main()
