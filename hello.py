from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World! 學號：411211325 授課教師：楊子青"

if __name__ == '__main__':
    app.run(port=5006) 