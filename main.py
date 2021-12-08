from flask import Flask, render_template, redirect, request, session, url_for

main = Flask(__name__)

@main.route('/home', methods=['POST', 'GET'])
@main.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')

@main.route('/set', methods=['POST', 'GET'])
def set():
    return render_template('agenda_set.html')

@main.route('/edit', methods=['POST', 'GET'])
def edit():
    return render_template('agenda_edit.html')

@main.route('/view', methods=['POST', 'GET'])
def view():
    return render_template('agenda_view.html')

main.run(debug=True)