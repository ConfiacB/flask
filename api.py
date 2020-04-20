from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:050900bc,,@localhost/todo'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():

    return jsonify({'data': "hello world"})


@app.route('/todo', methods=['GET'])
def get_all_todos():
    """
    Recupere tous les todo

    Avec la methode GET, recupere tous les todo
    Et pour chaque todo, on indique id, text et s'ils sont complétés
    Retourne un tableau de todo dans du JSON
    """
    todos = Todo.query.all()
    output = []

    for todo in todos:
        todo_data = {}
        todo_data['id'] = todo.id
        todo_data['text'] = todo.text
        todo_data['complete'] = todo.complete
        output.append(todo_data)

    return jsonify({'todo': output})


@app.route('/todo/<todo_id>', methods=['GET'])
def get_one_todo(todo_id):
    """
    Recupere un todo

    Avec la methode GET, recupere un todo a l'aide de son id
    Et ce todo, on indique id, text et s'il est complété
    Retourne ce todo dans du JSON
    """
    todo = Todo.query.filter_by(id=todo_id).first()

    if not todo:
        return jsonify({'message': "No todo found"})

    todo_data = {}
    todo_data['id'] = todo.id
    todo_data['text'] = todo.text
    todo_data['complete'] = todo.complete

    return jsonify(todo_data)


@app.route('/todo', methods=['POST'])
def create_todo():
    """
    Créé un todo

    Avec la methode POST, créé un todo
    On spécifie les champ de ce nouveau todo en récupérant le text de data
    On rentre ce todo dans la base de donnee db
    Retourne un message de creation JSON
    """
    data = request.get_json()
    new_todo = Todo(text=data['text'], complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': "Todo created"})


@app.route('/todo/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """
    Update un todo

    Avec la methode PUT, update un todo a l'aide de son id
    si le todo n'existe pas, retourne un message JSON
    Meta jour la base de donnee
    Retourne un message de confirmation JSON
    """
    todo = Todo.query.filter_by(id=todo_id).first()

    if not todo:
        return jsonify({'message': "No todo found"})

    todo.complete = True
    db.session.commit()

    return jsonify({'message': "Todo item has been completed"})


@app.route('/todo/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """
    Supprime un todo

    Avec la methode DELETE, supprime un todo a l'aide de son id
    si le todo n'existe pas, retourne un message JSON
    Met a jour la base de donnee
    Retourne un message de confirmation JSON
    """
    todo = Todo.query.filter_by(id=todo_id).first()

    if not todo:
        return jsonify({'message': "No todo found"})

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': "Todo has been deleted"})


if __name__ == "__main__":
    app.run(debug=True)
