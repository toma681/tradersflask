import enum
from flask import Flask, json, request, jsonify, session, Response, Blueprint
from .game import Game
from collections import OrderedDict
import sys

from .cache import cache
from .cache_api import cache as user_cache

gameB_api = Blueprint('gameB_api', __name__)

# TODO Configure for multiple games and with multiple players
@gameB_api.before_app_first_request
@cache.cached(timeout=300, key_prefix='game_users')
def create_game_users():
    return []

@gameB_api.before_app_first_request
@cache.cached(timeout=300, key_prefix='original_game_users')
def create_original_game_users():
    return []

@gameB_api.route('/createGame', methods=['POST'])
def create_game():
    """
    Creates game. Returns the password of the game, which is no-matter-what set to "flask_passcode" for now.
    {
        "num_players": 6,
        "min_spread": 4,
        "max_spread": 40,
        "card_range_low": 1,
        "card_range_high": 50,
        "game_id": "abcd",
        "password": "pwd"
    }
    """
    game_id = request.json['game_id']
    game = cache.get(game_id)
    # password = request.json['password']
    # if password is None:
    #     password = ""
    password = "flask_passcode"
    new_game = Game(num_players=request.json['num_players'], min_spread=request.json['min_spread'], max_spread=request.json['max_spread'], card_range_low=request.json['card_range_low'], card_range_high=request.json['card_range_high'], password=password)
    if request.json.get("override", False):
        cache.set(game_id, new_game)
    elif game is not None:
        return Response('Game already created with game_id: ' + game_id, status=500)
    cache.set(game_id, new_game)
    print(repr(cache))
    print(repr(new_game))
    return Response('Game created.', status=200)

@gameB_api.route('/addUser', methods=['POST'])
def add_user():
    '''
    Adds user to game.
    {
        'username': string,
        "game_id": "abcd"
    }. This will be abbreviated to user_data going forward.

    200 if added or if already in game.
    400/403 for user handling (see verify_user) or 400 if exceeds max users in game.
    '''
    # Verification
    # users = user_cache.get('users')
    # verification = verify_user(request.json)
    # if verification.status_code != 200:
    #     return verification

    # Don't re-add user if already in game
    # print(cache)
    game_id = request.json['game_id']
    game = cache.get(game_id)
    username = request.json['username']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    game_users = game.players
    for user in game_users:
        if user == username:
            return Response('You are already in this game', status=500)
    # Check user limit
    if len(game_users) >= game.get_num_players():
        return Response("Exceeds max users", status=400)

    # Add user
    game.add_user(username)
    cache.set(game_id, game)
    print(game_users)
    res = [key for key, value in game_users.items()]
    print([key for key, value in game_users.items()])
    return Response(res, status=200)

# TODO
def verify_get_user_pos(user_data, game_id):
    '''
    Helper function used to verify user and get user position, 
    for setter functions (POST requests).
    '''
    game = cache.get(game_id)
    game_users = game.players
    # Get game user position
    if len(game_users) != game.get_num_players():
        return Response('Game is not full yet', status=400)
    position = -1
    users = OrderedDict(zip(sorted(game.all_players), game_users))
    for key, value in users.items():
        if user_data == value:
            position = key
            break
    if position == -1:
        return Response('User not in game', status=400)

    # Verification
    # users = user_cache.get('users')
    # verification = verify_user(user_data)
    # if verification.status_code != 200:
    #     return verification
    
    return position

@gameB_api.route("/makeMarket", methods=['POST'])
def make_market():
    '''
    {
        "user": user_data,
        "bid": 5,
        "bid_lots": 1,
        "ask": 8,
        "ask_lots": 1,
        "game_id": "abcd"
    }

    Ends turn
    '''
    game_id = request.json['game_id']
    game = cache.get(game_id)
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if game.status != 1:
        return Response('Game with game_id: ' + game_id + ' has not been started.', status=401)
    try:
        data = request.json
        user_data = data['user']
        bid = int(data['bid'])
        bid_lots = int(data['bid_lots'])
        ask = int(data['ask'])
        ask_lots = int(data['ask_lots'])
    except:
        return Response(status=400)

    # position = verify_get_user_pos(user_data, game_id)
    # if isinstance(position, Response):
    #     return position
    try:
        # valid_turn = verify_turn(game, user_data)
        # print(user_data)
        valid_turn = True
        if valid_turn:
            response_str = game.make_market(game.players[user_data], bid, bid_lots, ask, ask_lots)
        else:
            return Response("It is not " + user_data + "'s turn.", status=400)
    except Exception as e:
        return Response(str(e), status=400)

    cache.set(game_id, game)
    return Response(response_str, status=200)

