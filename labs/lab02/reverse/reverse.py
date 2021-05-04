def reverse_words(string_list):
    new_string = []
    for string in string_list:
        words = string.split(' ')
        reversed_string = ' '.join(reversed(words))
        new_string.append(reversed_string)
    return new_string

if __name__ == "__main__":
    print(reverse_words(["Hello World", "I am here"]))
    # it should print ['World Hello', 'here am I']
