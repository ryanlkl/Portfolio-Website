from flask import Flask, render_template, redirect, url_for
from wtforms import StringField, EmailField, SubmitField
from flask_wtf import FlaskForm
from flask_wtf.file import DataRequired
from flask_ckeditor import CKEditorField, CKEditor
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.config["SECRET_KEY"] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

class ContactForm(FlaskForm):
  name = StringField("Name",validators=[DataRequired()])
  email = EmailField("Email",validators=[DataRequired()])
  message = CKEditorField("Message",validators=[DataRequired()])
  submit = SubmitField("Send")

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/contact",methods=["GET","POST"])
def contact():
  form = ContactForm()
  return render_template("contact.html",form=form)

if __name__ == "__main__":
  app.run(debug=True)
