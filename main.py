from flask import Flask, render_template, redirect, url_for, flash
from wtforms import StringField, EmailField, SubmitField
from flask_wtf import FlaskForm
from flask_wtf.file import DataRequired
from flask_ckeditor import CKEditorField, CKEditor
from flask_bootstrap import Bootstrap
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)

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
  if form.validate_on_submit():
    smtp_server = "smtp.gmail.com"
    sender_email = os.environ.get("EMAIL")
    sender_password = os.environ.get("PASSWORD")

    try:
      with smtplib.SMTP(smtp_server) as connection:
        connection.starttls()
        connection.login(user=sender_email,password=sender_password)
        connection.sendmail(
          from_addr=sender_email,
          to_addrs=os.environ.get("PERSONAL_EMAIL"),
          msg=f"Subject:New Message from {form.name.data}\n\n{form.email.data}:\n{form.message.data}"
        )
      flash("Form submitted successfully")
      return redirect(url_for("contact", error=False))
    except Exception as e:
      flash(e)
      return redirect(url_for("contact", error=True))

  return render_template("contact.html",form=form)

if __name__ == "__main__":
  app.run(debug=True)
