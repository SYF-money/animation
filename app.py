from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话管理，请替换为你的密钥

# 模拟的用户数据库
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('用户名已存在，请选择其他用户名。')
        else:
            users[username] = password
            flash('注册成功！请登录。')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            flash('登录成功！')
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误。')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return f'欢迎，{session["username"]}！这是你的仪表盘。'

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('你已注销。')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)