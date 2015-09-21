from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, DateTimeField, HiddenField
from wtforms.validators import Required


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class TimePickerForm(Form):
    storeid = StringField('Store', validators=[Required()])
    dishid = StringField('Dish', validators=[Required()])
    time = DateTimeField('Time', format='%m/%d/%Y %H:%M', validators=[Required])
    submit = SubmitField('Submit')

class StateUpdateForm(Form):
	state = HiddenField('State')
	submit = SubmitField('Submit')