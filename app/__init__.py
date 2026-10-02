import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(os.path.join(app.root_path, "static", "uploads"), exist_ok=True)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "portfolio.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_site():
        from app.models import SiteSettings
        return {"site": SiteSettings.query.first()}

    @app.errorhandler(404)
    def not_found(error):
        from flask import render_template
        return render_template("404.html"), 404

    with app.app_context():
        db.create_all()
        seed_data()

    return app

def seed_data():
    from app.models import User, SiteSettings, Skill, Project, Experience, Certificate, BlogPost
    from werkzeug.security import generate_password_hash

    if not User.query.filter_by(username=os.getenv("ADMIN_USERNAME", "admin")).first():
        db.session.add(User(
            username=os.getenv("ADMIN_USERNAME", "admin"),
            password_hash=generate_password_hash(os.getenv("ADMIN_PASSWORD", "admin123"))
        ))

    if not SiteSettings.query.first():
        db.session.add(SiteSettings(
            name="Uttam Khand",
            role="Python & Web Developer",
            tagline="I build beautiful, useful and secure digital experiences.",
            about="I am a student and developer who enjoys building websites, Python applications and cybersecurity projects.",
            email="hello@example.com",
            location="Nepal",
            github="https://github.com/",
            linkedin="https://linkedin.com/",
            instagram="https://instagram.com/"
        ))

    if Skill.query.count() == 0:
        for name, level in [("Python",90),("Flask",85),("HTML",95),("CSS",90),("JavaScript",75),("C",70),("Cybersecurity",78)]:
            db.session.add(Skill(name=name, level=level))

    if Project.query.count() == 0:
        samples = [
            ("Uttam's Board","A modern screen annotation and whiteboard application.","Python, Tkinter","", "github"),
            ("Cyber Insight","A cybersecurity awareness and learning website.","Flask, HTML, CSS, JavaScript","", "github"),
            ("Student Management System","A terminal-based student management application with authentication.","Python, SQLite","", "github")
        ]
        for title, desc, tech, image, linktype in samples:
            db.session.add(Project(title=title, description=desc, technologies=tech, image=image, github_url="https://github.com/"))

    if Experience.query.count() == 0:
        db.session.add(Experience(title="Student Developer", company="Personal Projects", period="2025 — Present",
                                  description="Building Flask websites, Python applications and cybersecurity learning projects."))

    if Certificate.query.count() == 0:
        db.session.add(Certificate(title="Python & Web Development", issuer="Personal Learning", year="2026"))

    if BlogPost.query.count() == 0:
        db.session.add(BlogPost(title="Welcome to my portfolio", slug="welcome-to-my-portfolio",
                                excerpt="A short introduction to this Flask-powered portfolio.",
                                content="Welcome! This portfolio is built with Flask, SQLite, HTML, CSS and JavaScript.",
                                published=True))

    db.session.commit()
