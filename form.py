from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


class UserAddress(FlaskForm):
    user = SelectField('User', coerce=int)
    number = StringField('Number', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Add Address')

'''
class UserStatus(FlaskForm):
    status = SelectField('Status', choices=[('Registered', 'Registered'), ('Pending', 'Pending'), ('Not Registered', 'Not Registered'), ('Left', 'Left')])
    submit = SubmitField('Update Status')
'''
