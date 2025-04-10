from flask import Flask, render_template_string, url_for

app = Flask(__name__)

@app.route('/')
def home():
    links = [
        {'name': '登入', 'url': url_for('login')},
        {'name': '儀表板', 'url': url_for('dashboard')}
    ]
    
    links_html = ''.join([f'<li><a href="{link["url"]}">{link["name"]}</a></li>' for link in links])
    
    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>測試頁面 - 411211325</title>
    </head>
    <body>
        <h1>Flask 測試頁面</h1>
        <p>學號：411211325</p>
        <p>授課教師：楊子青</p>
        <ul>
            {links_html}
        </ul>
    </body>
    </html>
    """)

@app.route('/login')
def login():
    return "登入頁面成功! 學號：411211325 授課教師：楊子青"

@app.route('/dashboard')
def dashboard():
    return "儀表板頁面成功! 學號：411211325 授課教師：楊子青"

if __name__ == '__main__':
    app.run(debug=True, port=5003) 