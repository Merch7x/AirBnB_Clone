#!/usr/bin/env python3
"""Acts as the main entry point for the backend
For development and Debugging purposes
"""
import cmd
import re
import sys
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Creates a command processor instance object."""
    prompt = '(hbnb)'
    __classes = {cls.__name__: cls for cls in [
        BaseModel, User, State, City, Place, Amenity, Review]}

    # def default(self, line):
    #     """Handle unknown syntax"""
    #     print(f"*** Unknown syntax: {line}")

    def do_help(self, arg):
        """Get help on commands"""
        if arg:
            super().do_help(arg)
            self.stdout.write('\n')
        else:
            self.stdout.write('\n')
            super().do_help(arg)

    def do_quit(self, arg):
        """quits the interpreter"""
        return sys.exit

    def do_EOF(self, arg):
        """Waits for EOF signal"""
        return True

    def default(self, arg):
        """Handle commands that have not been explicity defined"""
        defined = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"(\w+).(\w+)\((.*?)\)$", arg)

        if match:
            class_name, command, argument = match.groups()

            if command in defined:
                call = f"{class_name} {argument}"
                return defined[command](call)

        print(f"*** Unknown syntax: {arg}")

    def do_create(self, line):
        """Creates a BaseModel instance saves it to json
        and prints the id
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            arg = HBNBCommand.__classes[args[0]]
            my_arg = arg()
            storage.save()
            print(my_arg.id)

    def do_show(self, line):
        """Prints the string representation of an instance"""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                obj = storage.all()[key]
                print("[{}] ({}) {}".format(
                    type(obj).__name__,
                    obj.id,
                    str(obj.__dict__)
                ))

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id"""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                storage.all().pop(key)
                storage.save()
                # print("Instance is gone")  # debugging purposes

    def do_all(self, line):
        """Prints all string representation of all instances
        based or not on the class name
        """
        args = line.split()
        if len(args) == 0:
            res1 = []
            for value in storage.all().values():
                res1.append("[{}] ({}) {}".format(
                    type(value).__name__,
                    value.id,
                    str(value.__dict__)
                ))
            print(res1)
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            res2 = []
            for key, value in storage.all().items():
                if key.split('.')[0] == args[0]:
                    res2.append("[{}] ({}) {}".format(
                        type(value).__name__,
                        value.id,
                        str(value.__dict__)
                    ))
                print(res2)

    def do_update(self, line):
        """Updates an instance based on the class name and id
        by adding or updating attribute
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        elif len(args) < 3:
            print("* attribute name missing **")
        elif len(args) < 4:
            print("** value missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            my_dict = storage.all()
            if key in my_dict:
                obj = my_dict[key]
                setattr(obj, args[2], args[3])
            my_dict[args[2]] = str(args[3])
            storage.save()

    def do_count(self, line):
        """count the number of instances of a class"""
        args = line.split()

        if len(args) == 0:
            print("** class name is missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            count = sum(1 for obj in storage.all().values()
                        if isinstance(obj, HBNBCommand.__classes[args[0]]))
            print(count)

    def postloop(self):
        """Checks if the input is from terminal or not"""
        if not sys.stdin.isatty():
            print()
            return

    def emptyline(self):
        """Handles empty lines"""
        return


if __name__ == '__main__':
    HBNBCommand().cmdloop()
