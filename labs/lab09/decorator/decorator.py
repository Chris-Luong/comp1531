import sys

MESSAGE_LIST = []

def authorise(function):
    """ Alternative solution
    def wrapper(*args, **kwargs):
        authToken = args[0]
        if authToken != "CrocodileLikesStrawberries":
            raise ValueError("Invalid authentication")
        return function(*args[1:])
    return wrapper
    """
    def wrapper(auth_token, *args, **kwargs):
        if auth_token != 'CrocodileLikesStrawberries':
            raise Exception('Invalid token')
        return function(*args, **kwargs)
    return wrapper


@authorise
def get_message():
    return MESSAGE_LIST

@authorise
def add_message(msg):
    global MESSAGE_LIST
    MESSAGE_LIST.append(msg)

if __name__ == '__main__':
    authToken = ""
    if len(sys.argv) == 2:
        authToken = sys.argv[1]

    add_message(authToken, "Hello")
    add_message(authToken, "How")
    add_message(authToken, "Are")
    add_message(authToken, "You?")
    print(get_message(authToken))
