# pylint: disable=invalid-name, C0111, C0301
from flask import Flask, jsonify, abort, make_response, request, url_for, redirect
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)

# TODO 1: Create a schema for an event


events = [
    {
        'id': 1,
        'title': u'Surprise party for Janice',
        'description': u'Janice is turning 20 on the 2nd of september! We will make sure she has a great time!',
        'location': u'Shoot 2 kill - Laser Tag, Rishon LeZion, Israel',
        'secret': True
    },
    {
        'id': 2,
        'title': u'Tony bailed out of jail party!',
        'description': u'Tony escaped prison and did not get caught! PARTY',
        'location': u'Shoot 2 kill - Laser Tag, Rishon LeZion, Israel',
        'secret': True
    }
]

users = [
    {
        'username': 'don',
        'password': 'juan',
        'email': 'donjuan@gmail.com',
        'permission': 'admin'
    },
    {
        'username': 'eric',
        'password': 'einstein',
        'email': 'eeric@gmail.com',
        'permission': 'basic'
    }
]


@auth.get_password
def get_password(username):
    user = [user for user in users if user['username'] == username]
    # if len(user) == 0:
        # abort(401)
    if len(user) != 0:
        return user[0]['password']
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    

@app.route('/')
def hello_world():
    """ Returns to the client - 'Hello World!' """
    return 'Hello World!'


@app.route('/inevent/api/v1.0/events', methods=['GET'])
@auth.login_required
def get_events():
    """Returns to the client all the events available"""
    return jsonify({'events': events})

@app.route('/inevent/api/v1.0/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """
    Returns to the client the event requested.
    :param event_id:
    """
    event = [event for event in events if event['id'] == event_id]
    print event
    if len(event) == 0:
        abort(404)
    return jsonify({'event': event[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found', 'info': str(error)}), 404)

@app.route('/inevent/api/v1.0/events/create', methods=['POST'])
def create_event():
    """ Creates a new event by posting from the client """
    if not request.json or not 'title' in request.json:
        abort(400)
    new_event = {
        'id': events[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'location': request.json.get('location', ""),
        'secret': False
    }
    events.append(new_event)
    return jsonify({'event': new_event}), 201

@app.route('/inevent/api/v1.0/events/update/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = [event for event in events if event['id'] == event_id]
    print 'Event -', event
    print 'Type -', type(event)
    if len(event) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and not isinstance(request.json['title'], unicode):
        abort(400)
    if 'description' in request.json and not isinstance(request.json['description'], unicode):
        abort(400)
    if 'location' in request.json and not isinstance(request.json['location'], unicode):
        abort(400)
    if 'secret' in request.json and not isinstance(request.json['secret'], bool):
        abort(400)
    event[0]['title'] = request.json.get('title', event[0]['title'])
    event[0]['description'] = request.json.get('description', event[0]['description'])
    event[0]['location'] = request.json.get('location', event[0]['location'])
    event[0]['secret'] = request.json.get('secret', event[0]['secret'])
    return jsonify({'result': True})

@app.route('/inevent/api/v1.0/events/delete/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = [event for event in events if event['id'] == event_id]
    if len(event) == 0:
        abort(404)
    events.remove(event[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
