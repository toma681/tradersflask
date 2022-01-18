from flask import Flask, json, request, jsonify, session, Response, Blueprint
import sys, string, random

from .cache import cache as cache

users_api = Blueprint('users_api', __name__)

@users_api.before_app_first_request
@cache.cached(timeout=300, key_prefix='users')
def before_first_request():
    return {}

@users_api.route('/registerUser', methods=['POST'])
def register_user():
    '''
    (string-ascii) username
    - This can be a username or email address.

    Verifies username is not already used.
    200 if not used. Returns SHA key in body.
    400 if used. Error user.
    '''
    users = cache.get('users')
    print(request)
    new_user = request.data.decode('ascii')
    if new_user in users:
        return Response(status=400)

    # Ensure no collissions (although super, super unlikely)
    hash = None
    letters = string.ascii_lowercase
    while hash == None:
        hash = ''.join(random.choice(letters) for i in range(32))
        for user in users:
            if users[user] == hash:
                hash = None
                break
    users[new_user] = hash

    cache.set('users', users)

    return Response(json.dumps(hash), status=200)

def verify_user(data):
    users = cache.get('users')

    try:
        username = str(data['username'])
        secret_key = str(data['secret_key'])
    except:
        return Response(status=400)

    if username not in users:
        return Response("User does not exist", status=400)
    if users[username] != secret_key:
        return Response(status=403)
    else:
        return Response(status=200)

@users_api.route('/verifyUser', methods=['POST'])
def verify_user_api():
    '''
    {
        'username': string,
        'secret_key': string 
    }
    403 if incorrect. 200 if correct.
    400 if incorrect data or user does not exist.
    '''
    data = request.json
    return verify_user(data)
