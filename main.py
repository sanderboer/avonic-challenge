import os
import sys
from House.Main import HouseDatabase
from Utils.State import UiState


def main():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    database = HouseDatabase.from_json()
    ui_state = UiState(database)
    while ui_state.choose_action() != 3:
        pass


if __name__ == "__main__":
    sys.exit(main())  # next section explains the use of sys.exit
