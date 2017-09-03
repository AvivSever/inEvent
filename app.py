# pylint: disable=invalid-name, C0111, C0301
from flask import Flask, jsonify, abort, make_response, request

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


@app.route('/')
def hello_world():
    """ Returns to the client - 'Hello World!' """
    return 'Hello World!'


@app.route('/inevent/api/v1.0/events', methods=['GET'])
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
    return make_response(jsonify({'error': 'Not Found', 'external information': str(error)}), 404)

@app.route('/inevent/api/v1.0/events/create', methods=['POST'])
def create_event():
    """ Creates a new event by posting from the client """
    if not request.json or not 'title' in request.json:
        abort(400)
    new_event = {
        'id': events[-1]['id'] + 1,
        'title': request.json['title']
    }

if __name__ == '__main__':
    app.run(debug=True)
