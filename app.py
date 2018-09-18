from typing import Tuple

from flask import Flask, jsonify, request, Response, url_for, redirect
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route("/users")
def users():
    team = request.args.get('team')
    user_team = {}
    for i in db.initial_db_state["users"]:
        if i["team"] == team:
            if user_team["users"] == None:
                user_team["users"] = []
                user_team["users"].append(i)
            else:
                user_team["users"].append(i)
    return create_response(user_team)

@app.route("/users/<id>")
def users_id(id):
    for i in db.initial_db_state["users"]:
        if i["id"] == int(id):
            return create_response(i)
    return redirect('/404')

@app.errorhandler(404)
def id_not_found(e):
    return "404 Error Message: Wrong id!"
# TODO: Implement the rest of the API here!

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
