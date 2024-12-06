# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
# db = SQLAlchemy(app)

# class User(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   username = db.Column(db.String(80), unique=True)
#   password = db.Column(db.String(120))  # 실제로는 해싱된 비밀번호를 저장해야 합니다.

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#   if request.method == 'POST':
#       username = request.form['username']
#       password = request.form['password']

#       user = User(username=username, password=password)  # 해싱되지 않은 비밀번호 저장 - 실제로는 이렇게 하면 안 됩니다.
#       db.session.add(user)
#       db.session.commit()

#       return redirect(url_for('login'))
#   return render_template('signup.html')

# if __name__ == '__main__':
#     app.run(debug=True)
