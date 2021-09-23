import random
import os
import json

from pyfiglet import Figlet
from termcolor import colored
from colorama import Fore

DB_LOCATION = os.path.join(os.path.dirname(__file__), 'db.json')

def pushToDatabase(data):
    with open(DB_LOCATION, 'w') as file:
        json.dump(data, file, ensure_ascii=False)


def readFromDatabase():
    if os.path.exists(DB_LOCATION):
        return json.loads(open(DB_LOCATION, 'r').read() or '[]')

    return []


def clear():
    # check and make call for specific operating system
    os.system('clear' if os.name == 'posix' else 'cls')


templates = Figlet(font='slant')
print(colored(templates.renderText("   Guess   the \n    number"), 'green'))

print(f"{Fore.YELLOW}Welcome to the game of number guessing...\n"
      "Lets see the rules\n"
      "1) Choose the range in which a random number will be chosen\n"
      "2) For every wrong guess we deduct 5 from Score\n"
      "3) Total score is 100\n"
      "4) You loose if score is below 20\n\n"
      f"{Fore.YELLOW}Enjoy the game!!\n")

name = input(f"{Fore.GREEN}Please Enter your name: ")
print(f"{Fore.GREEN}Welcome to my Number game, " + name)


def GuessNumberGame():
    try:
        lower_limit = int(input(f"{Fore.GREEN}Enter the Lower Limit: "))
        upper_limit = int(input(f"{Fore.GREEN}Enter the Upper Limit: "))

        random_number = random.randint(lower_limit, upper_limit)

        print(f"{Fore.GREEN}You will have to choose a number between ", lower_limit, " and ", upper_limit)

        i = 0
        total_score = 100
        r = 1
        while total_score - i >= 20:

            try:
                user_number = int(input(f'{Fore.GREEN}\n\nGuess the number: '))

                if user_number < random_number:
                    clear()
                    i += 5
                    print(name + f"{Fore.GREEN}, My number is greater than your guessed number")
                    print(f"{Fore.GREEN}Your Score: " + str(total_score - i))

                elif user_number > random_number:
                    clear()
                    i += 5
                    print(name + f"{Fore.GREEN}, My number is less than your guessed number")
                    print(f"{Fore.GREEN}Your Score: " + str(total_score - i))

                elif user_number == random_number:
                    print(f"{Fore.GREEN}Your Score: " + str(total_score - i))
                    print(f"{Fore.MAGENTA}\nDear " + name +
                          f"{Fore.MAGENTA}!!"  f"{Fore.MAGENTA}\nCongratulations You have guessed the correct number!!")

                    r = 0
                    break

                else:
                    print(f"{Fore.RED}This is an invalid number. Please try again")
                    print(f"{Fore.GREEN}Your Score: " + str(total_score - i))

                    continue

            except ValueError:
                print("\nValue Error!!")

        if r == 1:
            print(f"{Fore.RED}Sorry you lost the game!!")

            print(f"{Fore.GREEN}My number was = " + str(random_number))

        loadScore(name, total_score - i)

    except ValueError:
        print("\nValue Error!! Please Enter Integer Value")


def loadScore(name, score):
    new_score = {
        'name': name,
        'score': score
    }
    all_scores = readFromDatabase()
    all_scores.append(new_score)
    pushToDatabase(all_scores)


def readTopScore():
    all_scores = sorted(readFromDatabase(),
                        key=lambda i: i['score'], reverse=True)

    print(f"{Fore.MAGENTA}Top 5 scorers:")
    for score in all_scores[:5]:
        print(f"{Fore.MAGENTA}{score['name']}: {score['score']}")


def main():
    GuessNumberGame()

    while True:
        another_game = input(f"{Fore.RED}Do you wish to play again? (y/n): ")
        if another_game == "y":
            GuessNumberGame()

        else:
            break

    readTopScore()


main()
print(f"{Fore.GREEN}\nEnd of the Game! Thank you for playing!")



