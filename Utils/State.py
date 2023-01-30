from House.Main import HouseDatabase
from Utils.Input import ChoiceObject, get_number


class Filter(ChoiceObject):
    _db: HouseDatabase
    _name: "Filter"
    _choices = [
        {"name": "Price.", "alt_names": []},
        {"name": "Houses for sale", "alt_names": []},
        {"name": "Houses that have been sold", "alt_names": []},
        {"name": "Houses for rent", "alt_names": []},
        {"name": "Houses that have been rented out", "alt_names": []},
        {"name": "Energy label", "alt_names": []},
    ]

    def __init__(self, database):
        self._db = database
        super().__init__()

    def choose_action(self):
        use = get_number(self.list(), 0, len(self._choices) - 1)
        if use == 0:
            self.filter_price()
        elif use == 1:
            self.filter_sale()
        elif use == 2:
            self.filter_sold()
        elif use == 3:
            self.filter_rent()
        elif use == 4:
            self.filter_rented()
        elif use == 5:
            self.filter_energy()

    def filter_price(self):
        min_price = get_number("minimum price : ", 1, 10000000)
        max_price = get_number("maximum price : ", min_price, 10000000)
        for house in self._db._houses:
            if min_price <= house._price <= max_price:
                print(house.overview())

    def filter_sale(self):
        for house in self._db._houses:
            if house._status.name().upper() == "For sale".upper():
                print(house.overview())

    def filter_sold(self):
        for house in self._db._houses:
            if house._status.name().upper() == "Sold".upper():
                print(house.overview())

    def filter_rent(self):
        for house in self._db._houses:
            if house._status.name().upper() == "For rent".upper():
                print(house.overview())

    def filter_rented(self):
        for house in self._db._houses:
            if house._status.name().upper() == "rented".upper():
                print(house.overview())

    def filter_energy(self):
        valid_choice = False
        label = ""
        while not valid_choice:
            label = input(
                "Select energy label: (most efficient) A, B, C, D or E (least efficient) or X to cancel"
            )
            if label.upper() in ["A", "B", "C", "D", "E", "X"]:
                valid_choice = True
            else:
                print("Invalid choice, please repeat.")
        for house in self._db._houses:
            if label.upper() == house.energy_label():
                print(house.overview())


class UiState(ChoiceObject):
    _db: HouseDatabase
    _name = "House"
    _choices = [
        {"name": "List all houses.", "alt_names": []},
        {"name": "Filter houses.", "alt_names": []},
        {"name": "Add a new house.", "alt_names": []},
        {"name": "Save and Quit.", "alt_names": []},
    ]
    _filter: Filter

    def __init__(self, database: HouseDatabase):

        self._db = database
        self._filter = Filter(database)
        super().__init__()

    def choose_action(self):
        use = get_number(self.list(), 0, len(self._choices) - 1)
        if use == 0:
            self._db.print_list()
        elif use == 1:
            self._filter.choose_action()
        elif use == 2:
            self._db.add_house()
        elif use == 3:
            self._db.save_txt()
        return use
