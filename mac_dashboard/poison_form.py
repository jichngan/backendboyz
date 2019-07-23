from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired
class SubmissionForm(FlaskForm):
  ipaddress = StringField('IP Address', validators = [DataRequired()])
  submit = SubmitField('Confirm your IP Address')

