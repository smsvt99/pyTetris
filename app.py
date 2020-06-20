import os
from flask import Flask, render_template, jsonify, send_file, request, redirect, url_for
from flask_mysqldb import MySQL
from Score import Score

app = Flask(__name__, static_url_path="/", static_folder="static")

app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_DB'] = "scoreboard"

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/getTopTen')
def getTopTen():
    cur = mysql.connection.cursor()
    cur.execute("select * from scoreboard order by score desc limit 10")
    results = cur.fetchall() #a tuple of tuples, which makes ugly JSON
    resultsList = [Score(result).toDict() for result in results] #cannot serialize python class as JSON
    cur.close()
    return jsonify(resultsList)

@app.route('/insertOne', methods=['POST'])
def insertOne():
    print (request.is_json)
    content = request.get_json()
    print(content)
    cur = mysql.connection.cursor()
    cur.execute("insert into scoreboard(name, score) values('{}','{}')".format(content["name"], content["score"]))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('allScores'))

@app.route('/allScores')
def allScores():
    cur = mysql.connection.cursor()
    cur.execute("select * from scoreboard order by score desc")
    results = cur.fetchall()
    resultsList = [Score(result).toDict() for result in results]
    cur.close()
    return render_template("allScores.html", scores = resultsList)

if (__name__) == "__main__":
    app.run(debug=True)