import os, uuid
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from app import db
from app.models import SiteSettings, Skill, Project, Experience, Certificate, BlogPost, Message, User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def save_upload(file):
    if not file or not file.filename:
        return ""
    allowed = {"png", "jpg", "jpeg", "gif", "webp", "pdf"}
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in allowed:
        return ""

    # The browser cropper replaces the file input with the cropped image bytes.
    # Save those bytes directly: do not resize, crop, or apply object-fit on the
    # server, so the stored image is exactly the image the user submitted.
    name = secure_filename(uuid.uuid4().hex + "." + ext)
    destination = os.path.join(current_app.config["UPLOAD_FOLDER"], name)
    file.save(destination)
    return name

@admin_bp.route("/")
@login_required
def dashboard():
    return render_template("admin/dashboard.html",
        projects=Project.query.count(), skills=Skill.query.count(),
        messages=Message.query.count(), posts=BlogPost.query.count(),
        unread=Message.query.filter_by(read=False).count()
    )

@admin_bp.route("/settings", methods=["GET","POST"])
@login_required
def settings():
    s = SiteSettings.query.first()
    if request.method == "POST":
        for field in ["name","role","tagline","about","email","location","github","linkedin","instagram"]:
            setattr(s, field, request.form.get(field,"").strip())
        upload = save_upload(request.files.get("profile_image"))
        if upload: s.profile_image = upload
        db.session.commit()
        flash("Settings updated.", "success")
        return redirect(url_for("admin.settings"))
    return render_template("admin/settings.html", item=s)

@admin_bp.route("/projects")
@login_required
def projects():
    return render_template("admin/projects.html", items=Project.query.order_by(Project.id.desc()).all())

@admin_bp.route("/projects/new", methods=["GET","POST"])
@admin_bp.route("/projects/<int:id>/edit", methods=["GET","POST"])
@login_required
def project_form(id=None):
    item = Project.query.get_or_404(id) if id else Project()
    if request.method == "POST":
        item.title=request.form.get("title","").strip()
        item.description=request.form.get("description","").strip()
        item.technologies=request.form.get("technologies","").strip()
        item.github_url=request.form.get("github_url","").strip()
        item.live_url=request.form.get("live_url","").strip()
        item.featured=bool(request.form.get("featured"))
        upload=save_upload(request.files.get("image"))
        if upload: item.image=upload
        if not id: db.session.add(item)
        db.session.commit()
        flash("Project saved.", "success")
        return redirect(url_for("admin.projects"))
    return render_template("admin/project_form.html", item=item)

@admin_bp.route("/projects/<int:id>/delete", methods=["POST"])
@login_required
def project_delete(id):
    db.session.delete(Project.query.get_or_404(id)); db.session.commit()
    flash("Project deleted.", "success")
    return redirect(url_for("admin.projects"))

@admin_bp.route("/skills", methods=["GET","POST"])
@login_required
def skills():
    if request.method == "POST":
        db.session.add(Skill(name=request.form.get("name",""), level=max(0,min(100,int(request.form.get("level",70))))))
        db.session.commit()
    return render_template("admin/skills.html", items=Skill.query.all())

@admin_bp.route("/skills/<int:id>/delete", methods=["POST"])
@login_required
def skill_delete(id):
    db.session.delete(Skill.query.get_or_404(id)); db.session.commit()
    return redirect(url_for("admin.skills"))

@admin_bp.route("/experience", methods=["GET","POST"])
@login_required
def experience():
    if request.method == "POST":
        db.session.add(Experience(title=request.form.get("title",""), company=request.form.get("company",""),
                                  period=request.form.get("period",""), description=request.form.get("description","")))
        db.session.commit()
    return render_template("admin/experience.html", items=Experience.query.order_by(Experience.id.desc()).all())

@admin_bp.route("/experience/<int:id>/delete", methods=["POST"])
@login_required
def experience_delete(id):
    db.session.delete(Experience.query.get_or_404(id)); db.session.commit()
    return redirect(url_for("admin.experience"))

@admin_bp.route("/certificates", methods=["GET","POST"])
@login_required
def certificates():
    if request.method == "POST":
        db.session.add(Certificate(title=request.form.get("title",""), issuer=request.form.get("issuer",""),
                                   year=request.form.get("year",""), url=request.form.get("url","")))
        db.session.commit()
    return render_template("admin/certificates.html", items=Certificate.query.order_by(Certificate.id.desc()).all())

@admin_bp.route("/certificates/<int:id>/delete", methods=["POST"])
@login_required
def certificate_delete(id):
    db.session.delete(Certificate.query.get_or_404(id)); db.session.commit()
    return redirect(url_for("admin.certificates"))

@admin_bp.route("/blog", methods=["GET","POST"])
@login_required
def blog():
    if request.method == "POST":
        title=request.form.get("title","").strip()
        slug=request.form.get("slug","").strip().lower().replace(" ","-")
        db.session.add(BlogPost(title=title, slug=slug, excerpt=request.form.get("excerpt",""),
                                content=request.form.get("content",""), published=bool(request.form.get("published"))))
        db.session.commit()
        flash("Blog post created.", "success")
    return render_template("admin/blog.html", items=BlogPost.query.order_by(BlogPost.id.desc()).all())

@admin_bp.route("/blog/<int:id>/delete", methods=["POST"])
@login_required
def blog_delete(id):
    db.session.delete(BlogPost.query.get_or_404(id)); db.session.commit()
    return redirect(url_for("admin.blog"))

@admin_bp.route("/messages")
@login_required
def messages():
    items=Message.query.order_by(Message.created_at.desc()).all()
    for m in items: m.read=True
    db.session.commit()
    return render_template("admin/messages.html", items=items)

@admin_bp.route("/messages/<int:id>/delete", methods=["POST"])
@login_required
def message_delete(id):
    db.session.delete(Message.query.get_or_404(id)); db.session.commit()
    return redirect(url_for("admin.messages"))

@admin_bp.route("/change-password", methods=["GET","POST"])
@login_required
def change_password():
    user=User.query.first()
    if request.method=="POST":
        password=request.form.get("password","")
        if len(password)<8:
            flash("Password must be at least 8 characters.","error")
        else:
            user.password_hash=generate_password_hash(password)
            db.session.commit()
            flash("Password changed.","success")
            return redirect(url_for("admin.dashboard"))
    return render_template("admin/change_password.html")
