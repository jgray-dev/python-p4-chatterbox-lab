from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        returnList = list()
        for message in Message.query.order_by('created_at').all():
            returnList.append(message.to_dict())
        return jsonify(returnList)
    if request.method == 'POST':
        msg = Message(
            body=request.get_json()['body'],
            username=request.get_json()['username']
        )
        db.session.add(msg)
        db.session.commit()
        return msg.to_dict()
        
        

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    msg = Message.query.filter(Message.id == id).first()

    if request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(msg, attr, data[attr])

        db.session.add(msg)
        db.session.commit()

        return jsonify(msg.to_dict()),200
    if request.method == 'DELETE':
        db.session.delete(msg)
        db.session.commit()
        return jsonify(msg.to_dict()),204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