def verify_turn(game, player):
    if len(game.players) > 0:
        my_id = game.players[player].player_id
        print(game.get_current_player())
        return game.get_current_player() == my_id
    return False
    
@gameB_api.route("/transact", methods=['POST'])
def transact():
    '''
    Player makes a transaction. Max one transaction per turn. Will error after that.
    {
        "user": user_data,
        'position': <'BUY','SELL'>,
        'quantity': int
    }
    '''

    # Uncache game
    game_id = request.json['game_id']
    game = cache.get(game_id)
    print("Game_id:", game_id)
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if game.status != 1:
        return Response('Game with game_id: ' + game_id + ' has not been started.', status=401)
    # Grab data
    try:
        data = request.json
        user_data = data['user']
        position = str(data['position'])
        quantity = int(data['quantity'])
        # Verify
        if not (position == 'BUY' or position == 'SELL'):
            raise Exception("Incorrect string value for position")
    except Exception as e:
        return Response(str(e), status=400)
    print(data)
    if quantity < 0:
        return Response('Negative quantities not allowed.', status=400) 
    # valid_turn = verify_turn(game, user_data)
    # user_position = verify_get_user_pos(user_data)
    # if isinstance(user_position, Response):
    #     return user_position
    valid_turn = True
    if valid_turn:
        # Perform action
        try:
            response_str = game.transact(game.players[user_data], position, quantity)
        except Exception as e:
            return Response(str(e), status=400) 
    else:
        return Response("It is not " + user_data + "'s term.", status=400)

    cache.set(game_id, game)
    return Response(response_str, status=200)

@gameB_api.route('/stall', methods=['POST'])
def stall():
    """
    Action to prevent players from stalling
    """
    game_id = request.json['game_id']
    game = cache.get(game_id)

    try:
        data = request.json
        user = data['user']
        user = str(user)
    except Exception as e:
        return Response(str(e), status=400)

    valid_turn = verify_turn(game, user)
    
    # user_position = verify_get_user_pos(user)
    # if isinstance(user_position, Response):
    #     return user_position

    if valid_turn:
        try:
            response_str = game.stall(user)
        except Exception as e:
            return Response(str(e), status=400)
    else:
        return Response("It is not " + user + "'s term.", status=400)
    # Perform action
    # Recache game
    cache.set(game_id, game)

    return Response(response_str, status=500)

@gameB_api.route('/drop', methods=['POST'])
def drop():
    """
    Drop player
    """
    game_id = request.json['game_id']
    game = cache.get(game_id)
    password = request.json['password']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if password != game.password:
        return Response('Incorrect password for game with game_id: ' + game_id, status=401)
    if game.status == 2:
        return Response('Game with game_id: ' + game_id + ' has already ended.', status=401)
    game_users = game.players

    try:
        data = request.json
        user = data['user']
        response_str = game.drop(user)
    except Exception as e:
        return Response(str(e), status=400)
    if game.num_players < 2:
        game.set_true_pnl()
        game.status = 2
        cache.set(game_id, game)
        return Response("Less than 2 players in the game, so it has been ended.", status=200)
    # Recache game
    cache.set(game_id, game)
    return Response(response_str, status=200)

@gameB_api.route('/undo', methods=['POST'])
def undo():
    """
    Undo last action
    """
    game_id = request.json['game_id']
    game = cache.get(game_id)

    # Perform action
    try:
        game = game.undo()
    except Exception as e:
        return Response(str(e), status=400)

    # Recache game
    cache.set(game_id, game)

    return Response("Undo", status=200)

