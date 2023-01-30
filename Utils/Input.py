import json


def repeatOnError(*exceptions):
    def checking(function):
        def checked(*args, **kwargs):
            while True:
                try:
                    result = function(*args, **kwargs)
                except exceptions as problem:
                    print("There was a problem with the input:")
                    # print(problem.__class__.__name__)
                    print(problem)
                    print("Please repeat!")
                else:
                    return result

        return checked

    return checking


@repeatOnError(ValueError)
def get_number(message, min, max, quit_option=False):
    if quit_option:
        message += "(x) to quit\n"
    choice = input(message)
    if quit_option and choice == "x":
        return -1
    value = int(choice)
    if value < min:
        raise ValueError("value is too low")
    if value > max:
        raise ValueError("value is too high")
    return value


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

    @classmethod
    def choose_optional(cls):
        use = get_number(cls.list(), 0, len(cls._choices) - 1, quit_option=True)
        if use == -1:
            return None
        else:
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
