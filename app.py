from flask import Flask, render_template, request
import csv
from algorytm_new import find_most_similar_film

app = Flask(__name__, template_folder='views')
app.debug = True

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        selected_value = request.form.get('my-select')
        return f'Selected value: {selected_value}'

    enum_data = read_csv()
    return render_template('base.html', enum_data=enum_data)

def generate_data(selected_value):
    return f'Generated data for {selected_value}'

@app.route('/solution', methods=['GET','POST'])
def solution():
    selected_value = request.form.get('my-select')
    generate_datar = find_most_similar_film(selected_value)
    return render_template('solution.html', generate_data=generate_datar, selected_value=selected_value)

@app.route('/about')  # Nowy routing dla '/about'
def about():
    return render_template('about.html')

# -----> 14.06.2023 - Zmiana bazy danych na nową movies_5000 <-------
def read_csv():
    enum_data = []  # This list will store the extracted enum values
    with open('movies_5000.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            enum_data.append(row['title'])  # Replace 'title' with the actual column name in your CSV file
    return enum_data

if __name__ == '__main__':
    app.run()