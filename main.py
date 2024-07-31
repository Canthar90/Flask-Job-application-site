from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import dotenv
import os
from datetime import datetime as dt


dotenv.load_dotenv()
secret_key = os.getenv("SECRET_KEY")
database_type = os.getenv("DATABASE_TYPE")
email_pass = os.getenv("EMAIL_PASS")
email_user = os.getenv("EMAIL_USERNAME")
email_server = os.getenv("MAIL_SERVER")
email_port = os.getenv("MAIL_PORT")

app = Flask(__name__)

app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = database_type
app.config["MAIL_PORT"] = email_port
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_SERVER"] = email_server
app.config["MAIL_USERNAME"] = email_user
app.config["MAIL_PASSWORD"] = email_pass
db = SQLAlchemy(app)

mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))

    

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = dt.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        form = Form(first_name=first_name, last_name=last_name,
                     email=email, date=date_obj, occupation=occupation)
        
        db.session.add(form)
        db.session.commit()

        message_body = f"Then you for your submission: {first_name} {last_name}"\
                        f"Here are your data: {first_name}\n{last_name}\n{occupation}\n, {date}"

        message = Message(subject="New for sumbmission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)
        
        mail.send(message)
        
        flash("Your form was submitted successfully", "success")
    
    
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)