from flask import render_template, request, Blueprint,redirect,url_for,send_from_directory
from app.models import Post,userImage,User
from flask_login import current_user, login_required
from google.cloud import storage
import tempfile,os
main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
@login_required
def home():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first_or_404()
        page = request.args.get('page', 1, type=int)
        uimages = userImage.query.filter_by(timage=user)\
            .order_by(userImage.imageDate.desc())\
            .paginate(page=page, per_page=5)
        return render_template('home.html', uimages=uimages)
    else:
        return redirect(url_for('users.home'))


def homeback():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
