from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), default="Your Name")
    role = db.Column(db.String(160), default="Developer")
    tagline = db.Column(db.Text, default="")
    about = db.Column(db.Text, default="")
    email = db.Column(db.String(160), default="")
    location = db.Column(db.String(160), default="")
    github = db.Column(db.String(255), default="")
    linkedin = db.Column(db.String(255), default="")
    instagram = db.Column(db.String(255), default="")
    profile_image = db.Column(db.String(255), default="")

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, default=70)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(255), default="")
    image = db.Column(db.String(255), default="")
    github_url = db.Column(db.String(255), default="")
    live_url = db.Column(db.String(255), default="")
    featured = db.Column(db.Boolean, default=True)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    company = db.Column(db.String(160), default="")
    period = db.Column(db.String(100), default="")
    description = db.Column(db.Text, default="")

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    issuer = db.Column(db.String(160), default="")
    year = db.Column(db.String(20), default="")
    url = db.Column(db.String(255), default="")

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    excerpt = db.Column(db.Text, default="")
    content = db.Column(db.Text, default="")
    published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False)
    subject = db.Column(db.String(200), default="")
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    read = db.Column(db.Boolean, default=False)
