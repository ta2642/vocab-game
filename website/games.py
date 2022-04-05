import random
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
        self.cur_id = -1
        self.correct = 0
        self.plays =[0] * self.n
        self.words = random.sample(word_list, self.n)


    def get_next_word(self):
        self.cur_id += 1
        return self.words[self.cur_id]

    def check_user_answer(self, user_answer):
        right_answer = word_dict[self.words[self.cur_id]]
        if user_answer ==right_answer:
            self.plays[self.cur_id] = 1
            self.correct +=1
            return True
        else:
            self.plays[self.cur_id] = -1
        return False


if __name__ == '__main__':
    gm = Game()
    Games = dict()
    Games[0] = Game()
    Games[1] = Game()
    print(Games.items())
    print(gm.words)
    print(Games[1].words)
    print(gm.get_next_word(), gm.cur_id)
    print(gm.get_next_word(), gm.cur_id, gm.correct)
    print(gm.cur_id, gm.check_user_answer('dog'),gm.cur_id, gm.correct)
    print(gm.get_next_word(), gm.cur_id, gm.correct)