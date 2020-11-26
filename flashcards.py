# Project: Flashcards  https://hyperskill.org/curriculum#about
# Stage 1/7: Stage one, card one  https://hyperskill.org/projects/127/stages/673/implement
# Stage 2/7: What's on the card?  https://hyperskill.org/projects/127/stages/674/implement
# Stage 3/7: Make it your own  https://hyperskill.org/projects/127/stages/675/implement
# Stage 4/7: A good stack  https://hyperskill.org/projects/127/stages/676/implement
# Stage 5/7: Menu, please!  https://hyperskill.org/projects/127/stages/677/implement
# Stage 6/7: Statistics  https://hyperskill.org/projects/127/stages/678/implement
# Stage 7/7: IMPORTant  https://hyperskill.org/projects/127/stages/679/implement#comment


import os.path
from io import StringIO
import argparse


# stage 7
# Argparse
# https://docs.python.org/3/howto/argparse.html
# https://docs.python.org/3/library/argparse.html


# stage 6
# create memory file (log) where all the questions and answers will be saved
memory_file = StringIO()
# memory_file.read()
# memory_file.write("")
# memory_file.getvalue()


class Card:
    '''
    creates cards and save them into the dictionary of all cards (term: [definition, statistic]),
    remove cards from the dictionary of all cards,
    increase statistics when a user enters a wrong definition,
    get the hardest card - the card with the maximum number of mistakes,
    reset statistics for all cards
    '''

    # dictionary of all cards
    all_cards_dict = {}

    def __init__(self, term, definition, stat=0):
        self.term = term
        self.definition = definition
        self.stat = stat
        # add current card to the dictionary of all cards ...
        # ... term: [definition, statistic]
        Card.all_cards_dict[self.term] = [self.definition, self.stat]

    def remove_card(c):
        ''' remove card c from the dictionary of all cards '''
        Card.all_cards_dict.pop(c, f'Can\'t remove "{c}": there is no such card.\n')

    def increase_stat(c):
        ''' increase statistic of card c in the dictionary of all cards
         when the user's answer is wrong (in test_all_cards() function) '''
        if c in Card.all_cards_dict.keys():
            Card.all_cards_dict[c][1] = int(Card.all_cards_dict[c][1])
            Card.all_cards_dict[c][1] += 1

    def get_hardest_card():
        ''' get the cards with the maximum number of wrong answers '''

        # create a list with the statistics of all cards in the dictionary
        stats_values = [int(v[1]) for k, v in Card.all_cards_dict.items()]

        # find the maximum of this list and create another list ...
        # ...containing the cards with maximum number of wrong answers
        if stats_values != [] and max(stats_values) > 0:
            hardest_cards_list = [('"' + k + '"') for k, v in Card.all_cards_dict.items() if v[1] == max(stats_values)]
            # create a string with the resulting cards (to print the result)
            hardest_cards_str = ', '.join(hardest_cards_list)
            print(f'The hardest card is {hardest_cards_str}. You have {max(stats_values)} errors answering it.')
        else:
            print("There are no cards with errors.")
        main()

    def reset_stats():
        ''' resets statistics for all the cards in the dictionary '''
        for k, v in Card.all_cards_dict.items():
            v[1] = 0
        print("Card statistics have been reset.")
        main()


def display_definition(t):
    ''' displays the definition of a card, parameter = the name (term) of the card '''
    if t in Card.all_cards_dict.keys():
        print(Card.all_cards_dict[t][0])


def validate_term():
    ''' checks if a term already exists in the dictionary of all cards
     and return the term if it does not exists in the dictionary'''
    t = input("The card:\n")
    while t in Card.all_cards_dict.keys():
        print(f'The card "{t}" already exists.\n')  # Try again:
        t = input("The card:\n")
    return t


def validate_definition():
    ''' checks if a definition exists for another term in the dictionary '''
    d = input("The definition of the card:\n")
    definitions = [v[0] for k, v in Card.all_cards_dict.items()]
    while d in definitions:
        print(f'The definition "{d}" already exists.\n')  # Try again:
        d = input("The definition of the card:\n")
    return d


def create_card(t, d, s):
    ''' creates a card with the validated term, definition and statistic = 0 by default
    using the constructor of the Card class '''
    Card(t, d, s)


def test_all_cards_in_dict():
    ''' tests all cards in the dictionary of all cards '''

    # n = len(Card.all_cards)  # stage 3 / 4
    number_of_tests = int(input(f"How many times to ask?"))
    keys_list = [k for k in Card.all_cards_dict.keys()]
    n = len(keys_list)
    # test all the terms for the number of times entered by the user ...
    # ... if the dictionary of cards is not empty
    if n:
        for i in range(number_of_tests):
            test_term = keys_list[i % n]
            answer = input(f'Print the definition of "{test_term}":\n')
            # create a list with the definitions of all terms in the dictionary
            definitions = [v[0] for k, v in Card.all_cards_dict.items()]

            if answer == Card.all_cards_dict[test_term][0]:
                print(f"Correct!\n")
            # if user answer is a definition for another term, print that correct
            # increase term statistics if the answer is wrong
            elif answer in definitions:
                existing_term = [k for k, v in Card.all_cards_dict.items() if v[0] == answer]
                print(f'Wrong. The right answer is "{Card.all_cards_dict[test_term][0]}", \
    but your definition is correct for "{existing_term[0]}".\n')
                Card.increase_stat(test_term)
            else:
                print(f'Wrong. The right answer is "{Card.all_cards_dict[test_term][0]}".')
                Card.increase_stat(test_term)

            # save questions and answers to the memory file (log)
            memory_file.write(f"{test_term} {answer}")


