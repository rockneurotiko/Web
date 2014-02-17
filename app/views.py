# -*- coding: utf-8 -*-
from flask import Flask,request,render_template,abort,g,send_from_directory,flash,redirect
from flask import g
from flask.ext.sqlalchemy import SQLAlchemy

#My own
from forms import LoginForm
from scripts import *

DEBUG = True
N_TWEETS = 7

app = Flask(__name__, static_folder='static')
app.config.from_object("config")
db2 = SQLAlchemy(app)

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    return value.strftime(format)

@app.before_request
def before_request():
    init_db()
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
@app.route('/index')
def index():
    populate_database()
    gits = getFromSource("github")
    tweets = getFromSource("twitter",N_TWEETS)
    return render_template('index.html', acthome="active", title="Index | Rock's Blog", tweets=tweets, gits=gits)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', 
        title = "Sign In | Rock's Blog",
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

"""
{
    title:  ,
    body:   ,
    timestamp:   ,
    author: {
        email:   ,
        nickname:   ,
    }
}
"""
@app.route('/blog')
def blog():
    populate_database()
    gits = getFromSource("github")
    tweets = getFromSource("twitter",N_TWEETS)
    return render_template('index.html', actblog="active", title="Blog | Rock's Blog", tweets=tweets, gits=gits)
    
@app.route('/about')
def about():
    populate_database()
    gits = getFromSource("github")
    tweets = getFromSource("twitter",N_TWEETS)
    return render_template('index.html', actabout="active", title="About | Rock's Blog", tweets=tweets, gits=gits)
    

@app.route('/contact')
def contact():
    populate_database()
    gits = getFromSource("github")
    tweets = getFromSource("twitter",N_TWEETS)
    return render_template('index.html', actcontact="active", title="Contact | Rock's Blog", tweets=tweets, gits=gits)


if __name__ == '__main__':
    app.run(debug=DEBUG)
