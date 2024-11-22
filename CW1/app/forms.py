from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class AssessmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    module_code = StringField('Module Code', validators=[DataRequired()])
    deadline = DateField('Deadline', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    is_completed = BooleanField('Completed')
