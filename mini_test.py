from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <body>
        <h1>最小測試</h1>
        <p>學號：411211325</p>
        <p>授課教師：楊子青</p>
        <a href="/test">測試連結</a>
    </body>
    </html>
    """

@app.route('/test')
def test():
    return "測試頁面 - 學號：411211325 授課教師：楊子青"

if __name__ == '__main__':
    app.run(port=5005) 