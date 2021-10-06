import random

user_wins = 0
computer_wins = 0
options = ["paper", "rock", "scissor"]

while True:
    user_input = input("Eneter the option paper, scissor, rock or press 'Q' for exit : ").lower()
    if user_input == 'q':
        break
    if user_input not in options:
        continue

    random_number = random.randint(0, 2)
    computer_pick = options[random_number]

    print("computer_pick:", computer_pick + '.')

    if user_input == 'paper' and computer_pick == 'rock':
        print("You win!")
        user_wins += 1
    elif user_input == 'rock' and computer_pick == 'scissor':
        print("You win!")
        user_wins += 1
    elif user_input == 'scissor' and computer_pick == 'paper':
        print("You win!")
        user_wins += 1
    elif user_input == computer_pick:
        print("Match draw \n no points")
    else:
        print("compter win!")
        computer_wins += 1

print("Your Wins:", user_wins, 'times')
print("computer Wins:", computer_wins, 'times')
print("Goodbuy!")