@gameB_api.route('/playerPositions', methods=['POST'])
def get_player_positions():
    """
    Gets all players' positions

    :return: (json) {"0": -1, "1": 1} (str) Key: Player ID, (int) Value: Position
    """
    game_id = request.json['game_id']
    game = cache.get(game_id)
    password = request.json['password']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if password != game.password:
        return Response('Incorrect password for game with game_id: ' + game_id, status=401)
    if game.status == 2:
        return Response('Game with game_id: ' + game_id + ' has already ended.', status=401)
    response = game.get_all_players_position()
    return Response(json.dumps(response), status=200)

@gameB_api.route("/revealedCards", methods=['POST'])
def get_revealed_cards():
    game_id = request.json['game_id']
    game = cache.get(game_id)
    password = request.json['password']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if password != game.password:
        return Response('Incorrect password for game with game_id: ' + game_id, status=401)
    response = game.get_revealed_cards()
    return Response(json.dumps(response), status=200)

@gameB_api.route("/truePnl", methods=['POST'])
def get_true_pnl():
    game_id = request.json['game_id']
    game = cache.get(game_id)
    password = request.json['password']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if password != game.password:
        return Response('Incorrect password for game with game_id: ' + game_id, status=401)
    if game.status != 2:
        return Response('Game with game_id: ' + game_id + ' not over yet.', status=401)
    response = game.get_true_pnl()
    return Response(json.dumps(response), status=200)

@gameB_api.route("/endGame", methods=['POST'])
def end_game():
    game_id = request.json['game_id']
    game = cache.get(game_id)
    password = request.json['password']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if password != game.password:
        return Response('Incorrect password for game with game_id: ' + game_id, status=401)
    if game.status != 1:
        return Response('Game with game_id: ' + game_id + ' is not in progress.', status=409)
    game.set_true_pnl()
    game.status = 2
    cache.set(game_id, game)
    return Response("End Game", status=200)

@gameB_api.route("/turnList", methods=['POST'])
def get_turn_list():
    game_id = request.json['game_id']
    game = cache.get(game_id)
    password = request.json['password']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if password != game.password:
        return Response('Incorrect password for game with game_id: ' + game_id, status=401)
    if game.status == 2:
        return Response('Game with game_id: ' + game_id + ' has already ended.', status=401)
    transact_lst = game.get_trade_log()
    response = []
    for i in range(len(transact_lst)):
        cur_transact = transact_lst[i]
        if len(cur_transact) == 2:
            for i in range(2):
                response = format_tranction_list(response, cur_transact[i])
        else: 
            response = format_tranction_list(response, cur_transact)
    response.reverse()
    return Response(json.dumps(response), status=200)

def format_tranction_list(response, cur_transact, game_id):
    '''
    Helper method that formats transactions into Front-End compatible dictionaries. 
    :param reponse: current reponse list
    :param cur_transact: action to add to response list
    :return: (list) updated response list
    '''
    game = cache.get(game_id)
    users = game.players
    if cur_transact["action"] == 'made market':
            response.append({
                "name": users[cur_transact['player']],
                "bid": cur_transact['bid'],
                "bid_size": cur_transact['bid_lots'],
                "ask": cur_transact['ask'],
                "ask_size": cur_transact['ask_lots'],
                "action": 'Make Market'
            })
    else:
        response.append({
            "name": users[cur_transact['player']],
            "bid": None,
            "bid_size": None,
            "ask": None,
            "ask_size": None,
            "action": str(cur_transact["action"]) +" " + str(cur_transact["quantity"])+"@"+str(cur_transact["price"])
        })
    return response

@gameB_api.route("/spread", methods=['POST'])
def get_spread():
    """
    Returns a dictionary containing two dictions for ask and bid
    Example response:
    {
        "ask": {"price": 8, "volume": 50},
        "bid": {"price": 5, "volume": 50}
    }
    """
    game_id = request.json['game_id']
    game = cache.get(game_id)
    password = request.json['password']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if password != game.password:
        return Response('Incorrect password for game with game_id: ' + game_id, status=401)
    response = game.get_current_spread()
    return Response(json.dumps(response), status=200)

@gameB_api.route("/range", methods=['POST'])
def get_range():
    """
    Returns a dictionary containing the range of cards
    Example response:
    {
        "low": 1,
        "high": 50
    }
    """
    game_id = request.json['game_id']
    game = cache.get(game_id)
    password = request.json['password']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if password != game.password:
        return Response('Incorrect password for game with game_id: ' + game_id, status=401)
    response = {"low": game.card_range_low, "high": game.card_range_high}
    return Response(json.dumps(response), status=200)

