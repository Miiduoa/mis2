from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Flask測試成功!</h1><p>這是一個簡單的Flask應用</p>"

if __name__ == '__main__':
    app.run(debug=True) 