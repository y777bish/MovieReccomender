from flask import Flask, render_template, request
import csv

app = Flask(__name__, template_folder=r'C:\projektSSI\MovieReccomender\views')
app.debug = True

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        selected_value = request.form.get('my-select')
        return f'Selected value: {selected_value}'

    enum_data = read_csv()
    return render_template('index.html', enum_data=enum_data)

def read_csv():
    enum_data = []  # This list will store the extracted enum values
    with open('movies.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            enum_data.append(row['title'])  # Replace 'title' with the actual column name in your CSV file
    return enum_data






if __name__ == '__main__':
    app.run()