@gameB_api.route("/players", methods=['POST'])
def get_players():
    """
    Returns a dictionary with keys=playerIds and values=usernames
    Example response:
    {
      "0": "zzz",
      "1": "aaa",
    }
    """
    game_id = request.json['game_id']
    game = cache.get(game_id)
    password = request.json['password']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if password != game.password:
        return Response('Incorrect password for game with game_id: ' + game_id, status=401)
    users = game.players
    response = OrderedDict()
    for player in game.players:
        id = game.players[player].player_id
        response[id] = player
    # response = OrderedDict(zip(sorted(game.players), users))
    return Response(json.dumps(response), status=200)

@gameB_api.route("/currentPlayer", methods=['POST'])
def get_current_player():
    """
    Returns the name of the current player
    Example response:
    "Alex"
    """
    game_id = request.json['game_id']
    game = cache.get(game_id)
    password = request.json['password']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if password != game.password:
        return Response('Incorrect password for game with game_id: ' + game_id, status=401)
    if game.status == 2:
        return Response('Game with game_id: ' + game_id + ' has already ended.', status=401)
    users = game.players
    current_player = game.get_current_player()
    # current_player_name = users[sorted(game.all_players).index(current_player)]
    return Response(json.dumps(current_player), status=200)

@gameB_api.route("/cardRange", methods=['POST'])
def get_card_range():
    """
    Returns the card range (i.e. [1. 50])
    """
    game_id = request.json['game_id']
    game = cache.get(game_id)
    password = request.json['password']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if password != game.password:
        return Response('Incorrect password for game with game_id: ' + game_id, status=401)
    low = game.card_range_low
    high = game.card_range_high
    return [low, high]

@gameB_api.route("/playerCard", methods=['POST'])
def get_player_card():
    """
    Shows what card each player has

    {"Alex": 2, "Bob": 7, ...}
    """
    game_id = request.json['game_id']
    game = cache.get(game_id)
    password = request.json['password']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if password != game.password:
        return Response('Incorrect password for game with game_id: ' + game_id, status=401)
    if game.status != 1:
        return Response('Game with game_id: ' + game_id + ' is not in progress.', status=409)
    # users = game.all_players
    cards = game.get_players_cards()
    # res = dict(zip(users, cards.values()))
    return cards

@gameB_api.route("/gameUser", methods=['POST'])
def get_game_user():
    """
    Gets game users
    """
    game_id = request.json['game_id']
    game = cache.get(game_id)
    password = request.json['password']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if password != game.password:
        return Response('Incorrect password for game with game_id: ' + game_id, status=401)
    users = game.all_players
    return " ".join(users)

@gameB_api.route("/trueSum", methods=['POST'])
def get_true_sum():
    game_id = request.json['game_id']
    game = cache.get(game_id)
    password = request.json['password']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if password != game.password:
        return Response('Incorrect password for game with game_id: ' + game_id, status=401)
    if game.status != 1:
        return Response('Game with game_id: ' + game_id + ' is not in progress.', status=409)
    response = game.get_true_sum()
    return Response(json.dumps(response), status=200)


# NEW ROUTE
@gameB_api.route('/startGame', methods=['POST'])
def start_game():
    '''
    Begins the game.
    {
        'password': string,
        "game_id": "abcd"
    }. This will be abbreviated to user_data going forward.

    200 if game successfully started (exists in game cache).
    500 if game does not exist.
    409 if game already started.
    401 if permission levels not met.
    '''
    game_id = request.json['game_id']
    game = cache.get(game_id)
    password = request.json['password']
    if game is None:
        return Response('Game does not exist with game_id: ' + game_id, status=500)
    if password != game.password:
        return Response('Incorrect password for game with game_id: ' + game_id, status=401)
    if game.status != 0:
        return Response('Game with game_id: ' + game_id + ' has already been started.', status=409)
    if len(game.players) < 2:
        return Response('Game with game_id: ' + game_id + ' has less than 2 players.', status=409)
    game.start()
    
    # Add user
    cache.set(game_id, game)
    return Response('Game with game_id: ' + game_id + ' has started.', status=200)
