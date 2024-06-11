from flask import Flask, request, render_template
import os
import time
import uuid

app = Flask(__name__)

# Configure the database path and URL
DB_PATH = os.path.join(os.path.dirname(__file__), 'pastes.db')
DB_URL = f"sqlite:///{DB_PATH}"

# Set up the database connection
# (You'll need to install the `flask-sqlalchemy` library: `pip install flask-sqlalchemy`)
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class Paste(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<Paste id={self.id}>"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        paste_id = str(uuid.uuid4())
        paste = Paste(id=paste_id, content=content)
        db.session.add(paste)
        db.session.commit()
        return render_template('paste.html', paste_id=paste_id)
    return render_template('index.html')

@app.route('/<paste_id>')
def show_paste(paste_id):
    paste = Paste.query.get(paste_id)
    if paste:
        return render_template('paste.html', content=paste.content, created_at=paste.created_at)
    else:
        return 'Paste not found', 404

if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.create_all()
    app.run(debug=True)