from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from app.extensions import db
from app.models import Post,userImage
from app.posts.forms import PostForm
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os,tempfile
from flask import current_app as app
from app.posts.googleOCR import _get_ocr_tokens
from google.cloud import storage
from google.cloud import pubsub
import json
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
#CLOUD_STORAGE_BUCKET = "ccnew-275119:us-east1:clouddb"

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

posts = Blueprint('posts', __name__)
publisher = pubsub.PublisherClient()


@login_required
@posts.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.root_path+'/static/uploads',
                               filename)


@login_required
@posts.route('/ocr/<filename>')
def gOCR(filename):
    return _get_ocr_tokens(filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_required
@posts.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@posts.route('/get_file/<object>')
def get_file(object):

    gcs = storage.Client()
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob('bills/'+object)

    with tempfile.TemporaryDirectory() as tmpdirname:
        fullpath = os.path.join(tmpdirname, object)
        blob.download_to_filename(fullpath)
        return send_from_directory(tmpdirname, object) 


@login_required
@posts.route('/posts/images', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.root_path,'static/uploads', filename))
            gcs = storage.Client()

            # Get the bucket that the file will be uploaded to.
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

            # Create a new blob and upload the file's content.
            blob = bucket.blob("bills/"+str(filename))
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )
            respond = get_file(filename)
            filePath = 'https://'+CLOUD_STORAGE_BUCKET+'/get_file/'+filename
            data = ""
            data = gOCR(filePath)
            imageUser = userImage(imageName=filename, imageUrl=str(filePath), \
                content=data, timage=current_user)
            db.session.add(imageUser)
            db.session.commit()

            message = {
                'fileUrl': filePath,
                'userId': current_user.get_id()
            }
            topic_name = 'projects/{}/topics/{}'.format(
                os.getenv('GOOGLE_CLOUD_PROJECT'), 'ocr'
            )
            publisher.publish(topic_name, json.dumps(message).encode('utf8'))

            return redirect(url_for('main.home'))
    return render_template('postImage.html')


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
