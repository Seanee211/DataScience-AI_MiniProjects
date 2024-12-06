from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib
import mariadb as mdb
from datetime import timedelta
from final_implementation import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=20)  # 실제로는 보안에 유의하여 비밀키를 설정해야 함

# 이 부분은 실제 데이터베이스 연결에 대한 코드로 대체되어야 함
conn_params = {
    'host':'172.20.45.19',
    'user':'root',
    'password':'root',
    'port':3306,
    'db':'db_ai',
    'autocommit':True
}

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['password_confirm']
        email = request.form['email']

        if password != confirm_password:
            flash("비밀번호가 맞지 않습니다")
            return redirect(url_for('signup'))

        # SHA-256 메서드를 이용한 비밀번호 해쉬
        hash_object = hashlib.sha256(password.encode())
        password_hash = hash_object.hexdigest()

        db_conn = mdb.connect(**conn_params)
        cursor = db_conn.cursor()

        add_user = ("INSERT INTO users(username, password_hash, email) VALUES (%s, %s, %s)")

        data_user = (username, password_hash, email)
        
        cursor.execute(add_user,data_user)

         # 데이터베이스로 커밋
        db_conn.commit()
        
        cursor.close()
        db_conn.close()
        
        flash("회원가입 완료되었습니다.")
        return redirect(url_for('login'))
    return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('_flashes', None)

    if request.method == "POST":
        username=request.form.get("username")
        password=request.form.get("password")
        hash_object=hashlib.sha256(password.encode())
        hashed_password=hash_object.hexdigest()

        conn=mdb.connect(**conn_params)
        cur=conn.cursor()
        
        cur.execute("SELECT * FROM users WHERE username=%s",(username,))
        
        user=cur.fetchone() 
          
        if user and user[2] == hashed_password:  # user[2]는 비밀번호 해시가 저장된 열입니다.
            session.permanent = True
            session["user"]=user[1]

            flash("로그인이 완료되었습니다.")
            return redirect(url_for("index"))
    return render_template('login.html')


@app.route('/logout')
def logout():
     session.pop('user', None)
     flash('로그아웃 하셨습니다')
     return redirect(url_for('index'))

@app.route('/keyword', methods=['GET', 'POST'])
def keyword():
    return redirect(url_for('index'))

@app.route('/estimate_price', methods=['GET', 'POST'])
def estimate_price():
    return redirect(url_for('input_data'))


@app.route('/predict', methods=['POST'])
def predict():
    keyword = request.form.get('keyword')  # 사용자로부터 키워드 받기
    prediction = data_predict(keyword)  # 모델링 함수에 키워드 전달하여 예측 수행
    return render_template('prediction.html', prediction=prediction)  # 결과를 HTML 페이지에 전달


app.run()
