from flask import Flask, render_template
import csv

app = Flask(__name__, template_folder='E:/reposD/MovieReccomender/views')
app.debug = True

@app.route('/')

def index():
    enum_data = read_csv()
    return render_template('index.html', enum_data=enum_data)

def read_csv():
    enum_data = []  # This list will store the extracted enum values
    with open('titles.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            enum_data.append(row['title'])  # Replace 'title' with the actual column name in your CSV file
    return enum_data

if __name__ == '__main__':
    app.run()