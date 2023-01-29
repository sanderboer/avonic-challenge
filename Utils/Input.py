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
