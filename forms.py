from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
class ContactForm(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    subject = StringField("Subject")
    message = StringField("Message")
    submit = SubmitField("Send")