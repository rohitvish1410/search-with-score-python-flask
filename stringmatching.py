from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from fuzzywuzzy import fuzz, process

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "users_db"

mysql = MySQL(app)


@app.route('/stringmatch')
def stringmatch():
    cur = mysql.connection.cursor()
    kur = mysql.connection.cursor()
    students = cur.execute("SELECT * from test_db")
    if students > 0:
        studentDetails = cur.fetchall()
    nameList = []
    kur.execute("SELECT Name from test_db")
    studentNames = kur.fetchall()
    for i in range(len(studentNames)):
        nameList.append(studentNames[i][0])
    print(nameList)

    # def match_term(term, list_names, min_score=0):
    #    max_score = -1
    #    max_name = ""
    #    for term2 in list_names:
    #        score = fuzz.ratio(term,term2)
    #        if (score>min_score) and (score>max_score):
    #            max_term = term2
    #            max_score = score
    #    return(max_name,max_score)
    # for i in nameList:
    #    print(i,match_term(i,nameList,50))

    return render_template('stringmatch.html', studentDetails=studentDetails, nameList=nameList)


if __name__ == "__main__":
    app.run(debug=True)
