#!/usr/bin/python3
"""This module implements a simple command interpreter for AirBnB program.
"""
import cmd
import re

from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """Entry point of the command interpreter.

    Args:
        cmd (module): extends the functionality of the cmd module

    Returns:
        _type_: _description_
    """

    prompt = "(hbnb) "
    classes = {"BaseModel",
               "User",
               "State",
               "City",
               "Place",
               "Review",
               "Amenity",
               }

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """Quit command to exit the program."""
        print()
        return True

    def emptyline(self) -> bool:
        # return super().emptyline()
        pass

    def do_create(self, arg):
        """Create an object from the model specified by its class."""
        if not arg or len(arg) == 0:  # TO BE CHECKED
            print("** class name missing **")
            return
        if arg not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        obj = eval(arg)()
        obj.save()
        print(obj.id)

    def do_show(self, args):
        """Print the string representation of an instance.
        Representation is based on the class name and id.

        Args:
            args (str): a string containing args separated by spaces.
        """
        args = args.split()
        if not args or len(args) == 0:
            print("** class name missing **")
            return
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            print("** instance id missing **")
            return
        elif "{}.{}".format(args[0], args[1]) not in storage.all():
            print("** no instance found **")
            return
        else:
            print(storage.all()["{}.{}".format(args[0], args[1])])

    def do_destroy(self, args):
        """Delete an instance based on the class name and id.
        (save the change into the JSON file)

        Args:
            args (str): a string containing args separated by spaces.
        """
        args = args.split()
        if not args or len(args) == 0:
            print("** class name missing **")
            return
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            print("** instance id missing **")
            return
        elif "{}.{}".format(args[0], args[1]) not in storage.all():
            print("** no instance found **")
            return
        else:
            del storage.all()["{}.{}".format(args[0], args[1])]
            storage.save()

    def do_all(self, args):
        """Print all string representation of all instances.
        Representation is based or not on the class name.

        Args:
            args (str): a string containing args separated by spaces.
        """
        args = args.split()
        if args and args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        list_of_instances = []
        for i in storage.all().values():
            list_of_instances.append(eval(i.__class__.__name__)(**i).__str__())
        print(list_of_instances)

    def do_count(self, args):
        """Print number of objects from class."""
        args = args.split()
        if not args or len(args) != 1:
            print("** class name missing **")
            return
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        else:
            instances = 0
            for i in storage.all().values():
                if args[0] == i["__class__"]:
                    instances += 1
            print(instances)

    def do_update(self, args):
        """Print all string representation of all instances
        Represenation is based or not on the class name.

        Args:
            args (str): a string containing args separated by spaces.
        """
        args = args.split()
        if not args or len(args) == 0:
            print("** class name missing **")
            return
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            print("** instance id missing **")
            return
        elif "{}.{}".format(args[0], args[1]) not in storage.all():
            print("** no instance found **")
            return
        elif len(args) < 3:
            print("** attribute name missing **")
            return
        elif len(args) < 4:
            print("** value missing **")
            return
        elif args[2] in ["created_at", "updated_at", "id"]:
            return
        else:
            key = args[2]
            value = args[3]
            # check that the input has a dictionary from the 3rd command
            x = "".join(args[2:])
            x = x.replace(":", ": ").replace(",", ", ")
            if x.startswith("{") and x.endswith("}"):
                # convert the 3rd command from str to dict and iterate
                try:
                    for k, v in eval("{}".format(x)).items():
                        # update the dict with the key and value...
                        storage.all()["{}.{}".format(args[0], args[1])][k] = v
                except ValueError:
                    print("Invalid Dictionary")
            else:
                # no dictionary - standard format.
                storage.all()["{}.{}".format(args[0], args[1])][key] = value
                storage.save()

    def default(self, line: str) -> None:
        """Call on an input line when the command prefix is not recognized.

        If this method is not overridden, it prints an error message and
        returns.

        Args:
            line (str): sting of commands in a non-standard format

        Returns:
            str: calls the corresponding command the standard format
        """
        calls = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update,
        }

        if "." not in line:
            print("** Unknown syntax: {}\n".format(line))
            return False
        else:
            args = line.split(".", maxsplit=1)
            # split the second arg at '(',')', and ','
            others = re.split(r"[)(,]", args[1])
            # remove spaces in the result elements
            others = [i.strip() for i in others]
            command = others[0]
            string = args[0] + " " + " ".join(others[1:])
            if command in calls.keys():
                return calls[others[0]](string)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
    # print("") # TODO will this be valid for all exits
