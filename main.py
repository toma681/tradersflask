import os
import sys
import threading
from flask import Flask, send_from_directory
from app import app as backend_app
from moderator_scripts.a_cl import loop as a_cl
from moderator_scripts.b_cl import loop as b_cl

import logging

# # FRONTEND #
# frontend_app = Flask(__name__, static_folder='./client/build')

# # Serve React App
# @frontend_app.route('/', defaults={'path': ''})
# @frontend_app.route('/<path:path>')
# def serve(path):
#     if path != "" and os.path.exists(frontend_app.static_folder + '/' + path):
#         return send_from_directory(frontend_app.static_folder, path)
#     else:
#         return send_from_directory(frontend_app.static_folder, 'index.html')

# def runFrontend():
#     frontend_app.run(host='127.0.0.1', port=8080, debug=False, threaded=True)

def runBackend():
    backend_app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)


if __name__ == '__main__':
    # Executing the Threads seperatly.
    # t1 = threading.Thread(target=runFrontend)
    t2 = threading.Thread(target=runBackend)
    # t1.start()
    t2.start()

    if len(sys.argv) > 1:
        if sys.argv[1] == 'a':
            a_cl()
        elif sys.argv[1] == 'b':
            b_cl()
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        