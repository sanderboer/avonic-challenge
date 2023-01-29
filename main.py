import os
import sys
from House.Main import HouseDatabase


def main():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    houses = HouseDatabase("testdata.txt")
    houses.print_list()


if __name__ == "__main__":
    sys.exit(main())  # next section explains the use of sys.exit
