from flask import Flask, render_template
from dynamodb import get_all_users

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users')
def get_users():
    users = get_all_users()
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run()
