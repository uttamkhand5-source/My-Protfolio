from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import SiteSettings, Skill, Project, Experience, Certificate, BlogPost, Message

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html",
        skills=Skill.query.order_by(Skill.level.desc()).all(),
        projects=Project.query.filter_by(featured=True).order_by(Project.id.desc()).all(),
        experiences=Experience.query.order_by(Experience.id.desc()).all(),
        certificates=Certificate.query.order_by(Certificate.id.desc()).all(),
        posts=BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).limit(3).all()
    )

@main_bp.route("/project/<int:project_id>")
def project(project_id):
    p = Project.query.get_or_404(project_id)
    return render_template("project.html", project=p)

@main_bp.route("/blog/<slug>")
def blog(slug):
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    return render_template("blog.html", post=post)

@main_bp.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name","").strip()
    email = request.form.get("email","").strip()
    subject = request.form.get("subject","").strip()
    message = request.form.get("message","").strip()
    if not name or not email or not message:
        flash("Please fill in your name, email and message.", "error")
        return redirect(url_for("main.index") + "#contact")
    db.session.add(Message(name=name, email=email, subject=subject, message=message))
    db.session.commit()
    flash("Message sent successfully!", "success")
    return redirect(url_for("main.index") + "#contact")
