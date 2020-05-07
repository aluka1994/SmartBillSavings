from flask import render_template, request, Blueprint,redirect,url_for,send_from_directory
from app.models import Post,userImage,User,Product,GroceryList
from flask_login import current_user, login_required
from google.cloud import storage
from app.extensions import db
import tempfile,os,json
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
        grocery = GroceryList.query.filter_by(grocerylist=user)
        return render_template('home.html', uimages=uimages,glist = grocery)
    else:
        return redirect(url_for('users.home'))


@main.route("/deletegrocery/", methods=['GET', 'POST'])
@login_required
def deletegrocery():
    if current_user.is_authenticated and request.method == "POST":
        data = json.loads(request.data)
        gid = data['gid']
        fdata = {}
        if gid!="":
            user = User.query.filter_by(username=current_user.username).first_or_404()
            gcl = GroceryList.query.filter_by(id = gid,grocerylist=user).first_or_404()
            db.session.delete(gcl)
            db.session.commit()
            data['flag'] = "success"
            return json.dumps(data)
        else:
            data['flag'] = "fail"
            return json.dumps(data)
    else:
        data['flag'] = "fail"
        return json.dumps(data)

@main.route("/savegrocery/", methods=['GET', 'POST'])
@login_required
def savegrocery():
    if current_user.is_authenticated and request.method == "POST":
        data = json.loads(request.data)
        glist = data['gdata']
        if len(glist) > 0:
            user = User.query.filter_by(username=current_user.username).first_or_404()
            # gcl = GroceryList.query.filter_by(grocerylist=user)
            # db.session.delete(gcl)
            # db.session.commit()
            for value in glist:
                gcl = GroceryList.query.filter_by(productName=value,grocerylist=user).first()
                if gcl:
                    gcl.productName = value
                    db.session.add(gcl)
                    db.session.commit()    
                else:
                    gc = GroceryList(productName=value,quantity=1,grocerylist=user)
                    db.session.add(gc)
                    db.session.commit()
            data['flag'] = "success"
            return json.dumps(data)
        else:
            data['flag'] = "fail"
            return  json.dumps(data)
    else:
        data = {}
        data['flag'] = "fail"
        return json.dumps(data)




    return "grocerysaved"
    #return redirect(url_for('main.dashboard'))

@main.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first_or_404()
        page = request.args.get('page', 1, type=int)
        plist = Product.query.filter_by(productname=user)\
            .order_by(Product.purchase_date.desc())\
            .paginate(page=page, per_page=5)
            
        products = Product.query.filter_by(productname=user)\
            .order_by(Product.purchase_date.desc())
        
        grocerylist = GroceryList.query.filter_by(grocerylist=user)
        return render_template('dashboard.html', plist=plist,products=products,grocerylist = grocerylist)
    else:
        return redirect(url_for('users.home'))


def homeback():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
