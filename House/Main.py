import os
import sys
from Utils.Input import get_number
import json


class ChoiceObject:
    _choices = []
    _in_use = None
    _name = None

    def __init__(self) -> None:
        pass

    def __str__(self):
        return json.dumps(self.to_dict())

    @classmethod
    def list(cls):
        res = "{} choices are \n".format(cls._name)
        for val in [
            {"name": x["name"], "index": i} for i, x in enumerate(cls._choices)
        ]:
            res += "({}): {} \n".format(val["index"], val["name"])
        res += "Your choice: "
        return res

    @classmethod
    def choose(cls):
        use = get_number(cls.list(), 0, len(cls._choices) - 1)
        new_object = cls()
        new_object._in_use = use
        print("You have chosen: {}".format(new_object.to_dict()["name"]))
        return new_object

    def to_dict(self):
        res = {}
        if self._in_use is not None:
            res = dict(self._choices[self._in_use])
            res.pop("alt_names")
        return res

    def name(self):
        return self.to_dict()["name"]

    @classmethod
    def from_name(cls, name):
        for val in [
            {"index": i, "name": x["name"], "alt_names": x["alt_names"]}
            for i, x in enumerate(cls._choices)
        ]:
            if val["name"].upper() == name.upper() or name.upper() in [
                v.upper() for v in val["alt_names"]
            ]:
                new_obj = cls()
                new_obj._in_use = val["index"]
                if "installed" in new_obj._choices[val["index"]].keys():
                    new_obj._choices[val["index"]]["installed"] = True
                return new_obj


class Status(ChoiceObject):
    _name = "Status"
    _choices = [
        {"name": "For sale", "alt_names": []},
        {"name": "For rent", "alt_names": []},
        {"name": "Rented", "alt_names": []},
        {"name": "Sold", "alt_names": []},
    ]

    def __init__(self) -> None:
        super().__init__()


class HeatingMethod(ChoiceObject):
    _name = "Heating"
    _choices = [
        {"name": "Bio-mass boiler", "energy_index": 3, "alt_names": []},
        {
            "name": "Central heating",
            "energy_index": 2,
            "alt_names": ["centralheating"],
        },
        {"name": "Block heating", "energy_index": 6, "alt_names": []},
        {"name": "Boiler heating", "energy_index": 1, "alt_names": ["boiler"]},
        {"name": "Hybrid heat pu`mp", "energy_index": 6, "alt_names": []},
        {"name": "Heat pump", "energy_index": 10, "alt_names": []},
    ]

    def __init__(self):
        super().__init__()


class EnergyOptions(ChoiceObject):
    _choices = [
        {
            "name": "Facade insulation",
            "installed": False,
            "energy_index": 6,
            "alt_names": ["facade"],
        },
        {
            "name": "Floor insulation",
            "installed": False,
            "energy_index": 6,
            "alt_names": ["floor"],
        },
        {
            "name": "Roof insulation",
            "installed": False,
            "energy_index": 6,
            "alt_names": ["roof"],
        },
        {
            "name": "Insulated glass",
            "installed": False,
            "energy_index": 6,
            "alt_names": ["glass"],
        },
        {
            "name": "Sun boiler",
            "installed": False,
            "energy_index": 6,
            "alt_names": ["sunboiler"],
        },
        {
            "name": "Ventilation heat pump",
            "installed": False,
            "energy_index": 6,
            "alt_names": ["ventilationheatpump"],
        },
        {
            "name": "Solar panels",
            "installed": False,
            "energy_index": 6,
            "alt_names": ["pv", "solar"],
        },
        {
            "name": "Shower heat recovery",
            "installed": False,
            "energy_index": 6,
            "alt_names": ["shower"],
        },
    ]
    _name = "Energy use measures"

    def __init__(self):
        pass

    def list_options(self):
        return [x for x in EnergyOptions._choices if x["installed"] == True]

    @classmethod
    def choose(cls):
        new_object = cls()
        choosing = True
        while choosing:
            choice = get_number(cls.list(), 0, len(cls._choices) - 1, quit_option=True)
            if choice == -1:
                choosing = False
            cls._choices[choice]["installed"] = True
            print("------------------------------------------------")
            print(
                "Chosen so far: {}".format(
                    ", ".join([x["name"] for x in new_object.list_options()])
                )
            )
            print("------------------------------------------------")
        print(
            "You have chosen: {}".format(
                ", ".join([x["name"] for x in new_object.list_options()])
            )
        )
        return new_object

    def to_dict(self):
        return self._choices


