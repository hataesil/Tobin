import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myapp.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False         

db = SQLAlchemy(app)                                         

db.init_app(app)                                             

class Post(db.Model):                                        
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)             
    title = db.Column(db.String, nullable=False)             
    content = db.Column(db.String, nullable=False)

class Comment(db.Model):
    __tablename__ = "comments" #테이블 이름 설정
    id = db.Column(db.Integer, primary_key=True)
    content =  db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), 
        nullable=False)
        
db.create_all()                                            


@app.route("/")
def index():
    #myapp.db에 있는 모든 레코드를 불러와
    #보여준다.
    #SELECT*FROM posts;
    posts = Post.query.all()        #posts는 list type이다.
    comments = Comment.query.all()
    return render_template('index.html', posts = reversed(posts), comments = comments) # reversed(posts) -> 글들 반대로 보이게 하는 것
    
@app.route("/create")
def create():
    title = request.args.get('title')
    content = request.args.get('content')
    post = Post(title=title, content=content)
    db.session.add(post)
    db.session.commit()
    return redirect("/")
    # return render_template('create.html', title=title, content=content) -> 이거말고 홈인 index.html로 돌아가게 하자

@app.route("/edit/<int:id>")
def edit(id):
    # 1. 수정하려고 하는 레코드를 선택하여
    post = Post.query.get(id)
    # 2. 수정을 하고
    # post.title = "수정하셈"
    # post.content = "수정하셈"
    # 3. 커밋한다.
    return render_template('edit.html', post=post)

    
@app.route("/update/<int:id>")
def update(id):
    # 1. 수정하려고 하는 레코드를 선택하여
    post = Post.query.get(id)
    # 2. 수정을 하고
    post.title = request.args.get('title')
    post.content = request.args.get('content')
    # 3. 커밋한다.
    db.session.commit()
    return redirect('/')

@app.route("/delete/<int:id>")  #동적 변환 <> 사용
def delete(id): #id는 string으로 parse됨 int()이렇게 써도 되지만 위에 <int:id>로 한번에 써도됨
    #1. 지우려고 하는 레코드를 선택하여
    post = Post.query.get(id)    #()안에 해당 data primary
    #2. 지운다.
    db.session.delete(post)
    #3. 확정하고 DB에 반영한다. Commit
    db.session.commit()
    return redirect("/")

@app.route("/create_comment")
def comment_content():
    #Comment 테이블에 입력받은 내용을 저장한다.
    content = request.args.get('comment_content') # /comment_content로 날라온 파라미터 잡기
    post_id = int(request.args.get('post_id')) 
    comment = Comment(content=content, post_id = post_id)
    #위에 코드까지 객체 생성을 통해 하나의 행을 만든 것
    db.session.add(comment)
    db.session.commit()
    return redirect('/') 
    
    
    

#url 간단하게 줄이는 방법, 이런 식으로
# @app.route("</name>")
# def redirection(name):
#     url =URL.query.filter_by(name=name)
#     return redirect(url.rul)

#app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug = True)


#python3에서 댓글이 db에 저장됬는지 확인
#from app import Comment #기능 import
#comments = Comment.query.all() # 댓글 쓴 것 comments 변수에 저장
#comments[0] 으로 댓글 들어갔는지 확인
#comments[0].content로 안에 들어있는 댓글 코멘트 출력
