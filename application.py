from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
db = SQLAlchemy(app)

class Space(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parkSlot = db.Column(db.String(80), unique=True, nullable=False)
    isFull = db.Column(db.Boolean)

    def __repr__(self):
        return f"{self.parkSlot} - {self.isFull}"

@app.route('/')
def index():
    return "Hello!"

@app.route('/spaces')
def get_spaces():
    spaces = Space.query.all()
    output = []
    for space in spaces:
        space_data = {"parkSlot": space.parkSlot, "isFull": space.isFull}
        output.append(space_data)
    return {"park": output}

@app.route('/spaces/<id>')
def get_space(id):
    space = Space.query.get_or_404(id)
    return {"parkSlot": space.parkSlot, "isFull": space.isFull}

@app.route('/spaces', methods=['POST'])
def add_space():
    spaces = Space(parkSlot=request.json['parkSlot'], isFull=request.json['isFull'])
    db.session.rollback()
    db.session.add(spaces)
    db.session.commit()
    return {"id": spaces.id}

@app.route('/spaces/<id>', methods=['DELETE'])
def delete_space(id):
    space = Space.query.get(id)
    if space is None:
        return {"error": "not found"}
    db.session.rollback()
    db.session.delete(space)
    db.session.commit()
    return {"message": "successful"}

if __name__ == "__main__":
    app.debug=True
    app.run()