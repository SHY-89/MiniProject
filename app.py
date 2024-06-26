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

# Flask 애프리케이션에서 데이터베이스를 초기화하거나 생성할 때 사용되는 코드. Flask 애플리케이션 컨텍스트 내에서 데이터베이스 모델을 생성하거나 업데이트 하는 역할을 한다
with app.app_context(): # 애플리케이션 컨텍스트를 사용하여 애플리케이션 전체에서 현재 애플리케이션 객체와 데이터베이스 연결을 쉽게 접근 할 수 있다.
    db.create_all() #클래스에 담긴 모든 데이터베이스 테이블을 생성


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

    user_list = Users.query.all()  ## user_list에 Users DB에 있는 모든 정보를 저장
    return redirect(url_for('index',user=user_list))  # index에 user_list 정보를 전달

@app.route("/user/del/<int:id>", methods=['GET'])
def user_del(id):
    try:
        del_user = Users.query.get_or_404(id) ## id를 조회
        db.session.delete(del_user)
        db.session.commit()
    except Exception as e:  ## id가 없으면
        db.session.rollback() ## 변경사항 롤백
        app.logger.error(f"An error occurred: {str(e)}")  ##에러를 로그에 기록
        return "An error occurred", 500  ## 사용자에게 500 서버 오류 반환
    finally:  ## 예외처리와 관계없이
        db.session.close() ##데이터베이스 세션 close
    
    return redirect(url_for('index'))

@app.route('/document/<int:id>')
def document(id):
    user = Users.query.get_or_404(id)
    return render_template('document.html', user=user)
# post는 데이터를 서버로 제출하여 리소스를 생성하거나 업데이트하는데 사용되며, HTTP 요청의 본문에 데이터를 포함하여 전송. 보안적으로 더 안전하고, 길이 제한이 없다.
# 데이터베이스의 변화를 주는 작업은 POST, 단순히 데이터를 조회하는작업은 GET
@app.route('/user/edit/<int:id>', methods=['POST'])
def user_edit(id):
    user = Users.query.get_or_404(id)
    
    # form에서 보낸 데이터 받아오기
    # request.form.get() 메서드를 사용할때 뒤에 고유한 id 값을 추가하면 특정 input id 값을 가져올수 있다.
    name_receive = request.form.get("edit-recipient-name" + str(id))
    oneline_receive = request.form.get("edit-recipient-oneline" + str(id))
    mbti_receive = request.form.get("edit-recipient-mbti" + str(id))
    good_receive = request.form.get("edit-recipient-good" + str(id))
    about_receive = request.form.get("edit-recipient-about" + str(id))
    promise_receive = request.form.get("edit-recipient-promise" + str(id))
    blog_receive = request.form.get("edit-recipient-blog" + str(id))

    # 데이터를 DB에 업데이트하기
    user.name = name_receive
    user.oneline = oneline_receive
    user.mbti = mbti_receive
    user.good = good_receive
    user.about = about_receive
    user.promise = promise_receive
    user.blogurl = blog_receive

    db.session.commit()

    user_list = Users.query.all()
    return redirect(url_for('index', user=user_list))




if __name__ == '__main__':
    app.run(debug=True)