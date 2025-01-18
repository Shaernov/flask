from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attempt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts')
def posts():
    articles = Articles.query.order_by(Articles.date.desc()).all()
    return render_template('posts.html', articles=articles)

@app.route('/posts/<int:id>')
def post_detail(id):
    article = db.session.get(Articles, id)
    return render_template('post_detail.html', article=article)

@app.route('/posts/<int:id>/delete')
def post_delete(id):
    articles = Articles.query.get_or_404(id)

    try:
        db.session.delete(articles)
        db.session.commit()
        return redirect("/posts")
    except Exception as e:
            return f"При удалении статьи произошла ошибка {str(e)}"

@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = db.session.get(Articles, id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

  
        try:
            db.session.commit()
            return redirect("/posts")
        except Exception as e:
            return f"При обновлении статьи произошла ошибка {str(e)}"
    else:
        return render_template('post_update.html', article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        titl = request.form['title']
        intr = request.form['intro']
        tex = request.form['text']

        new_object = Articles(title=titl, intro=intr, text=tex)

        try:
            db.session.add(new_object)
            db.session.commit()
            return redirect("/posts")
        except Exception as e:
            return f"При добавлении статьи произошла ошибка {str(e)}"
    else:
        return render_template("create-article.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)