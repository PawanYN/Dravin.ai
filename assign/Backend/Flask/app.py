from flask import Flask ,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/')
def hello_world():
    todo = Todo(title='Haribol', desc="Please chant and be happy")
    db.session.add(todo)
    db.session.commit()
    return render_template('index.html')


@app.route("/admin")
def Hell():  
    print("hello word")

if __name__ == '__main__':
    app.run(debug=True)
    