from flask.ext.wtf import Form
 
from wtforms_alchemy import model_form_factory
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

 
from server import db
from model import User, Post
 
BaseModelForm = model_form_factory(Form)
 
class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session
 
class UserCreateForm(ModelForm):
    class Meta:
        model = User
    submit = SubmitField(("Login"))
 
class SessionCreateForm(Form):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
 
class PostCreateForm(ModelForm):
    class Meta:
        model = Post