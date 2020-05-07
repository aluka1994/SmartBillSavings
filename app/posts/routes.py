from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint,current_app)
from flask_login import current_user, login_required
from app.extensions import db
from app.models import Post,userImage,User,Product
from app.posts.forms import PostForm
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os,tempfile
from flask import current_app as app
from app.posts.googleOCR import _get_ocr_tokens
from google.cloud import storage
from app.posts.processOCR import getData
from google.cloud import pubsub_v1
from flask import current_app
import base64
import json
import logging
import os

# Initialize the publisher client once to avoid memory leak
# and reduce publish latency.

publisher = pubsub_v1.PublisherClient()
#CLOUD_STORAGE_BUCKET = "ccnew-275119:us-east1:clouddb"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
posts = Blueprint('posts', __name__)


@posts.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.root_path+'/static/uploads',
                               filename)


@posts.route('/ocr/<filename>')
@login_required
def gOCR(filename):
    return _get_ocr_tokens(filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@posts.route('/success/<name>')
@login_required
def success(name):
    return 'welcome %s' % name

@posts.route('/get_file/<object>')
def get_file(object):

    CLOUD_STORAGE_BUCKET = current_app.config['CLOUD_STORAGE_BUCKET']
    gcs = storage.Client()
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob('bills/'+object)

    with tempfile.TemporaryDirectory() as tmpdirname:
        fullpath = os.path.join(tmpdirname, object)
        blob.download_to_filename(fullpath)
        return send_from_directory(tmpdirname, object) 

@posts.route('/posts/images', methods=['GET', 'POST'])
@login_required
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
            CLOUD_STORAGE_BUCKET = current_app.config['CLOUD_STORAGE_BUCKET']
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

            # Create a new blob and upload the file's content.
            blob = bucket.blob("bills/"+str(filename))
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )
            respond = get_file(filename)
            CLOUD_URL = current_app.config['CLOUD_URL']
            filePath =  CLOUD_URL+"/get_file/"+filename
            data = ""
            #data = gOCR(filePath)
            imageUser = userImage(imageName=filename, imageUrl=str(filePath), \
                content=data,timage=current_user)
            db.session.add(imageUser)
            db.session.flush()
            tdata = {"imPath":filePath,"uid":current_user.id,"filename":filename,"tid":imageUser.id}
            db.session.commit()
            gt = (str(json.dumps(tdata))).encode('utf-8')
            topic_path = publisher.topic_path(current_app.config['PROJECT'],current_app.config['PUBSUB_TOPIC'])
            future = publisher.publish(topic_path, data=gt)
            return redirect(url_for('main.home'))
    return render_template('postImage.html')


@posts.route("/processdata/")
@login_required
def backendData():
    if (request.args.get('token', '') !=
            current_app.config['PUBSUB_VERIFICATION_TOKEN']):
        return 'Invalid request', 400

    envelope = json.loads(request.data.decode('utf-8'))
    payload = base64.b64decode(envelope['message']['imPath'])
    #return str(MESSAGES)
    # Returning any 2xx status indicates successful receipt of the message.
    return getData()

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
