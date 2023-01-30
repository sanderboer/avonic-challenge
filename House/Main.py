import os
import sys
from Utils.Input import get_number
import json
from Utils.Input import ChoiceObject


class Status(ChoiceObject):
    _name = "Status"
    _choices = [
        {"name": "For sale", "alt_names": []},
        {"name": "For rent", "alt_names": []},
        {"name": "Rented", "alt_names": []},
        {"name": "Sold", "alt_names": []},
    ]

    def __init__(self):
        super().__init__()


class HeatingMethod(ChoiceObject):
    _name = "Heating"
    _choices = [
        {"name": "Bio-mass boiler", "energy_index": 10, "alt_names": []},
        {
            "name": "Central heating",
            "energy_index": 10,
            "alt_names": ["centralheating"],
        },
        {"name": "Block heating", "energy_index": 10, "alt_names": []},
        {"name": "Boiler heating", "energy_index": 1, "alt_names": ["boiler"]},
        {"name": "Hybrid heat pu`mp", "energy_index": 20, "alt_names": []},
        {"name": "Heat pump", "energy_index": 30, "alt_names": []},
    ]

    def __init__(self):
        super().__init__()


class EnergyOptions(ChoiceObject):
    _choices = {}
    _name = "Energy use measures"

    def __init__(self):
        self._choices = [
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
        super().__init__()
        pass

    def list_options(self):
        return [x for x in self._choices if x["installed"] == True]

    @classmethod
    def choose_input(cls):
        new_object = cls()
        question = "{} choices are \n".format(new_object._name)
        for val in [
            {"name": x["name"], "index": i} for i, x in enumerate(new_object._choices)
        ]:
            question += "({}): {} \n".format(val["index"], val["name"])
        question += "Your choice: "
        choosing = True
        while choosing:
            choice = get_number(
                question, 0, len(new_object._choices) - 1, quit_option=True
            )
            if choice == -1:
                choosing = False
            else:
                new_object._choices[choice]["installed"] = True
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

    @classmethod
    def from_csv_str(cls, csv_str):
        new_object = cls()
        values = [int(x) for x in csv_str.split(",")]
        for i, value in enumerate(values):
            if i < len(new_object._choices):
                new_object._choices[i]["installed"] = True if value == 1 else False
        return new_object

    def to_dict(self):
        return self._choices

    def print_csv(self):
        options_list = list(
            map(lambda c: "1" if c["installed"] else "0", self._choices)
        )
        return ",".join(options_list)


class House:
    _status: Status
    _address = ""
    _postal_code = ""
    _num_rooms = -1
    _price = -1
    _heating: HeatingMethod
    _options: EnergyOptions

    def __init__(self):
        pass

    @classmethod
    def from_txt_data(
        cls, status, address, postal_code, num_rooms, price, heating, options
    ):
        new_object = cls()
        new_object._status = Status.from_name(status)
        new_object._address = address
        new_object._postal_code = postal_code
        new_object._num_rooms = num_rooms
        new_object._price = price
        new_object._heating = HeatingMethod.from_name(heating)
        new_object._options = EnergyOptions.from_csv_str(options)
        return new_object

    def __str__(self):
        return "{}:\n{}\n{}\n{} rooms\n{}\n{}\n{}\n".format(
            self._status.name(),
            self._address,
            self._postal_code,
            self._num_rooms,
            self.print_price(),
            self._heating.name(),
            self._options.print_csv(),
        )

    def overview(self):
        return "{}: {}, {}, {} rooms, {}, {}, label: {} options: {}".format(
            self._status.name(),
            self._address,
            self._postal_code,
            self._num_rooms,
            self.print_price(),
            self._heating.name(),
            self.energy_label(),
            ", ".join(
                [x["name"] for x in self._options.list_options()],
            ),
        )

    def energy_label(self):
        heating_req = self._num_rooms * 50
        energy_pts = self._heating.to_dict()["energy_index"]
        for option in self._options._choices:
            if option["installed"]:
                energy_pts += option["energy_index"]
        measure = heating_req / energy_pts
        label_vals = [
            {"label": "A", "min": 0, "max": 50},
            {"label": "B", "min": 51, "max": 100},
            {"label": "C", "min": 101, "max": 150},
            {"label": "D", "min": 151, "max": 200},
            {"label": "E", "min": 201, "max": 500000},
        ]
        res = ""
        for label in label_vals:
            if label["min"] <= measure <= label["max"]:
                res = label["label"]
        return res

    def print_price(self):
        pre_str = "saleprice"
        if self._status.name().upper() in ["RENTED", "FOR RENT"]:
            pre_str = "rentprice"
        return "{} {}".format(pre_str, self._price)

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


class HouseDatabase:
    _houses = []
    _db_filename = "house_database"

    def __init__(self):
        # self.load_houses_json()
        pass

    @classmethod
    def from_txt_file(cls):
        new_object = cls()
        if os.path.exists(cls._db_filename + ".txt"):
            with open(cls._db_filename + ".txt", "r") as file:
                num_houses = int(file.readline())
                for i in range(0, num_houses):
                    status = file.readline().strip().replace(":", "")
                    address = file.readline().strip()
                    postal_code = file.readline().strip()
                    num_rooms = int(file.readline().strip().split(" ")[0])
                    price = int(file.readline().strip().split(" ")[1])
                    heating = file.readline().strip()
                    options = file.readline().strip()
                    new_object._houses.append(
                        House.from_txt_data(
                            status,
                            address,
                            postal_code,
                            num_rooms,
                            price,
                            heating,
                            options,
                        )
                    )
        return new_object

    def to_dict(self):
        return [h.to_dict() for h in self._houses]

    def save_json(self):
        with open(self._db_filename + ".json", "w") as file:
            file.write(json.dumps(self.to_dict(), indent=4))

    def save_txt(self):
        with open(self._db_filename + ".txt", "w") as file:
            file.write(str(len(self._houses)) + "\n")
            for house in self._houses:
                file.write(str(house))

    def add_house(self):
        print("------------------------------------------------")
        print("-----Add a new house --------------------------")
        print("------------------------------------------------")
        house = House()
        print("-----Input status ------------------------------")
        house._status = Status.choose()
        print("-----Input address -----------------------------")
        house._address = input("Enter the address of the house: ")
        print("-----Input postal code -------------------------")
        house._postal_code = input("Enter the postal code of the house: ")
        print("-----Input number of rooms ---------------------")
        house._num_rooms = get_number(
            "Enter the number of rooms in the house: ", 1, 100
        )
        print("-----Input price ------------------------------")
        house._price = get_number(
            "Enter the sale/rent price of the house: ", 100, 1000000000
        )
        print("-----Input heating system ---------------------")
        house._heating = HeatingMethod.choose()
        print("-----Input energy saving options -------------")
        options = EnergyOptions.choose_input()
        house._options = options
        print("-----New house added to the database: --------")
        print(house.overview())
        print("------------------------------------------------")
        self._houses.append(house)

    def print_list(self):
        [print(house.overview()) for house in self._houses]
