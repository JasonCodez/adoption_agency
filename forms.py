from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Optional, NumberRange, URL, AnyOf

class AddPet(FlaskForm):
   """Form to add a pet"""

   name = StringField("Pet name", validators=[InputRequired()])
   species = StringField("Species", validators=[AnyOf(values=["cat", "dog", "porcupine"], message="We're only accepting Cats, Dogs and Porcupines at the current time")])
   photo_url = StringField("Photo URL", validators=[URL(), Optional()])
   age = IntegerField("Age", validators=[NumberRange(min=0, max=30, message="Please enter a number between 0 and 30")])
   notes = StringField("Notes")