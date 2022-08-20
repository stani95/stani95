import random
import bisect
import itertools
import copy

def play_game(bet, balance, verbose=True, randomize=True, reel_indexes=(0, 0, 0, 0)):
    if balance < bet:
        print("Unsufficient balance!")
        return balance

    balance -= bet

    if randomize is True:
        random_reels = [reel_values[bisect.bisect(start, random.randint(1, total_odds)) - 1] for i in range(3)]
    else:
        random_reels = [reel_values[reel_indexes[i]] for i in range(3)]

    reels = [list(i) for i in zip(*random_reels)]

    win = 0
    if len(set(reels[0])) == 1:
        winning_symbol = symbols[reels[0][0]]
        win += bet*paytable[(3, winning_symbol)]
    if len(set(reels[1])) == 1:
        winning_symbol = symbols[reels[1][0]]
        win += bet*paytable[(3, winning_symbol)]
    if len(set(reels[2])) == 1:
        winning_symbol = symbols[reels[2][0]]
        win += bet*paytable[(3, winning_symbol)]

    if reels == [[3, 3, 3], [3, 3, 3], [3, 3, 3]]:
        win -= 3*bet*paytable[(3, 'seven')]
        win += bet*jackpot_multiplier
        if verbose:
            print("CONGRATULATIONS! JACKPOT HIT!!!!")

    balance += win

    if verbose:
        print(reels[0])
        print(reels[1])
        print(reels[2])
        print()
        print(f"BET: {bet}")
        print(f"WIN: {win}")
        print(f"NEW BALANCE: {balance}")
        print()
        print("---------")
        print()

    return balance

def increment_position(position):
    if position[3] != reel_odds[position[0]]*reel_odds[position[1]]*reel_odds[position[2]] - 1:
        position[3] += 1
    else:
        position[3] = 0
        if position[2] != 27:
            position[2] += 1
        elif position[1] != 27:
            position[1] += 1
            position[2] = 0
        elif position[0] != 27:
            position[0] += 1
            position[1] = 0
            position[2] = 0
        else:
            return True
    return False

if __name__ == "__main__":

    symbols = ['cherry', 'lemon', 'plum', 'seven']

    paytable = {
        (3, 'cherry'): 3,
        (3, 'lemon'): 3,
        (3, 'plum'): 5,
        (3, 'seven'): 15,
    }

    jackpot_multiplier = 100

    reel_values = {
        0: [0,0,0],
        1: [1,1,1],
        2: [2,2,2],
        3: [3,3,3],
        4: [0,0,1],
        5: [1,0,0],
        6: [0,0,2],
        7: [2,0,0],
        8: [0,0,3],
        9: [3,0,0],
        10: [1,1,0],
        11: [0,1,1],
        12: [1,1,2],
        13: [2,1,1],
        14: [1,1,3],
        15: [3,1,1],
        16: [2,2,0],
        17: [0,2,2],
        18: [2,2,1],
        19: [1,2,2],
        20: [2,2,3],
        21: [3,2,2],
        22: [3,3,0],
        23: [0,3,3],
        24: [3,3,1],
        25: [1,3,3],
        26: [3,3,2],
        27: [2,3,3]
    }

    reel_odds = {
        0: 6,
        1: 6,
        2: 6,
        3: 1,
        4: 2,
        5: 2,
        6: 2,
        7: 2,
        8: 2,
        9: 2,
        10: 2,
        11: 2,
        12: 2,
        13: 2,
        14: 2,
        15: 2,
        16: 2,
        17: 2,
        18: 2,
        19: 2,
        20: 2,
        21: 2,
        22: 2,
        23: 2,
        24: 2,
        25: 2,
        26: 2,
        27: 2
    }

    total_odds = sum([v for v in reel_odds.values()])
    current_value = 0
    reel_rng_matrix = {}
    start = []
    for k,v in reel_odds.items():
        current_value += v
        reel_rng_matrix[k] = [current_value - v + 1, current_value]
        start.append(current_value - v + 1)

    in_text = "Please enter 0 to play, 1 for theoretical RTP, 2 for simulation, 3 for long simulation: "
    what_to_do = -1
    while what_to_do not in [0,1,2,3]:
        what_to_do = int(input(in_text))

    # User playing
    if what_to_do == 0:
        balance = int(input("Please enter amount of money to deposit: "))
        bet = int(input("Please enter amount of money to bet: "))

        while True:
            user_input = input("Press Enter to spin. Press 'x' to exit. --> ")
            if user_input == '':
                balance = play_game(bet, balance)
            elif user_input == 'x':
                print(f"You exit with balance {balance}")
                break

    # Obtain theoretical RTP
    elif what_to_do == 1:
        initial_balance = 100000000
        balance = copy.deepcopy(initial_balance)
        position = [0,0,0,0]
        num_spins = sum([i[0]*i[1]*i[2] for i in itertools.product(list(reel_odds.values()), repeat=3)])
        stop = False
        while stop is False:
            balance = play_game(1, balance, verbose=False, randomize=False, reel_indexes=tuple(position))
            stop = increment_position(position)
        print(f"RTP = {100*(balance+num_spins-initial_balance)/num_spins}%")

    # Simulation
    elif what_to_do == 2:
        initial_balance = 200000      # $200k initial balance
        num_spins = 1000000           # 1M number of spins
        bet = 1                       # $1 bet amount
        balance = copy.deepcopy(initial_balance)
        for i in range(num_spins):
            if i%50000 == 0:          # Print balance after every 50k spins
                print(f"Current balance = ${balance}")
            balance = play_game(bet, balance, verbose=False)
        print(f"RTP = {100*(balance+num_spins-initial_balance)/num_spins}%")

    # Long simulation
    elif what_to_do == 3:
        initial_balance = 1000000      # $1M initial balance
        num_spins = 10000000           # 10M number of spins
        bet = 1                        # $1 bet amount
        balance = copy.deepcopy(initial_balance)
        for i in range(num_spins):
            if i%100000 == 0:          # Print balance after every 100k spins
                print(f"Current balance = ${balance}")
            balance = play_game(bet, balance, verbose=False)
        print(f"RTP = {100*(balance+num_spins-initial_balance)/num_spins}%")
