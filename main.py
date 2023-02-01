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
from flask import Flask,request
import json,time
#now dumps is global func waw
app = Flask(__name__)
# contains levels
levels = {
    'test': {
        'name': 'test server',
        'spawn': {
            'x': -135,
            'y': -155
        },
        'entities': [
            {
                'obj': 'sign',
                'name': 'Info',
                'text': 'this server is to test the cubix backend',
                'location': {
                    'x': -130,
                    'y': -155
                }
            }
        ],
        'players': {}
    }
}
responses = {
    'noLevel': '{"error": "requested level doesnt exist", "success": false}',
    'alreadyJoined': '{"error": "there is already someone online with that name", "success": false}',
    'noPlayer': '{"error": "there is noone in this server by that name", "success": false}',
    'success': '{"success": true}'
}
def newObject(level, type, name, location, meta):
    newObj = {
        'obj': type,
        'name': name,
        'location': location
    }
    if type == 'sign':
        newObj['text'] = meta['text']
    if type == 'player': 
        levels[level]['players'][name] = len(levels[level]['entities'])
    levels[level]['entities'].append(newObj)

def usernameUsed(level, username):
    return username in levels[level]['players']

@app.route('/join', methods=["GET"])
def push_user():
    try:
        level = request.args.get("level")
        username = request.args.get("user")
        if level == None:
            return levels.keys()
        if not level in levels: 
            return responses['noLevel']
        if usernameUsed(level, username):
            return responses['alreadyJoined']

        newObject(level, 'player', username, levels[level]['spawn'],"hi")
        return levels
    except BaseException as e:
        return str(e)

@app.route('/leave', methods=["GET"])
def remove_user():
    level = request.args.get("level")
    username = request.args.get("user")
    if not level in levels: 
        return responses['noLevel']
    if not username in levels[level]['players']:
        return responses['noPlayer']
        
    player = levels[level]['players'][username]
    levels[level]['entities'].remove(player)
    return responses['success']

@app.route('/', methods=["GET"])
def hello_world():
    return 'you should not be here >:('
