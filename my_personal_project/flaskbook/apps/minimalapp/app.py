from flask import Flask, render_template, url_for, current_app, g, flash, make_response, session
from flask import request, redirect
from email_validator import validate_email, EmailNotValidError

# Flask 객체 생성 => Web Server 기능의 객체 생성
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello Flaskbook! Second'

@app.route('/hello/<name>', methods=['GET', 'POST'], endpoint="hello-endpoint")
def hello(name):
    return f'hello {name}'

@app.route("/name/<erum>")
def show_name(erum):
    return render_template('index.html', name=erum)

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('hello-endpoint', name='soojin'))
#     print(url_for('show_name', erum='lol', page='1'))

# with app.test_request_context("users?updated=true"):
#     print(request.args.get("updated"))

@app.route("/contact")
def contact():
    response = make_response(render_template("contact.html"))
    response.set_cookie("flaskbook key", "flaskbook value")
    session['username'] = 'Seanlee'

    return response

@app.route("/contact/complete", methods=["GET", 'POST'])
def contact_complete():
    if request.method=="POST":
        username = request.form['username']
        email = request.form['email']
        description = request.form['description']

        # 이메일 보내는 건 나중에 구현할 부분

        #입력 체크
        is_valid=True

        if not username:
            flash('사용자명은 필수 입니다')
            is_valid = False

        if not email:
            flash('메일 주소는 필수 입니다')
            is_valid = False

        # try:
        #     validate_email(email)
        # except EmailNotValidError:
        #     flash('메일 주소의 형식으로 입력해주세요')
        #     is_valid = False

        if not description:
            flash('문의 내용은 필수입니다')
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        flash('문의해주셔서 감사합니다')
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")

app.config['SECRET_KEY'] = "2AZSMss3p5QPbcY2hBs"
