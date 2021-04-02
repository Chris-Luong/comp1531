from isbn import isValid
from socket import socket, AF_INET, SOCK_STREAM

def ISBNValidator(function):
    pass

@ISBNValidator
def sendToPublisher(isbn):
    """
    Pretend to send ISBN to the publisher via the Internet by sending it to localhost.
    Don't worry about any of the code below, just something cool you can do with Python, but please put your focus on the use of decorator here.
    """
    new_socket = socket(AF_INET, SOCK_STREAM)
    new_socket.connect(('localhost', 8000))
    new_socket.send(isbn.encode())
    print('Sent ISBN to the publisher!')

@ISBNValidator
def printBook(isbn):
    """
    Print out the book along with ISBN.
    """
    BOOK_NAME = 'Legend of Hayden'
    print(f'Printing book <{BOOK_NAME}>\nISBN: {isbn}')

if __name__ == "__main__":
    # Get the ISBN
    isbn = input('What is the ISBN? ')

    # Call the functions that uses ISBN
    sendToPublisher(isbn)
    printBook(isbn)