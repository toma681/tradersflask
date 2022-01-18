import sys
import json
import requests
import os
import time

def read_command(args):
    #args = sys.argv
    options = ["create", "add", "market", "play", "drop", "undo", "end"]

    errors = {"Arguments": "No arguments entered.",
              "Invalid": "Invalid choice.",
              "Length": "Number of arguments entered is invalid.",
              "Type": "Argument types are invalid.",
              "Spread": "Your spreads do not match the rule"}

    if len(args) == 1:
        print(errors['Arguments'])
        return
    if args[1] not in options:
        print(errors['Invalid'])
        return

    # Example input: python cl.py create 3 10 20 30

    if args[1] == "create":
        if len(args) != 6:
            print(errors['create'])
            return

        num_players = args[2]
        q1_value = args[3]
        q2_value = args[4]
        q3_value = args[5]
        # Todo add option
        override = args[6] if len(args) >= 7 else True

        try:
            num_players = int(num_players)
            q1_value = int(q1_value)
            q2_value = int(q2_value)
            q3_value = int(q3_value)
            override = bool(override)
        except:
            assert False, errors["Type"]

        msg = {"true_values": [q1_value, q2_value, q3_value],
               "num_players": num_players,
               'override': override}

        confirm = requests.post(url='http://127.0.0.1:5000/GameA/createGame', json=msg)

        print(confirm.text)

    # Example input: python cl.py add Alex Bob Charlie

    elif args[1] == "add":
        if len(args) == 2:
            print(errors['Length'])
            return

        num_args = len(args)
        ret = []

        try:
            for i in range(2, num_args):
                username = str(args[i])
                ret.append(username)
        except:
            assert False, errors["Type"]

        usernames = " ".join(ret)
        msg = {'usernames': usernames}

        confirm = requests.post(url='http://127.0.0.1:5000/GameA/addName', json=msg)
        print(confirm.text)

    # Example input: python cl.py market Alex q1 5 10 2 2 q2 6 8 5 5 q3 100 110 17 18

    elif args[1] == "market":
        if len(args) != 18:
            print(errors['Length'])
            return

        user = args[2]
        q1_bid, q1_ask, q1_bid_lots, q1_ask_lots = args[4], args[5], args[6], args[7]
        q2_bid, q2_ask, q2_bid_lots, q2_ask_lots = args[9], args[10], args[11], args[12]
        q3_bid, q3_ask, q3_bid_lots, q3_ask_lots = args[14], args[15], args[16], args[17]

        try:
            user = str(user)
            q1_bid, q1_ask, q1_bid_lots, q1_ask_lots = round(float(q1_bid), 1), round(float(q1_ask), 1), int(
                q1_bid_lots), int(q1_ask_lots)
            q2_bid, q2_ask, q2_bid_lots, q2_ask_lots = round(float(q2_bid), 1), round(float(q2_ask), 1), int(
                q2_bid_lots), int(q2_ask_lots)
            q3_bid, q3_ask, q3_bid_lots, q3_ask_lots = round(float(q3_bid), 1), round(float(q3_ask), 1), int(
                q3_bid_lots), int(q3_ask_lots)
        except:
            assert False, errors["Type"]

        q1_spread = q1_ask - q1_bid
        q2_spread = q2_ask - q2_bid
        q3_spread = q3_ask - q3_bid

        if set([q1_spread, q2_spread, q3_spread]) != set([2, 5, 10]):
            print(errors["Spread"])
            return

        # Minimum lots
        if q1_bid_lots < 5 or q1_ask_lots < 5 or q2_bid_lots < 5 or q2_ask_lots < 5 or q3_bid_lots < 5 or q3_ask_lots < 5:
            q1_bid_lots = max(q1_bid_lots, 5)
            q1_ask_lots = max(q1_ask_lots, 5)
            q2_bid_lots = max(q2_bid_lots, 5)
            q2_ask_lots = max(q2_ask_lots, 5)
            q3_bid_lots = max(q3_bid_lots, 5)
            q3_ask_lots = max(q3_ask_lots, 5)
        # Maximum lots
        elif q1_bid_lots > 20 or q1_ask_lots > 20 or q2_bid_lots > 20 or q2_ask_lots > 20 or q3_bid_lots > 20 or q3_ask_lots > 20:
            q1_bid_lots = min(q1_bid_lots, 20)
            q1_ask_lots = min(q1_ask_lots, 20)
            q2_bid_lots = min(q2_bid_lots, 20)
            q2_ask_lots = min(q2_ask_lots, 20)
            q3_bid_lots = min(q3_bid_lots, 20)
            q3_ask_lots = min(q3_ask_lots, 20)

        msg = {
                "user": user,
                "q1_bid": q1_bid,
                "q1_ask": q1_ask,
                "q1_bid_size": q1_bid_lots,
                "q1_ask_size": q1_ask_lots,
                "q2_bid": q2_bid,
                "q2_ask": q2_ask,
                "q2_bid_size": q2_bid_lots,
                "q2_ask_size": q2_ask_lots,
                "q3_bid": q3_bid,
                "q3_ask": q3_ask,
                "q3_bid_size": q3_bid_lots,
                "q3_ask_size": q3_ask_lots
        }

        confirm = requests.post(url='http://127.0.0.1:5000/GameA/makeMarket', json=msg)

        print(confirm.text)

    # Example input: python cl.py drop Alex

    elif args[1] == "drop":
        if len(args) != 3:
            print(errors['Length'])
            return

        user = args[2]
        try:
            user = str(user)
        except:
            assert False, errors["Type"]

        msg = {
                "user": user,
                "q1_bid": 0,
                "q1_ask": 0,
                "q1_bid_size": 0,
                "q1_ask_size": 0,
                "q2_bid": 0,
                "q2_ask": 0,
                "q2_bid_size": 0,
                "q2_ask_size": 0,
                "q3_bid": 0,
                "q3_ask": 0,
                "q3_bid_size": 0,
                "q3_ask_size": 0
        }

        confirm = requests.post(url='http://127.0.0.1:5000/GameA/makeMarket', json=msg)

        print(confirm.text)

    # Example input: python cl.py play

    elif args[1] == "play":
        if len(args) != 2:
            print(errors['Length'])
            return

        confirm = requests.post(url='http://127.0.0.1:5000/GameA/playRound')
        print(confirm.text)

    # Example input: python cl.py undo

    elif args[1] == "undo":
        if len(args) != 2:
            print(errors['Length'])
            return

        confirm = requests.post(url='http://127.0.0.1:5000/GameA/undo')
        print(confirm.text)

    # Example input: python cl.py end
    elif args[1] == "end":
        if len(args) != 2:
            print(errors['Length'])
            return

        confirm = requests.post(url='http://127.0.0.1:5000/GameA/end')
        print(confirm.text)


def print_beginning():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('#####################################################################')
    print('#                                                                   #')
    print('#                             Commands:                             #')
    print('#          create num_players q1_value q2_value q3_value            #')
    print('#                add player_name1 player_name2 etc                  #')
    print('#  market name q1 1b 1a 1bL 1aL q2 2b 2a 2bL 2aL q3 3b 3a 3bL 3aL   #')
    print('#                               play                                #')
    print('#                            drop player                            #')
    print('#                               undo                                #')
    print('#                                end                                #')
    print('#                                                                   #')
    print('#####################################################################')

def find_remaining_time(start):
    elapsed_time = int(time.time() - start)
    minutes = str(elapsed_time//60)
    minutes = '0'*(2-len(minutes)) + minutes
    seconds = str(elapsed_time%60)
    seconds = '0'*(2-len(seconds)) + seconds
    return 'Time Elapsed: ' + minutes + ':' + seconds

def loop():
    print_beginning()
    start = time.time()
    playing = True
    while playing:
        command = input('>>> ')
        args = command.split(' ')
        args.insert(0, 'placeholder')
        read_command(args)
        print(find_remaining_time(start))
        if command == 'reveal':
            playing=False

if __name__ == "__main__":
    loop()
