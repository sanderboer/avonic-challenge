# ________________________________________________________________________
# _______/\\\\\__/\\\\\____/\\\\\\\\\_____/\\\____/\\\_____/\\\\\\\\______
# ______/\\\///\\\\\///\\\_\////////\\\___\/\\\___\/\\\___/\\\//////______
# ______\/\\\_\//\\\__\/\\\___/\\\\\\\\\\__\/\\\___\/\\\__/\\\____________
# _______\/\\\__\/\\\__\/\\\__/\\\/////\\\__\/\\\___\/\\\_\//\\\__________
# ________\/\\\__\/\\\__\/\\\_\//\\\\\\\\/\\_\//\\\\\\\\\___\///\\\\\\\\__
# _________\///___\///___\///___\////////\//___\/////////______\////////__
# ________________________________________________________________________
# Copyright 2023 MAUC architecture, research and design
#     avonic.py created on: 24.01.2023
#     Avonic Coding Challenge

import os


class House:
    def __init__(self, status, address, postal_code, num_rooms, price, heating):
        self.status = status
        self.address = address
        self.postal_code = postal_code
        self.num_rooms = num_rooms
        self.price = price
        self.heating = heating

    def __str__(self):
        return f"{self.status}: {self.address}, {self.postal_code}, {self.num_rooms} rooms, {self.price}, {self.heating}"


class HouseDatabase:
    def __init__(self, filename):
        self.filename = filename
        self.houses = []
        self.load_houses()

    def load_houses(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                num_houses = int(file.readline())
                for i in range(num_houses):
                    line = file.readline().strip().split()
                    self.houses.append(
                        House(
                            line[0],
                            line[1],
                            line[2],
                            int(line[3]),
                            int(line[4]),
                            line[5],
                        )
                    )

    def save_houses(self):
        with open(self.filename, "w") as file:
            file.write(str(len(self.houses)) + "\n")
            for house in self.houses:
                file.write(str(house) + "\n")

    def add_house(self):
        status = input(
            "Enter the status of the house (FOR SALE, SOLD, FOR RENT, RENTED): "
        )
        address = input("Enter the address of the house: ")
        postal_code = input("Enter the postal code of the house: ")
        num_rooms = int(input("Enter the number of rooms in the house: "))
        price = int(input("Enter the sale/rent price of the house: "))
        heating = input(
            "Enter the type of heating system in the house (boiler or centralheating): "
        )
        self.houses.append(
            House(status, address, postal_code, num_rooms, price, heating)
        )

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
