from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'helloworld'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app) #initializes database

    # blueprint for auth routes in our app
    from .auth import auth #relative import
    app.register_blueprint(auth, url_prefix = "/")

    #blueprint for other parts of app
    from .views import views
    app.register_blueprint(views, url_prefix = "/")

    # need to import db model User first before creating db
    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login" #redirect to login page
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id): #loads id of user for a session
        return User.query.get(int(id))

    return app


def create_database(app):
    # if db doesnt exist
    if not path.exists("website/" + DB_NAME):
        db.create_all(app = app)
        print('created db!')

'''



@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/hello")
def hello():
    return render_template('hello.html')


@app.route("/about", methods = ['GET'])
def about():
    return render_template('about.html')


@app.route("/feedback", methods = ['GET'])
def feedback():
    return render_template('feedback.html')


@app.route("/<usr>")
def user(usr):
    return f"<h1> {usr} </h1>"


def display_progress():
    return 100

word_list = ['bird', 'cat', 'green' , 'blue', 'red', 'black', 'white',
             'dance', 'sing', 'bird', 'cat', 'green' , 'blue', 'red', 'black', 'white',
             'dance', 'sing','bird', 'cat', 'green' , 'blue', 'red', 'black', 'white',
             'dance', 'sing','bird', 'cat', 'green' , 'blue', 'red', 'black', 'white',
             'dance', 'sing','bird', 'cat', 'green' , 'blue', 'red', 'black', 'white',
             'dance', 'sing']
word_dict = {'bird': 'pajaro', 'cat': 'gato', 'green': 'verde',
             'blue': 'azul', 'red': 'rojo', 'black': 'negro',
             'white': 'blanco', 'dance': 'bailar', 'sing': 'cantar'}

class Game():
    def __init__(self, n = 10):
        self.n = n
        self.cur_id = 0
        self.correct = 0
        self.plays =[0] * self.n
        self.words = random.sample(word_list, self.n)

    def game_over(self):
        if self.cur_id == self.n:
            return True
        return False

    def get_next_word(self):
        self.cur_id += 1
        return self.words[self.cur_id-1]

    def check_user_answer(self, user_answer):
        right_answer = word_dict[self.words[self.cur_id-1]]
        if user_answer ==right_answer:
            self.plays[self.cur_id-1] = 1
            self.correct +=1
            return True, right_answer
        else:
            self.plays[self.cur_id-1] = -1
        return False, right_answer


@app.route("/start_game", methods =['GET'])
def start_game():
    #generate new id for game
    global game_id
    game_id = game_id + 1

    #create new game
    Games[game_id] = Game()

    #send game object and id to play
    return redirect(url_for('game', id = game_id))

@app.route("/game/<id>/end", methods =['POST', 'GET'])
def game_end(id):
    id = int(id)
    if request.method == 'POST':
        if request.form['action'] == 'play again':
            return redirect(url_for('start_game'))
    else:
        return render_template('stats.html',
                           correct=Games[id].correct,
                           current=Games[id].cur_id)


@app.route("/game/<id>", methods =['POST', 'GET'])
def game(id):
    id = int(id)
    if request.method == 'POST':
        print(request.form.items())
        if request.form['user_input']:
            user_answer = request.form['user_input']
            check, correct_answer = Games[id].check_user_answer(user_answer)
            return render_template('result.html',
                                   user_answer = user_answer,
                                   correct_answer = correct_answer,
                                   current=Games[id].cur_id,
                                   correct=Games[id].correct)
        elif request.form['action'] == 'next':
            return redirect(url_for('game', id = game_id))
        elif request.form['action'] == 'play again':
            return redirect(url_for('start_game'))
        elif request.form['action'] == 'end':
            return redirect((url_for('game_end', id= id)))
        elif request.form['action'] == 'prev':
            return render_template('game.html',
                               word_to_serve=Games[id].words[Games[id].cur_id-1],
                               current = Games[id].cur_id-1,
                               correct = Games[id].correct)

    else:
        #check game status, if game ended, display stats
        if(Games[id].game_over()):
            return redirect((url_for('game_end', id= id)))
        else:
            #if game ongoing, get next word,
            word = Games[id].get_next_word()
            return render_template('game.html',
                                   word_to_serve = word,
                                   current = Games[id].cur_id,
                                correct = Games[id].correct)

'''

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5102)




