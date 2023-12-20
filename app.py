from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def play_game(user_choice):
    choices = ['pierre', 'papier', 'ciseaux', 'lezard', 'spock']
    computer_choice = random.choice(choices)

    # Détermine le résultat en fonction des règles
    result = determine_result(user_choice, computer_choice)

    update_score(result)

    return {'user': user_choice, 'computer': computer_choice, 'result': result, 'score': get_score()}

def determine_result(user_choice, computer_choice):
    # Détermine le résultat en fonction des règles
    if user_choice == computer_choice:
        return 'Égalité !'
    elif (
        (user_choice == 'ciseaux' and computer_choice == 'papier') or
        (user_choice == 'papier' and computer_choice == 'pierre') or
        (user_choice == 'pierre' and computer_choice == 'lezard') or
        (user_choice == 'lezard' and computer_choice == 'spock') or
        (user_choice == 'spock' and computer_choice == 'ciseaux') or
        (user_choice == 'ciseaux' and computer_choice == 'lezard') or
        (user_choice == 'lezard' and computer_choice == 'papier') or
        (user_choice == 'papier' and computer_choice == 'spock') or
        (user_choice == 'spock' and computer_choice == 'pierre') or
        (user_choice == 'pierre' and computer_choice == 'ciseaux')
    ):
        return 'Vous avez gagné !'
    else:
        return 'L\'ordinateur a gagné !'

def update_score(result):
    if 'score' not in session:
        session['score'] = {'player': 0, 'computer': 0}

    if result == 'Vous avez gagné !':
        session['score']['player'] += 1
    elif result == 'L\'ordinateur a gagné !':
        session['score']['computer'] += 1

def get_score():
    return session.get('score', {'player': 0, 'computer': 0})

@app.route('/')
def index():
    # Vérifie si c'est le début d'une nouvelle partie
    if session.pop('new_game', False):
        if 'score' not in session:
            session['score'] = {'player': 0, 'computer': 0}

    return render_template('index.html', score=session['score'])

@app.route('/play', methods=['POST'])
def play():
    user_choice = request.form['choice']
    result = play_game(user_choice)

    # Marque le début d'une nouvelle partie dans la session
    session['new_game'] = True

    return render_template('result.html', result=result)
  

@app.route('/replay', methods=['GET'])
def replay():
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)