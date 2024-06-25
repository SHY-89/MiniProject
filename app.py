from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# DB 기본 코드

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    oneline = db.Column(db.String(100), nullable=False)
    mbti = db.Column(db.String(100), nullable=False)
    good = db.Column(db.String(100), nullable=False)
    about = db.Column(db.String(100), nullable=False)
    promise = db.Column(db.String(100), nullable=False)
    blogurl = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f'{self.name} {self.oneline} {self.mbti}'


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    user_list = Users.query.all()
    
    return render_template('index.html',user=user_list)


@app.route("/user/create/")
def user_create():
    # form에서 보낸 데이터 받아오기
    name_receive = request.args.get("recipient-name")
    oneline_receive = request.args.get("recipient-oneline")
    mbti_receive = request.args.get("recipient-mbti")
    good_receive = request.args.get("recipient-good")
    about_receive = request.args.get("recipient-about")
    promise_receive = request.args.get("recipient-promise")
    blog_receive = request.args.get("recipient-blog")

    # 데이터를 DB에 저장하기
    users = Users(name=name_receive, oneline=oneline_receive, mbti=mbti_receive,
                  good=good_receive, about=about_receive, promise=promise_receive, blogurl=blog_receive)
    db.session.add(users)
    db.session.commit()

    user_list = Users.query.all()
    return redirect(url_for('index',user=user_list))


@app.route('/document/<int:id>')
def document(id):
    user = Users.query.get_or_404(id)
    return render_template('document.html', user=user)


if __name__ == '__main__':
    app.run()
