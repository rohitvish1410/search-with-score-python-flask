from fuzzywuzzy import fuzz, process
from flask import Flask, render_template, request

app = Flask(__name__)

names = ['Rohit', 'Rohan', 'Raj', 'Ram', 'Ramesh', 'Sujeet', 'Sudeep', 'Sanjay', 'Priyanka', 'Priyanshi', 'Mahesh', 'Mukesh',
         'Mangesh', 'Rohit', 'Raj', 'Priya', 'Preeti', 'Aakash', 'Akash', 'Aakash', 'Priyanshi', 'Sanjay', 'Sujata', 'Rajesh']


@app.route('/slider')
def slider():
    return render_template('slider.html')


@app.route('/process2', methods=['GET', 'POST'])
def process2():
    names = ['Rohit', 'Rohan', 'Raj', 'Ram', 'Ramesh', 'Sujeet', 'Sudeep', 'Sanjay', 'Priyanka', 'Priyanshi', 'Mahesh', 'Mukesh',
             'Mangesh', 'Rohit', 'Raj', 'Priya', 'Preeti', 'Aakash', 'Akash', 'Aakash', 'Priyanshi', 'Sanjay', 'Sujata', 'Rajesh']

    user_input = request.form['user_input']
    input_score = int(request.form['input_value'])
    match_name_list = []
    name_score_list = []
    message = 'No results found'
    for new_name in names:
        match_name = ""
        name_score = fuzz.ratio(user_input, new_name)
        if name_score >= input_score:
            match_name = new_name
            match_name_list.append(match_name)
            name_score_list.append(name_score)
    if len(match_name_list) != 0:
        return render_template('slider.html', match_name_list=match_name_list, name_score_list=name_score_list)
    else:
        return message


if __name__ == "__main__":
    app.run(debug=True)