def remove_card():
    ''' removes card from the dictionary of all cards using the .remove_card() method of the Card class '''
    c = input("Which card?\n")
    if c in Card.all_cards_dict.keys():
        Card.remove_card(c)
        print("The card has been removed.\n")
    else:
        print(f'Can\'t remove "{c}": there is no such card.\n')
    main()


def export_cards():
    ''' exports the cards in the dictionary (term definition statistic)
        to the user input file '''
    file_name = input("File name:\n")
    with open(f"{file_name}", "w+") as f:
        for k, v in Card.all_cards_dict.items():
            f.write(f"{k} {v[0]} {v[1]}\n")
    print(f"{len(Card.all_cards_dict.keys())} cards have been saved.\n")
    main()


def import_cards():
    ''' imports the cards from the user input file (each card on one line: term definition statistic)
        to the dictionary of all cards by creating a new card, using the Card class '''
    file_name = input("File name:\n")
    if not os.path.exists(file_name):
        print("File not found.\n")
    else:
        with open(file_name, "r") as f:
            for line in f:
                create_card(line.split()[0], line.split()[1], line.split()[2])
        # find the number of cards that have been added
        cards_number = len(Card.all_cards_dict.keys())
        print(f"{cards_number} cards have been loaded.")
    main()


def display_all_cards():
    ''' display all cards in the dictionary (in case it will be necessary) '''
    for k, v in Card.all_cards_dict.items():
        print(k + " : " + v)
    print("\n")
    main()


def save_log():
    ''' saves the log (questions and user answers) from the memory file to the user input file'''
    file_name = input("File name:\n")
    with open(file_name, "w+") as log:
        for line in memory_file:
            log.write(line)
    print("The log has been saved.\n")


def display_hardest_card():
    ''' display the card with maximum number of mistakes in statistics using the
     .get_hardest_card() method of the Card class '''
    Card.get_hardest_card()


def import_arg(file_name):
    ''' when provided with command-line arguments,
        if --import_from=FILE is passed, read the initial card set from the external file
        and print "n cards have been loaded" as the first line of the output...
        ... if such an argument is not provided, the initial should initially be empty ...
        ... and no message about card loading should be output '''
    if not os.path.exists(file_name):
        print("File not found.\n")
    else:
        # save the cards from the import file into the dictionary of all cards
        with open(file_name, "r") as f:
            for line in f:
                create_card(line.split()[0], line.split()[1], line.split()[2])
        cards_number = len(Card.all_cards_dict.keys())
        print(f"{cards_number} cards have been loaded.")


def export_arg(file_name):
    ''' when provided command-line arguments,
        if --export_to=FILE is passed, write all cards that are in program memory into this file
        after the user has entered exit '''
    with open(f"{file_name}", "w+") as f:
        for k, v in Card.all_cards_dict.items():
            f.write(f"{k} {v[0]} {v[1]}\n")
    print(f"{len(Card.all_cards_dict.keys())} cards have been saved.\n")


def main():
    ''' main function: output the menu and execute actions according with the user choice '''

    # stage 6
    choice = input("Input the action (add, remove, import, export, \
ask, exit, log, hardest card, reset stats):\n")

    if choice == "add":
        term = validate_term()
        definition = validate_definition()
        create_card(term, definition, 0)
        print(f'The pair ("{term}":"{definition}") has been added.\n')
    elif choice == "remove":
        remove_card()
    elif choice == "import":
        import_cards()
    elif choice == "export":
        export_cards()
    elif choice == "ask":
        test_all_cards_in_dict()
    elif choice == "display cards":
        display_all_cards()
    elif choice == "log":
        save_log()
    elif choice == "hardest card":
        display_hardest_card()
    elif choice == "reset stats":
        Card.reset_stats()
    elif choice == "exit":
        print("Bye bye!")
        export_arg(args.export_to)  # export_arg(params['export_to'])
        exit()

    main()


# stage 7
# create an instance of the argument parser
parser = argparse.ArgumentParser()
# add expected argument by using the parser's method .add_argument()
parser.add_argument('--import_from')  # , type=str, action="store", dest="import_from")
parser.add_argument('--export_to')  # , type=str, action="store", dest="export_to")

# documentation: args = parser.parse_args(['-import_fromval', '-export_toval'])
# documentation: params = vars(args)  # convert arguments to dictionary
# documentation: import_arg(params['import_from'])

# parse the argument by means of .parse_args() method
args = parser.parse_args()

# if --import_from argument is passed, read the initial card set from the external file ...
# ... and print a message as the first line of the output, using the function import_arg()
if args.import_from:
    import_arg(args.import_from)

if __name__ == "__main__":
    main()
