from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from urllib.parse import quote
from flask import Flask, render_template, jsonify, request
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'Njnj0235'
CORS(app)
password = 'Neevesh@123'
encoded_password = quote(password)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:{}@localhost:3306/task_manager'.format(encoded_password)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = [{'id': task.id, 'name': task.name, 'completed': task.completed} for task in tasks]
    return jsonify(task_list)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(name=data.get('name'))
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id, 'name': new_task.name, 'completed': new_task.completed}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get_or_404(task_id)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify({'id': task.id, 'name': task.name, 'completed': task.completed})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/api/tasks/<int:task_id>/edit', methods=['PUT'])
def edit_task(task_id):
    data = request.get_json()
    task = Task.query.get_or_404(task_id)
    task.name = data.get('name', task.name)
    db.session.commit()
    return jsonify({'id': task.id, 'name': task.name, 'completed': task.completed})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'password':
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html', error=None)

@app.before_request
def check_authentication():
    allowed_routes = ['login']  # Add routes that should be accessible without authentication
    if request.endpoint and request.endpoint not in allowed_routes and 'username' not in session:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
