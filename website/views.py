from flask import Flask, render_template, url_for, redirect, request
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import  current_user

import random

views = Blueprint("views", __name__)

Games = dict()
game_id  = -1

@views.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html', user= current_user)

@views.route("/profile")
def profile():
    return render_template('profile.html', user= current_user)

@views.route("/hello")
def hello():
    return render_template('hello.html', user= current_user)


@views.route("/about", methods = ['GET'])
def about():
    return render_template('about.html', user= current_user)


@views.route("/feedback", methods = ['GET'])
def feedback():
    return render_template('feedback.html', user= current_user)


@views.route("/<usr>")
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



@views.route("/start_game", methods =['GET'])
def start_game():
    #generate new id for game
    global game_id
    game_id = game_id + 1

    #create new game
    Games[game_id] = Game()

    #send game object and id to play
    return redirect(url_for('views.game', id = game_id))

@views.route("/game/<id>/end", methods =['POST', 'GET'])
def game_end(id):
    id = int(id)
    if request.method == 'POST':
        if request.form['action'] == 'play again':
            return redirect(url_for('views.start_game'))
    else:
        return render_template('stats.html',
                           correct=Games[id].correct,
                           current=Games[id].cur_id)


@views.route("/game/<id>", methods =['POST', 'GET'])
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
            return redirect(url_for('views.game', id = game_id))
        elif request.form['action'] == 'play again':
            return redirect(url_for('views.start_game'))
        elif request.form['action'] == 'end':
            return redirect((url_for('views.game_end', id= id)))
        elif request.form['action'] == 'prev':
            return render_template('game.html',
                               word_to_serve=Games[id].words[Games[id].cur_id-1],
                               current = Games[id].cur_id-1,
                               correct = Games[id].correct, user= current_user)

    else:
        #check game status, if game ended, display stats
        if(Games[id].game_over()):
            return redirect((url_for('views.game_end', id= id)))
        else:
            #if game ongoing, get next word,
            word = Games[id].get_next_word()
            return render_template('game.html',
                                   word_to_serve = word,
                                   current = Games[id].cur_id,
                                correct = Games[id].correct, user= current_user)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5102)




