from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ArticleImportForm(FlaskForm):
    category_name = StringField('Category ', validators=[DataRequired(),
                                Length(min=2, max=100)])
    submit = SubmitField()
