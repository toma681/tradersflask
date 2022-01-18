# Order to call these functions in:
# /createGame
# for each user in game.num_users:
#   /addUser
# for each round in game.num_rounds:
#   for each user in game.num_users:
#       /makeMarket
#   /playRound
#   /roundTransactions
#   /roundUnrealizedPnls
# /finalRoundRealizedPnls
# /finalRoundTotalPnls

import enum
from flask import Flask, json, request, jsonify, session, Response, Blueprint
from collections import OrderedDict
import copy
from .game import Game
from .player import Player
import sys

from .cache import cache
from .cache_api import cache as user_cache

gameA_api = Blueprint('gameA_api', __name__)

# TODO Configure for multiple games and with multiple players
@gameA_api.before_app_first_request
@cache.cached(timeout=300, key_prefix='game_users')
def create_game_users():
    return []

@gameA_api.route('/createGame', methods=['POST'])
def create_game():
    """
    Example body:
    {
        "true_values": [10, 20, 30],
        "num_players": 5,
        "override": true
    }
    """
    game = cache.get("game")
    game_users = cache.get('game_users')

    new_game = Game(true_values=request.json['true_values'], num_players=request.json['num_players'])
    if request.json.get("override", False):
        cache.clear()
        cache.set("game", new_game)
        cache.set("game_users", [])
    elif game is not None:
        return Response('Game already created', status=200)

    game = Game(true_values=request.json['true_values'], num_players=request.json['num_players'])

    for i in range(request.json['num_players']):
        game_users.append("Player {}".format(i))

    cache.set("game", game)
    cache.set('game_users', game_users)
    return Response('Game created', status=200)


@gameA_api.route('/addName', methods=['POST'])
def add_name():
    """
    Adds the name of the players.
    {
        'usernames': Alex Bob Charlie David Eevee
    }
    :return:
    """
    game_users = cache.get('game_users')
    msg = request.json['usernames']
    msg = msg.split()

    # Check user limit
    game = cache.get('game')
    if len(msg) > game.num_players:
        return Response("Exceeds max users", status=400)

    game.player_setup(msg)
    game_users = copy.deepcopy(msg)

    # Cache
    cache.set('game_users', game_users)
    cache.set('game', game)
    return Response(json.dumps(game_users), status=200)


def verify_get_user_pos(user_data):
    '''
    Helper function used to verify user and get user position,
    for setter functions (POST requests).
    '''
    game_users = cache.get('game_users')

    position = -1
    for i, pair in enumerate(game_users):
        if user_data == game_users[i]:
            position = i
            break
    if position == -1:
        return Response('User not in game', status=400)

    # Verification
    # users = user_cache.get('users')
    # verification = verify_user(user_data)
    # if verification.status_code != 200:
    #     return verification

    return position


@gameA_api.route("/makeMarket", methods=['POST'])
def make_market():
    '''
    Expects json data for a particular player to have:
    {
        "user": "Alex",
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
    '''
    game = cache.get('game')
    try:
        data = request.json
        user_data = data['user']  # username
        q1_bid, q1_bid_size, q1_ask, q1_ask_size = float(data['q1_bid']), int(data['q1_bid_size']), float(data['q1_ask']), int(data['q1_ask_size'])
        q2_bid, q2_bid_size, q2_ask, q2_ask_size = float(data['q2_bid']), int(data['q2_bid_size']), float(data['q2_ask']), int(data['q2_ask_size'])
        q3_bid, q3_bid_size, q3_ask, q3_ask_size = float(data['q3_bid']), int(data['q3_bid_size']), float(data['q3_ask']), int(data['q3_ask_size'])
    except:
        return Response(status=400)

    position = verify_get_user_pos(user_data)
    if isinstance(position, Response):
        return position  # return whatever error response the helper function gave

    try:
        assigned = game.players[position].assign_bids_and_asks([q1_bid_size, q1_bid, q1_ask, q1_ask_size], [q2_bid_size, q2_bid, q2_ask, q2_ask_size], [q3_bid_size, q3_bid, q3_ask, q3_ask_size])
    except Exception as e:
        return Response(str(e), status=400)

    cache.set('game', game)
    return Response(assigned, status=200)


@gameA_api.route("/playRound", methods=['POST'])
def play_round():
    '''
    Game class calculates all the transactions between players.
    First checks if all players have inputted their most recent markets
    No input needed for this function call.
    Call this function after all users have put in their markets for a given round.
    This function doesn't return anything, call the functions below for that.
    '''

    # Uncache game
    game = cache.get('game')
    game_users = cache.get('game_users')

    if len(game_users) != game.num_players:
        return Response("Not enough users", status=400)

    # make sure every user has inputted data exactly k times (where k is the current round of game)
    # for user, markets_made in game_users:
    #     if markets_made != game.num_rounds_played + 1:
    #         return Response("Mismatch between current round number and user's round", status=400)

    # Grab data
    try:
        result_bool = game.play_round()
    except Exception as e:
        return Response(str(e), status=400)

    # Recache game
    cache.set('game', game)

    return Response(result_bool, status=200)

@gameA_api.route('/undo', methods=['POST'])
def undo():
    """
    Undo last action
    """
    game = cache.get('game')

    # Perform action
    try:
        game = game.undo()
    except Exception as e:
        return Response(str(e), status=400)

    # Recache game
    cache.set('game', game)

    return Response("Undo", status=200)

@gameA_api.route('/end', methods=['POST'])
def end_game():
    """
    Ends the Game
    """
    game = cache.get('game')

    game.end_game = True

    # Cache
    cache.set('game', game)
    return Response("END GAME", status=200)

@gameA_api.route("/players", methods=['GET'])
def get_players():
    """
    Returns a list of usernames
    Example response:
    {
      ["Alex", "Bob", "Charlie"]
    }
    """
    users = cache.get('game_users')
    return Response(json.dumps(users), status=200)


@gameA_api.route("/market", methods=['GET'])
def get_market():
    """
    Returns all players' market
    """
    game = cache.get('game')
    response = game.get_market()
    return Response(json.dumps(response), status=200)


@gameA_api.route("/transaction", methods=['GET'])
def get_transaction():
    game = cache.get('game')
    response = game.get_last_transaction_display()
    return Response(json.dumps(response), status=200)


@gameA_api.route("/pnl", methods=['GET'])
def get_pnl_table():
    game = cache.get('game')
    response = game.get_adjusted_pnl_table()
    return Response(json.dumps(response), status=200)


@gameA_api.route("/finalRoundTotalPnls", methods=['GET', 'POST'])
def get_final_pnls():
    game = cache.get('game')
    try:
        response = game.pnls
    except:
        return Response("Didn't play final round yet", status=400)
    return Response(json.dumps(response), status=200)


@gameA_api.route("/avgTransaction", methods=['GET'])
def get_avg_transaction():
    game = cache.get('game')
    response = game.get_avg_transactions_prices()
    return Response(json.dumps(response), status=200)
