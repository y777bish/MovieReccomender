from flask import Flask, render_template, request
import csv

app = Flask(__name__, template_folder='views')
app.debug = True

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        selected_value = request.form.get('my-select')
        return f'Selected value: {selected_value}, \t Rob Leser'

    enum_data = read_csv()
    return render_template('index.html', enum_data=enum_data)



# -----> 14.06.2023 - Zmiana bazy danych na nową movies_5000 <-------
def read_csv():
    enum_data = []  # This list will store the extracted enum values
    with open('movies_5000.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            enum_data.append(row['title'])  # Replace 'title' with the actual column name in your CSV file
    return enum_data



# ----> W przyszłości kiedyś tu może będzie algorytm albo nie xD (c) Szlugenko <------
def generate_data(selected_value):
    # Add your data generation logic here based on the selected value
    # This is just a placeholder
    return f'Generated data for {selected_value}'




if __name__ == '__main__':
    app.run()