import sys
import json
import requests
import os
import time

def read_command(args):
    #args = sys.argv
    options = ["create", "cards", "market", "transact", "add", "buy", "sell", "reveal", "stall", "drop", "undo", "start", "end", "true"]

    errors = {"Arguments": "No arguments entered.",
              "Invalid": "Invalid choice.",
              "Length": "Number of arguments entered is invalid.",
              "Type": "Argument types are invalid."}

    #assert len(args) > 1, errors["Arguments"]
    #assert args[1] in options, errors["Invalid"]

    if len(args) == 1:
        print(errors['Arguments'])
        return
    if args[1] not in options:
        print(errors['Invalid'])
        return

    # Example input: python cl.py create 5 50 200 1 50 abcd password
    # Password is temporarily mandatory.
    if args[1] == "create":
        #assert len(args) == 7, errors["Length"]
        if len(args) != 9:
            print(errors['create'])
            return

        num_players = args[2]
        min_spread, max_spread = args[3], args[4]
        card_range_low = args[5]
        card_range_high = args[6]
        game_id = args[7]
        password = args[8]
        # Todo add option
        override = args[9] if len(args) >= 10 else True

        try:
            num_players = int(num_players)
            min_spread = int(min_spread)
            max_spread = int(max_spread)
            card_range_low = int(card_range_low)
            card_range_high = int(card_range_high)
            override = bool(override)
        except:
            assert False, errors["Type"]

        msg = {'num_players': num_players,
               'min_spread': min_spread,
               'max_spread': max_spread,
               'card_range_low': card_range_low,
               'card_range_high': card_range_high,
               'game_id': game_id,
               'password': password,
               'override': override}

        confirm = requests.post(url='http://127.0.0.1:5000/GameB/createGame', json=msg)

        print(confirm.text)

    # Example input: start abcd password
    elif args[1] == "start":
        if len(args) != 4:
            print(errors['Length'])
            return
        game_id = args[2]
        password = args[3]
        msg = {'game_id': game_id, 'password': password}

        confirm = requests.post(url='http://127.0.0.1:5000/GameB/startGame', json=msg)
        if confirm.status_code == 200:
            print('Game ' + game_id + ' has been started')
            return
        print(confirm.text)
        pass
    
    # Example input: python cl.py add Alex

    elif args[1] == "add":
        #assert len(args) == 3, errors["Length"]
        if len(args) != 4:
            print(errors['Length'])
            return

        username = args[2]
        game_id = args[3]

        try:
            username = str(username)
        except:
            assert False, errors["Type"]

        msg = {'username': username, 'game_id': game_id}

        confirm = requests.post(url='http://127.0.0.1:5000/GameB/addUser', json=msg)
        if confirm.status_code == 200:
            print(username + ' has been added')
            print(confirm.text)
            return
        print(confirm.text)

    elif args[1] == "cards":
        if len(args) != 4:
            print(errors['Length'])
            return
        game_id = args[2]
        password = args[3]
        msg = {'game_id': game_id, 'password': password}
        confirm = requests.post(url='http://127.0.0.1:5000/GameB/playerCard', json=msg )
        print(confirm.text)

    # Example input: python cl.py market Alex 100 1 100 1

    elif args[1] == "market":
        #assert len(args) == 7, errors["Length"]
        if len(args) != 8:
            print(errors['Length'])
            return

        user = args[2]
        bid, ask = args[3], args[4]
        bid_lots, ask_lots = args[5], args[6]
        game_id = args[7]
        try:
            user = str(user)
            bid = int(bid)
            ask = int(ask)
            bid_lots = int(bid_lots)
            ask_lots = int(ask_lots)
        except:
            assert False, errors["Type"]

        # Check min lots
        if bid_lots < 5 or ask_lots < 5:
            bid_lots = max(bid_lots, 5)
            ask_lots = max(ask_lots, 5)
        # Check max lots
        elif bid_lots > 20 or ask_lots > 20:
            bid_lots = min(bid_lots, 20)
            ask_lots = min(ask_lots, 20)

        msg = {'user': user,
               'bid': bid,
               'bid_lots': bid_lots,
               'ask': ask,
               'ask_lots': ask_lots,
               'game_id': game_id}

        confirm = requests.post(url='http://127.0.0.1:5000/GameB/makeMarket', json=msg)
        print(confirm.text)

    # Example input: python cl.py buy Alex 3

    elif args[1] == "buy":
        #assert len(args) == 4, errors["Length"]
        if len(args) != 5:
            print(errors['Length'])
            return

        user = args[2]
        quantity = args[3]
        game_id = args[4]
        try:
            user = str(user)
            quantity = int(quantity)
        except:
            assert False, errors["Type"]

        msg = {'user': user,
               'position': "BUY",
               'quantity': quantity,
               "game_id": game_id}

        confirm = requests.post(url='http://127.0.0.1:5000/GameB/transact', json=msg)

        print(confirm.text)

    # Example input: python cl.py sell Alex 3

    elif args[1] == "sell":
        #assert len(args) == 4, errors["Length"]
        if len(args) != 5:
            print(errors['Length'])
            return

        user = args[2]
        quantity = args[3]
        game_id = args[4]
        try:
            user = str(user)
            quantity = int(quantity)
        except:
            assert False, errors["Type"]

        msg = {'user': user,
               'position': "SELL",
               'quantity': quantity,
               'game_id': game_id}
        confirm = requests.post(url='http://127.0.0.1:5000/GameB/transact', json=msg)
        print(confirm.text)

    # Example input: python cl.py stall Alex

    elif args[1] == "stall":
        if len(args) != 4:
            print(errors['Length'])
            return

        user = args[2]
        game_id = args[3]
        try:
            user = str(user)
        except:
            assert False, errors["Type"]

        msg = {'user': user, 'game_id': game_id}

        confirm = requests.post(url='http://127.0.0.1:5000/GameB/stall', json=msg)
        print(confirm.text)

    # Example input: python cl.py drop Alex

    elif args[1] == "drop":
        if len(args) != 5:
            print(errors['Length'])
            return

        user = args[2]
        game_id = args[3]
        password = args[4]
        try:
            user = str(user)
        except:
            assert False, errors["Type"]

        msg = {'user': user, 'game_id': game_id, 'password': password}

        confirm = requests.post(url='http://127.0.0.1:5000/GameB/drop', json=msg)
        print(confirm.text)

    # Example input: python cl.py undo

    elif args[1] == "undo":
        if len(args) != 4:
            print(errors['Length'])
            return

        game_id = args[2]
        password = args[3]
        msg = {'game_id': game_id, 'password': password}
        confirm = requests.post(url='http://127.0.0.1:5000/GameB/undo', json=msg)
        print(confirm.text)

    # Example input: python cl.py end
    elif args[1] == "end":
        if len(args) != 4:
            print(errors['Length'])
            return
        game_id = args[2]
        password = args[3]
        msg = {'game_id': game_id, 'password': password}
        confirm = requests.post(url='http://127.0.0.1:5000/GameB/endGame', json=msg)
        print(confirm.text)

    # Example input: python cl.py true
    elif args[1] == "true":
        if len(args) != 4:
            print(errors['Length'])
            return
        game_id = args[2]
        password = args[3]
        msg = {'game_id': game_id, 'password': password}
        confirm = requests.post(url='http://127.0.0.1:5000/GameB/trueSum', json=msg)
        print(confirm.text)

def print_beginning():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('#####################################################################')
    print('#                                                                   #')
    print('#                             Commands:                             #')
    print('# create num_players min_spread max_spread lowest_card highest_card #')
    print('#                          add player_name                          #')
    print('#                               cards                               #')
    print('#      market player_name bid_price ask_price bid_lots ask_lots     #')
    print('#                      buy player_name quantity                     #')
    print('#                     sell player_name quantity                     #')
    print('#                           stall player                            #')
    print('#                            drop player                            #')
    print('#                               undo                                #')
    print('#                               true                                #')
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
