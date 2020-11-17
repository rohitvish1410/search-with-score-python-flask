from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from fuzzywuzzy import fuzz, process

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "users_db"

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        Id = request.form['Id']
        Name = request.form['Name']
        Subject = request.form['Subject']
        City = request.form['City']
        Status = request.form['Status']
        cur = mysql.connection.cursor()
        cur.execute("INSERT into test_db(Id,Name,Subject,City,Status) VALUES (%s,%s,%s,%s,%s)",
                    (Id, Name, Subject, City, Status))
        mysql.connection.commit()
        cur.close()
        return "Successfully inserted new entry!"

    return render_template('index.html')


@app.route('/students')
def students():
    cur = mysql.connection.cursor()
    students = cur.execute("SELECT * from test_db")
    if students > 0:
        studentDetails = cur.fetchall()
        return render_template('students.html', studentDetails=studentDetails)


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/match', methods=['GET', 'POST'])
def match():
    if request.method == 'POST':
        name_of_student = request.form['name_of_student']
        subject_of_student = request.form['subject_of_student']
        city_of_student = request.form['city_of_student']
        status_of_student = request.form['status_of_student']
        cur = mysql.connection.cursor()
        kur = mysql.connection.cursor()

        nameList = []
        kur.execute("SELECT Name from test_db")
        studentNames = kur.fetchall()
        for i in range(len(studentNames)):
            nameList.append(studentNames[i][0])

        input_score = int(request.form['input_value'])
        match_name_list = []
        name_score_list = []
        message = 'No results found'
        for new_name in nameList:
            match_name = ""
            name_score = fuzz.ratio(name_of_student, new_name)
            sql = """UPDATE test_db SET Score = %s WHERE Name = %s"""
            val = (name_score, new_name)
            cur.execute(sql, val)
            if name_score >= input_score:
                match_name = new_name
                match_name_list.append(match_name)
                name_score_list.append(name_score)
        #print(match_name_list, name_score_list)
        copy_name_score_list = name_score_list.copy()
        copy_name_score_list.sort(reverse=True)
        # print(copy_name_score_list)

        match_name_dict = {}
        for key in match_name_list:
            for value in name_score_list:
                match_name_dict[key] = value
                name_score_list.remove(value)
                break
        sorted_dict = {k: v for k, v in sorted(
            match_name_dict.items(), key=lambda v: v[1], reverse=True)}
        # print(sorted_dict)
        filtered_match_name_list = list(sorted_dict.keys())
        # print(filtered_match_name_list)

        final_list = []
        final_tuple = ()
        for each_name in filtered_match_name_list:
            if subject_of_student == 'None' and city_of_student == 'None' and status_of_student == 'None':
                cur.execute(
                    "SELECT * from test_db WHERE Name = '"+each_name+"'")
            elif subject_of_student != 'None' and city_of_student == 'None' and status_of_student == 'None':
                cur.execute("SELECT * from test_db WHERE Name = '" +
                            each_name+"' AND Subject = '"+subject_of_student+"'")
            elif subject_of_student == 'None' and city_of_student != 'None' and status_of_student == 'None':
                cur.execute("SELECT * from test_db WHERE Name = '" +
                            each_name+"' AND City = '"+city_of_student+"'")
            elif subject_of_student == 'None' and city_of_student == 'None' and status_of_student != 'None':
                cur.execute("SELECT * from test_db WHERE Name = '" +
                            each_name+"' AND Status = '"+status_of_student+"'")
            elif subject_of_student == 'None' and city_of_student != 'None' and status_of_student != 'None':
                cur.execute("SELECT * from test_db WHERE Name = '"+each_name +
                            "' AND City = '"+city_of_student+"' AND Status = '"+status_of_student+"'")
            elif subject_of_student != 'None' and city_of_student != 'None' and status_of_student == 'None':
                cur.execute("SELECT * from test_db WHERE Name = '"+each_name +
                            "' AND Subject = '"+subject_of_student+"' AND City = '"+city_of_student+"' ")
            elif subject_of_student != 'None' and city_of_student == 'None' and status_of_student != 'None':
                cur.execute("SELECT * from test_db WHERE Name = '"+each_name +
                            "' AND Subject = '"+subject_of_student+"' AND Status = '"+status_of_student+"' ")
            elif subject_of_student != 'None' and city_of_student != 'None' and status_of_student != 'None':
                cur.execute("SELECT * from test_db WHERE Name = '"+each_name+"' AND Subject = '" +
                            subject_of_student+"' AND City = '"+city_of_student+"' AND Status = '"+status_of_student+"'")
            student_info = cur.fetchall()
            student_info_list = list(student_info)
            for i in student_info_list:
                final_list.append(i)
        final_tuple = tuple(final_list)
        # print(final_tuple)

        if len(match_name_list) != 0:
            return render_template('search.html', final_tuple=final_tuple)
        else:
            return message

        cur.execute("UPDATE test_db SET Score = NULL")
        mysql.connection.commit()
        cur.close()

        # return render_template('search.html', student_info=student_info)


@app.route('/slider')
def slider():
    return render_template('slider.html')


if __name__ == "__main__":
    app.run(debug=True)
