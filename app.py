from forms import AddPet
from flask import Flask, redirect, render_template, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet

app = Flask(__name__)

app.config["SECRET_KEY"] = "whatsthemagicword"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def pet_list():
   """Shows a list of pets for adoption"""
   pets = Pet.query.order_by(Pet.name)
   return render_template('homepage.html', pets=pets)

@app.route("/add", methods=["GET"])
def show_pet_form():
   """Shows the pet form"""

   form = AddPet()

   return render_template("pet_add_form.html", form=form)

@app.route("/add", methods=["POST"])
def add_pet():
   """Handles the pet form on submit"""
   form = AddPet()

   if form.validate_on_submit():
      name = form.name.data
      species = form.species.data
      photo_url = form.photo_url.data
      age = form.age.data
      notes = form.notes.data
      flash(f"Success! {name} was added to be adopted!")
      pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
      db.session.add(pet)
      db.session.commit()
      return redirect("/add")

   else:
      return render_template("pet_add_form.html", form=form)

@app.route('/profile/<int:id>')
def pet_profile(id):
   """Shows pet profile"""
   pet = Pet.query.get(id)
   

   return render_template('pet_profile.html', pet=pet)

@app.route('/profile/<int:id>/edit', methods=["GET", "POST"])
def pet_edit_form(id):
   """Shows and edits the form for the pet profile"""
   pet = Pet.query.get_or_404(id)

   form = AddPet(obj=pet)

   
   if form.validate_on_submit():
      pet.name = form.name.data
      pet.species = form.species.data
      pet.photo_url = form.photo_url.data
      pet.age = form.age.data
      pet.notes = form.notes.data
      flash(f"Success! {pet.name} was edited!")
      db.session.commit()
      return redirect(f"/profile/{id}/edit")
   else:
      return render_template('pet_edit.html', form=form, pet=pet)


