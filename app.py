from flask import Flask, g, render_template, redirect, url_for, flash, request, jsonify
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


import requests
import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'dfa111lkjlksfAF097KKLN1231231209SFDFKJASFMN'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# models.initialize()  MOVE HERE FOR LIVE WEBAPP
    

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user
    

@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response

@app.route('/register', methods=('GET','POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registered!", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=('GET','POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been loged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been loggeout!, come back soon!", "success")
    return redirect(url_for('index'))

@app.route('/new_cigar', methods=('GET','POST'))
@login_required
def new_cigar():
    form = forms.CigarForm()
    if form.validate_on_submit():
        flash("You have added a new cigar", "success")
        models.Cigar.create_cigar(
            cigar_name = form.cigar_name.data,
            brand = form.brand.data,
            body = form.body.data,
            wrapper = form.wrapper.data,
            binder = form.binder.data,
            filler = form.filler.data,
            orgin = form.orgin.data
        )          
        return redirect(url_for('index'))
    return render_template('new-cigar.html', form=form)

@app.route('/cigar/<cigar_name>', methods=['GET', 'POST'])  #Testing Getting indvidual Cigar Pages
def view_cigar(cigar_name):
    form = forms.RatingForm()    
    cigar = models.Cigar.get(models.Cigar.cigar_name**cigar_name) 
    if form.validate_on_submit():          
        models.Rate.create(
            user = g.user._get_current_object(),
            cigar = cigar, 
            size = form.size.data,
            comment = form.comment.data,
            rating = int(form.rating.data),
            location = request.form['rating_location']
        )  
        models.Cigar.average(cigar) 
        return redirect(url_for('index'))
    return render_template('rate.html', form=form, cigar=cigar)

@app.route('/search')    #SEARCH STILL IN EARLY STAGE
def search():
    """used to search database and 'check-in' cigars.  still in very early stages"""
    # sort_filter, being used to set select box equal to page parameters, need to adjust
    keyword = request.args.get('search')
    sort_filter = None 
    sort_options = {                     #Used to pass options to select box 
        'cigar_name_asc' : 'Name (A-Z)',
        'cigar_name_dsc' : 'Name (Z-A)',
        'highest_rating' : 'Highest Rating'
        }
    result_order = models.Cigar.cigar_name   
    if request.args.get('sort'):
        sort_filter = request.args.get('sort')
        if sort_filter == 'cigar_name_dsc':
            result_order = models.Cigar.cigar_name.desc()
        elif sort_filter == 'highest_rating':
            result_order = models.Cigar.avg_rating.desc()
        else:
            pass  #Allow for more sorts later
        cigar_results = (models.Cigar.select().where(models.Cigar.cigar_name.contains(keyword))
        .order_by(result_order))
    else:
        cigar_results = (models.Cigar.select().where(models.Cigar.cigar_name.contains(keyword))
    .order_by(result_order))

    
    return render_template('search.html', keyword=keyword, cigar_results=cigar_results, sort_options=sort_options, sort_filter=sort_filter)

#TESTING Location additions
# Add foursquare wrapper to allow better calls at later time
@app.route('/sendRequest')  
def results():
    params = {
        "client_id": 'LRYLMHH5W1GEZYJWGM2XWIBAEOM0HLY5QY0BXJ5UIWFRB0LL',
        "client_secret" : 'D141PZTEO5QQ40OZZ2OZELACVKDXWKUHRZLVY5EJ5JCWZ12K',
        "ll" : request.args.get('lat') + ',' + request.args.get('lng'),
        "radius" : 40000,
        "v": 20180103,
        "limit" : 15
    }
    search_req = requests.get('https://api.foursquare.com/v2/venues/search', params=params)
    search_json = search_req.json()
    
    # print(search_json['response']['venues'])
    location_ouput = {}
    for item in search_json['response']['venues']:
        location_ouput[item['id']] = item['name']

    # print(location_ouput)        
    

    
    return jsonify(location_ouput)


@app.route('/')
def index():
    latest_ratings = models.Rate.select().limit(20)  #selects 20 latest ratings, can change!
    top_cigars = models.Cigar.select().order_by(models.Cigar.avg_rating.desc()).limit(10)
    return render_template('index.html', latest_ratings=latest_ratings, top_cigars=top_cigars)

if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG,host=HOST,port=PORT)