from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return "Hello, World! 這是一個簡單的測試頁面!"

if __name__ == '__main__':
    app.run(debug=True) 