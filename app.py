from flask import Flask, render_template

app = Flask(__name__, template_folder='E:/reposD/MovieReccomender/views')
app.debug = True

@app.route('/')

def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()