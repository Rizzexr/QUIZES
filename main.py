from flask import Flask, render_template, request, session, jsonify
import datetime

app = Flask(__name__)
app.secret_key = 'vyboryvyborycandidatypidory'

logged_times = {}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/rizzexr')
def admin_panel():
    return render_template('admin.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    session['username'] = username
    return render_template('index.html', username=username)

@app.route('/clear', methods=['POST'])
def clear():
    global logged_times
    logged_times = {}  
    return render_template('admin.html')

@app.route('/log_time', methods=['POST'])
def log_time():
    global logged_times 

    username = session.get('username')
    time_standart = request.json.get('time_pressed')
    time_mili = request.json.get('milisek')

    if username and time_standart is not None and time_mili is not None:
        time_object = datetime.datetime.fromtimestamp(time_standart / 1000)  
        formatted_time = time_object.strftime('%H:%M:%S.') + str(time_mili)

        logged_times[username] = formatted_time
        print(f"User: {username}, Time Pressed: {formatted_time}")
        print("Current log:", logged_times)  

        return 'Time logged successfully', 200
    else:
        return 'User not found or invalid time', 400

@app.route('/get_times')
def get_times():
    global logged_times
    return jsonify(logged_times)  

@app.errorhandler(404)
def page_not_found(error):
    return "Страница не найдена", 404

@app.errorhandler(500)
def internal_server_error(error):
    return "Внутренняя ошибка сервера", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')