import os


def print_opening_message():
    """the opening line and the number of attempts
    :return: None
    """
    HANGMAN_ASCII_ART = ("""
      _    _                       
     | |  | |
     | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
     |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
     | |  | | (_| | | | | (_| | | | | | | (_| | | | |
     |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                          __/ |
                         |___/ 
     """)
    max_tries = "6"
    print(HANGMAN_ASCII_ART, max_tries)


def check_valid_input(letter_guessed, old_letters_guessed):
    """
    Checks if the input from the user is correct (not greater than one, letters only,
    and the user has not guessed before)
    :param letter_guessed: The user's guess
    :param old_letters_guessed: The user's guessing list
    :type letter_guessed: str
    :type old_letters_guessed: list
    :return:true if everything is correct false if not
    :rtype: bool
    """
    letter_guessed = letter_guessed.lower()
    proper_input = (not(len(letter_guessed) > 1) and letter_guessed.isalpha() and letter_guessed not in
                    old_letters_guessed)
    return proper_input


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """Uses the check_valid_input function to check the correctness of the input
    If true adds to the guesswork list If not Prints to user X and all the letters guessed moth now in order
    :param letter_guessed: The user's guess
    :param old_letters_guessed: The user's guessing list
    :type letter_guessed: str
    :type old_letters_guessed: list
    :return:true if everything is correct false if not
    :rtype: bool
    """
    if check_valid_input(letter_guessed, old_letters_guessed) is True:
        old_letters_guessed.append(letter_guessed)
        return True
    else:
        print('x')
        old_letters_guessed.sort()
        print("-> ".join(old_letters_guessed))
        return False


def show_hidden_word(secret_word, old_letters_guessed):
    """Displays the user's guessing status so far If a letter from the word is already guessed
    the letter will be displayed if not displayed: _

    :param secret_word: The word the user needs to guess
    :param old_letters_guessed: The user's guessing list
    :type secret_word: str
    :type old_letters_guessed: list
    :return:Status screen where the user sees how many letters from the word he guessed and how much he is missing
    :rtype: str
    """
    status_screen = ''
    for i in secret_word:
        if i in old_letters_guessed:
            status_screen = status_screen + i
        else:
            status_screen = status_screen + " _ "
    return status_screen


def check_win(secret_word, old_letters_guessed):
    """Checks if the user guessed the word and won
    :param secret_word: The word the user needs to guess
    :param old_letters_guessed: The user's guessing list
    :type secret_word: str
    :type old_letters_guessed: list
    :return:true if won false if not yet
    :rtype: bool
    """
    for i in secret_word:
        if i not in old_letters_guessed:
            return False
    return True


def print_hangman(num_of_tries):
    """Prints the drawing according to the number of attempts
    :param num_of_tries: The number of times the user guessed
    :type num_of_tries: int
    :return:None
    """
    two = """    x-------x
    |
    |
    |
    |
    |"""
    tree = """    x-------x
    |       |
    |       0
    |
    |
    |"""
    four = """    x-------x
    |       |
    |       0
    |       |
    |
    |"""
    five = """    x-------x
    |       |
    |       0
    |      /|\\
    |
    |"""
    six = """    x-------x
    |      |
    |      0
    |     /|\\
    |     /
    |"""
    seven = """    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\ 
    |"""
    HANGMAN_PHOTOS = {1: two, 2: tree, 3: four, 4: five, 5: six, 6: seven}
    print(HANGMAN_PHOTOS[num_of_tries])


def choose_word(file_path, index):
    """Returns the word from the file according to the resulting index
    :param file_path:The path where the file containing the vocabulary is located
    :param index:The number of the word in the file
    :type file_path:str
    :type index: int
    :return:secret_word: The word the user needs to guess
    :rtype: str
    """
    str_user = os.path.expanduser(file_path)
    with open(str_user, "r") as str_user:
        words = str_user.readline()
    words = words.replace("\n", "")
    words = words.split(" ")
    help_list = []
    for word in words:
        if word not in help_list:
            help_list.append(word)
    index = index % len(words) - 1
    secret_word = (words[index])
    return secret_word


def main():
    old_letters_guessed = []
    secret_word = ''
    num_of_tries = 0

    print_opening_message()
    while secret_word == '':
        try:
            secret_word = choose_word(input("Enter file path: "), int(input("Enter index: ")))
        except FileNotFoundError:
            print("No path found, please try again")

    print("""\nLet’s start!
    x-------x""")
    while True:
        print("\n", show_hidden_word(secret_word, old_letters_guessed))
        while True:
            letter_guessed = input("Guess a letter:")
            if try_update_letter_guessed(letter_guessed, old_letters_guessed) is True:
                break
        if letter_guessed not in secret_word:
            num_of_tries += 1
            print_hangman(num_of_tries)
        if check_win(secret_word, old_letters_guessed) is True:
            print(f'{secret_word} \nWIN')
            break
        if num_of_tries == 6:
            print(f'{show_hidden_word(secret_word, old_letters_guessed)} \nLOSE')
            break


if __name__ == "__main__":
    main()


