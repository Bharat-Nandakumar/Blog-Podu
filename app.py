from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

    def __init__(self, title, subtitle, author, date_posted, content):
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.date_posted = date_posted
        self.content = content

@app.route("/")
def index():
    posts=Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template("index.html",posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    date_posted=post.date_posted.strftime('%B %d, %Y')
    return render_template("post.html",post = post,date_posted = date_posted)

@app.route('/add')
def add():
    return render_template("add.html")

@app.route('/addpost',methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title = title, subtitle=subtitle, author=author, content=content,date_posted=datetime.now())
    db.session.add(post)
    db.session.commit()
    return redirect (url_for('index'))  

@app.route('/updatepost/<int:post_id>')
def updatepost(post_id):
    return render_template("update.html",post_id = post_id)


@app.route('/update/<int:post_id>',methods=['POST'])
def update(post_id):
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    up_post = Blogpost.query.filter_by(id=post_id).one()
    up_post.title = title
    up_post.subtitle = subtitle
    up_post.author = author
    up_post.content = content
    up_post.date_posted = datetime.now()
    db.session.commit()
    return redirect (url_for('index')) 


@app.route('/delete/<int:delpost_id>',methods=['POST','GET'])
def delete(delpost_id):
    del_post = Blogpost.query.filter_by(id=delpost_id).one()
    db.session.delete(del_post)
    db.session.commit()
    return redirect (url_for('index')) 


 
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)