class House:
    _status = None
    _address = ""
    _postal_code = ""
    _num_rooms = -1
    _price = -1
    _heating = None
    _options = None

    def __init__(self):
        pass

    @classmethod
    def from_txt_data(
        cls, status, address, postal_code, num_rooms, price, heating, options=None
    ):
        new_object = cls()
        new_object._status = Status.from_name(status)
        new_object._address = address
        new_object._postal_code = postal_code
        new_object._num_rooms = num_rooms
        new_object._price = price
        new_object._heating = HeatingMethod.from_name(heating)
        new_object._options = EnergyOptions()
        return new_object

    def __str__(self):
        return f"{self._status.name()}: {self._address}, {self._postal_code}, {self._num_rooms} rooms, {self._price}, {self._heating.name()}"

    def to_dict(self):
        return {
            "status": self._status.name(),
            "address": self._address,
            "postal_code": self._postal_code,
            "num_rooms": self._num_rooms,
            "price": self._price,
            "heating": self._heating.name(),
            "options": self._options.to_dict(),
        }

    @classmethod
    def from_dict(cls, dict):
        new_object = cls()
        new_object._status = Status.from_name(dict["status"])
        new_object._address = dict["address"]
        new_object._postal_code = dict["postal_code"]
        new_object._num_rooms = dict["num_rooms"]
        new_object._price = dict["price"]
        new_object._heating = HeatingMethod.from_name(dict["heating"])
        options = EnergyOptions()
        options._choices = dict["options"]
        new_object._options = options

        return new_object


class HouseDatabase:
    _houses = []
    _db_filename = "house_database.json"

    def __init__(self):
        # self.load_houses_json()
        pass

    @classmethod
    def from_txt_file(cls, filename):
        new_object = cls()
        if os.path.exists(filename):
            with open(filename, "r") as file:
                num_houses = int(file.readline())
                for i in range(0, num_houses):
                    status = file.readline().strip().replace(":", "")
                    address = file.readline().strip()
                    postal_code = file.readline().strip()
                    num_rooms = int(file.readline().strip().split(" ")[0])
                    price = int(file.readline().strip().split(" ")[1])
                    heating = file.readline().strip()
                    new_object._houses.append(
                        House.from_txt_data(
                            status, address, postal_code, num_rooms, price, heating
                        )
                    )
        return new_object

    @classmethod
    def from_json(cls):
        houses_dict = []
        with open(cls._db_filename, "r") as content:
            houses_dict = json.load(content)
        new_object = cls()
        for val in houses_dict:
            cls._houses.append(House.from_dict(val))
        return new_object

    def to_dict(self):
        return [h.to_dict() for h in self._houses]

    def save(self):
        with open(self._db_filename, "w") as file:
            file.write(json.dumps(self.to_dict(), indent=4))

    def save_txt(self):
        with open(self._db_filename, "w") as file:
            file.write(str(len(self._houses)) + "\n")
            for house in self._houses:
                file.write(str(house) + "\n")

    def add_house(self):
        status = ["FOR SALE", "SOLD", "FOR RENT", "RENTED"]
        heating = ["boiler", "central heating"]
        status_id = get_number(
            "Enter the status of the house: (1) FOR SALE, (2) SOLD, (3) FOR RENT, (4) RENTED): ",
            1,
            4,
        )
        address = input("Enter the address of the house: ")
        postal_code = input("Enter the postal code of the house: ")
        num_rooms = get_number("Enter the number of rooms in the house: ", 1, 100)
        price = get_number("Enter the sale/rent price of the house: ", 1000, 1000000000)
        heating_id = get_number(
            "Enter the type of heating system in the house: (1) boiler or (2) central heating): ",
            1,
            2,
        )
        self.houses.append(
            House(
                status[status_id - 1],
                address,
                postal_code,
                num_rooms,
                price,
                heating[heating_id - 1],
            )
        )

    def print_list(self):
        [print(house) for house in self.houses]

    def filter_houses(self):
        price_min = int(input("Enter the minimum price: "))
        price_max = int(input("Enter the maximum price: "))
        status = input(
            "Enter the status of the house (FOR SALE, SOLD, FOR RENT, RENTED): "
        )
        heating = input(
            "Enter the type of heating system in the house (boiler or centralheating): "
        )
        filtered_houses = [
            house
            for house in self.houses
            if price_min <= house.price <= price_max
            and house.status == status
            and house.heating == heating
        ]
        if filtered_houses:
            for house in filtered_houses:
                print(house)
        else:
            print("No houses match the specified criteria.")


class Filter:
    def __init__(
        self,
        min_price=None,
        max_price=None,
        availability=None,
        sale_or_rent=None,
        energy_label=None,
    ):
        self.min_price = min_price
        self.max_price = max_price
        self.availability = availability
        self.sale_or_rent = sale_or_rent
        self.energy_label = energy_label

    def apply(self, houses):
        filtered_houses = []
        for house in houses:
            if (
                (self.min_price is None or house.price >= self.min_price)
                and (self.max_price is None or house.price <= self.max_price)
                and (
                    self.availability is None or house.availability == self.availability
                )
                and (
                    self.sale_or_rent is None or house.sale_or_rent == self.sale_or_rent
                )
                and (
                    self.energy_label is None or house.energy_label == self.energy_label
                )
            ):
                filtered_houses.append(house)
        return filtered_houses
