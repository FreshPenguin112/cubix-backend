"""
levels: {
    levelName: {
        name: 'levelName' # technicaly redundent but simplfies the code using this json
        spawn: {
            x: 0,
            y: 0
        }
        entities: [
            {
                obj: 'player',
                name: 'p1',
                location: {
                    x: 10,
                    y: -10
                }
            },
            {
                obj: 'key',
                name: 'Key',
                location: {
                    x: 15,
                    y: 10
                }
            }
        ]
        players: {'p1': 0} # this way we dont need to comb through all the entities just to find players
    }
}
"""
from flask import Flask, request
from flask_cors import CORS
import json, time, sys, math

app = Flask(__name__)
CORS(app)

levels = {
    'test': {
        'name':
        'test server',
        'spawn': {
            'x': -135,
            'y': -155
        },
        'entities': [{
            'obj': 'sign',
            'name': 'Info',
            'text': 'this server is to test the cubix backend',
            'location': {
                'x': -130,
                'y': -155
            }
        }],
        'players': {}
    }
}
responses = {
    'noLevel': '{"error": "requested level doesnt exist", "success": false}',
    'alreadyJoined':
    '{"error": "there is already someone online with that name", "success": false}',
    'noPlayer':
    '{"error": "there is noone in this server by that name", "success": false}',
    'success': '{"success": true}',
    "noName": '{"error": "you forgot to put a name", "success": false}',
    "invalidAction": '{"error": "the provided action is not valid", "success": false}',
    "outOfRange": '{"error": "the provided target/position is out of range", "success": false}'
}


def newObject(level, type, name, location, meta={}):
    newObj = {'obj': type, 'name': name, 'location': location}

    if type == 'sign':
        newObj['text'] = meta['text']
    if type == 'player':
        levels[level]['players'][name] = len(levels[level]['entities'])
    levels[level]['entities'].append(newObj)


def getDistance(pos1, pos2):
    xd = pos2['x'] - pos1['x']
    yd = pos2['y'] - pos1['y']
    return math.sqrt(xd + yd)


def usernameUsed(level, username):
    return username in levels[level]['players']


@app.route('/join', methods=["GET"])
def push_user():
    level = request.args.get("level")
    username = request.args.get("user")
    if level == None:
        return levels.keys()
    if username == None:
        return responses['noName']
    if not level in levels:
        return responses['noLevel']
    if usernameUsed(level, username):
        return responses['alreadyJoined']

    newObject(level, 'player', username, levels[level]['spawn'])
    return levels


@app.route('/leave', methods=["GET"])
def remove_user():
    level = request.args.get("level")
    username = request.args.get("user")
    if not level in levels:
        return responses['noLevel']
    if not usernameUsed(level, username):
        return responses['noPlayer']
    entity = levels[level]['players'][username]
    levels[level]['entities'].pop(entity)
    del levels[level]['players'][username]
    return responses['success']


@app.route('/levels', methods=["GET"])
def levelslol():
    return list(levels.keys())


@app.route('/level/<level>', defaults={'attr': None}, methods=["GET"])
@app.route('/level/<level>/<attr>', methods=["GET"])
def levelget(level, attr):
    if not level in levels:
        return responses['noLevel']
    level = levels[level]
    if not attr == None:
        return level[attr]
    return level


@app.route('/update/<level>/<username>/<action>', methods=["POST"])
def setUser(level, username, action):
    actionData = request.json['data']
    if not type(actionData) == dict:
        return responses['invalidAction']
    if not level in levels:
        return responses['noLevel']
    if not usernameUsed(level, username):
        return responses['noPlayer']
    level = levels[level]
    playerIdx = level['players'][username]
    player = level['entities'][playerIdx]
    if action == 'grab':
        targetIdx = actionData['target']
        target = level['entities'][targetIdx]
        targetPos = target['location']
        playerPos = player['location']
        distance = getDistance(playerPos, targetPos)
        level['entities'][targetIdx]['location'] = actionData['moveTo']
        level['entities'][playerIdx]['holding'] = actionData['target']
        return responses['success']
    elif action == 'move':
        targetPos = actionData['newPos']
        playerPos = player['location']
        distance = getDistance(playerPos, targetPos)
        if distance >= 10:
            return responses['outOfRange']
        level['entities'][playerIdx]['location'] = targetPos
        return responses['success']
    else:
        return responses['invalidAction']
        

@app.route('/', methods=["GET"])
def hello_world():
    return 'you should not be here >:('
