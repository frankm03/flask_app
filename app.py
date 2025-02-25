from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "supersecretkey123"  # ✅ Add a unique secret key


# ✅ Database Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get project directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids warnings

db = SQLAlchemy(app)  # ✅ Make sure this is included

# ✅ Create a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

@app.route('/')
def home():
    return render_template('index.html') # Load from templates

@app.route('/about')
def about():
    return render_template('about.html') # Load from templates

@app.route('/contact')
def contact():
    return render_template('contact.html') # Load from templates

@app.route("/users")
def users():
    users_list = User.query.all()  # Fetch all users from the database
    return render_template("users.html", users=users_list)

# ✅ Route for the Registration Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        # ✅ Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Try another!", "danger")
            return redirect(url_for("register"))

        # ✅ Add the new user
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()

        flash("User registered successfully!", "success")
        return redirect(url_for("users"))  # Redirect to users page after registration

    return render_template("register.html")

@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully!", "success")
    else:
        flash("User not found!", "danger")

    return redirect(url_for("users"))  # Redirect back to users page

if __name__ == '__main__':
    app.run(debug=True)

