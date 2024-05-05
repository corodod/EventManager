from flask import Flask, jsonify, render_template, \
    request, redirect, url_for  # Импортируем jsonify для преобразования данных в формат JSON
from flask_socketio import SocketIO
import sqlite3

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

# Создаем подключение к базе данных
conn = sqlite3.connect('events.db', check_same_thread=False)
cursor = conn.cursor()

# Создаем таблицу для хранения событий, если она еще не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS events
                  (id INTEGER PRIMARY KEY, date TEXT, time TEXT, event TEXT)''')
conn.commit()

@app.route('/')
def index():
    # Получаем события из базы данных
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    return render_template('index.html', events=events)

@app.route('/add_event', methods=['POST'])
def add_event():
    date = request.form['date']
    event = request.form['event']
    time = request.form['time']

    # Добавляем событие в базу данных
    cursor.execute('INSERT INTO events (date, time, event) VALUES (?, ?, ?)', (date, time, event))
    conn.commit()

    return redirect(url_for('index'))

@app.route('/delete_event', methods=['POST'])
def delete_event():
    date = request.form['date']
    time = request.form['time']

    # Удаляем событие из базы данных
    cursor.execute('DELETE FROM events WHERE date=? AND time=?', (date, time))
    conn.commit()

    return redirect(url_for('index'))

@app.route('/get_event_data')
def get_event_data():
    # Получаем события из базы данных
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()

    # Формируем список событий в формате JSON
    event_list = [{'date': event[1], 'time': event[2], 'event': event[3]} for event in events]

    return jsonify({'events': event_list})  # Возвращаем данные о событиях в формате JSON


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
