from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float,desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
# api_key="d366a11d349469acb489a388416ed43d"
# api_access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMzY2YTExZDM0OTQ2OWFjYjQ4OWEzODg0MTZlZDQzZCIsIm5iZiI6MTcyMzUyNjIwNi44MTE4NTIsInN1YiI6IjY2YjYwZDdmNDI1ZTE3YzUzZjAxNWQ4MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lGuUUOxCHrTJECWWcmwQCmpvA8PtuUd2ewJ71TZyJZM"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class Editform(FlaskForm):
    rating = StringField("Rating out of 10.Eg:7.5", [DataRequired()])
    review = StringField("Your review", [DataRequired()])
    submit = SubmitField("submit")

class AddMovie(FlaskForm):
    movie_name = StringField("Movie Name",[DataRequired()])
    add_movie = SubmitField("Add Movie")
# CREATE DB
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///favorite_movie.db"

db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500),nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer,nullable=True)
    review: Mapped[str] = mapped_column(String(250),nullable=True)
    img_url: Mapped[str] = mapped_column(String(250),nullable=True)

    def __repr__(self):
        return f"<Movie {self.title}>"


with app.app_context():
    db.create_all()

new_movie = Movie(
    title="Phone Booth",
    year=2002,
    description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    rating=7.3,
    ranking=10,
    review="My favourite character was the caller.",
    img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
)
second_movie = Movie(
    title="Avatar The Way of Water",
    year=2022,
    description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    rating=7.3,
    ranking=9,
    review="I liked the water.",
    img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
)

#
# with app.app_context():
#     db.session.add(second_movie)
#     db.session.add(new_movie)
#     db.session.commit()


@app.route("/")
def home():

    # all_movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()
    # for i in range(len(all_movies)):
    #     all_movies[i].ranking = len(all_movies)-i
    all_movies = db.session.execute(db.select(Movie).order_by(desc(Movie.rating))).scalars().all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = i+1
    db.session.commit()
    return render_template("index.html", all_movies=all_movies)


@app.route("/edit",methods=["GET","POST"])
def edit():
    id = request.args.get('id')
    edit_form = Editform()
    with app.app_context():
        movie = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
    # movie = db.get_or_404(Movie,id)
    if edit_form.validate_on_submit():
        with app.app_context():
            movie = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
            movie.rating = float(edit_form.rating.data)
            movie.review = edit_form.review.data
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html',movie=movie,editform=edit_form)

@app.route('/delete')
def delete():
    id = request.args.get('id')
    with app.app_context():
        movie = db.get_or_404(Movie,id)
        db.session.delete(movie)
        db.session.commit()
    return redirect(url_for('home'))

omdb_url = "https://www.omdbapi.com/"
omdb_api_key ="ffa5a3d8"

@app.route('/add',methods=["POST","GET"])
def add():
    add_form = AddMovie()
    if add_form.validate_on_submit():
        movie_name = add_form.movie_name.data
        params = {
            "s":movie_name,
            "apikey":omdb_api_key,
        }
        result = requests.get(omdb_url,params=params).json()["Search"]
        return  render_template('select.html',movies=result)
    return render_template('add.html',add_form=add_form)

@app.route('/add_movie/<title>')
def add_movie(title):
    params = {
        "t":title,
        "apikey":omdb_api_key,
    }
    result = requests.get(omdb_url,params=params).json()
    print(result)
    new_movie = Movie(
        title=result["Title"],
        year =result["Year"],
        description = result["Plot"],
        rating = result["imdbRating"],
        img_url=result["Poster"],
    )
    db.session.add(new_movie)
    db.session.commit()
    movie_by_id = db.session.execute(db.select(Movie).where(Movie.title==title)).scalar()
    #here scalar() is imp
    return redirect(url_for('edit',id=movie_by_id.id))
if __name__ == '__main__':
    app.run(debug=False)
