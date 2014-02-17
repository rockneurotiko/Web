import sqlite3
import time
import os.path
import feedparser
from datetime import datetime
import re
from flask import g

from views import app

DATABASE = 'tmp/rockneurotiko.sqlite'
DEBUG = True
SECRET_KEY = 'zumTUzM3IhUVQgeX9c55'

def connect_db():
    """Returns a new connection to the sqlite database"""
    return sqlite3.connect(app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)

def init_db():
    """Create the database if it doesn't exist"""
    if not os.path.isfile(app.config['DATABASE']):
        app.logger.debug('DB disappeared, making a new one')
        f = app.open_resource('schema.sql')
        db = connect_db()
        db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one = False):
    """Query database returning dictionary"""
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def populate_database():
    init_db()
    if data_is_stale():
        load_twitter()
        load_github()

def data_is_stale():
    """Find the last entry in the sqlite database to determine if we need to
    refresh the data.  This stops us from pulling them each request"""
    try:
        last_updated = g.db.cursor().execute('select last_refresh from entries order by last_refresh desc limit 1').fetchone()[0]
    except:
        return True

    if not last_updated or (datetime.now() - last_updated).seconds > 10800:
        return True

    return False


def load_twitter():
    #Chanchullo para RSS twitter: http://www.visioncritical.com/blog/how-add-twitter-feeds-feedly-or-how-add-rss-feeds-hootsuite-quick-tip
    twitter = feedparser.parse("https://script.google.com/macros/s/AKfycbw-WRJKn60YSrSXsxnT7Cv1SiOg0bPBj_fwEksDsvgXBtt60R4/exec")
    g.db.cursor().execute('DELETE FROM twitter')
    
    for entry in twitter.entries:
        data = parseLongURL(entry['summary'])
        g.db.cursor().execute('INSERT INTO twitter VALUES (?, ?, ?, ?, ?, ?, ?,?)', 
                (None, 
                entry['link'], 
                "static/twitter_1.png",
                data, 
                "twitter", 
                datetime.strptime(entry['published'][:-6], '%a, %d %b %Y %H:%M:%S'), 
                datetime.now(),
                None))
    g.db.commit()


def parseLongURL(cont):
    http = re.findall(r'(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', cont)
    for j in http:
        url = "%s://%s%s" % (j[0],j[1],j[2])
        splitted = cont.split(url)
        if len(url) > 25:
            url = url[:25] + "..."
        if len(splitted) == 2:
            cont = splitted[0] + url + splitted[1]
        else:
            print url, splitted
        #print cont[cont.find(url):cont.find(url)+len(url)]
    return cont

def load_github():
    github = feedparser.parse("http://github.com/rockneurotiko.atom")
    g.db.cursor().execute('DELETE FROM github')

    for entry in github.entries:
        title = entry['link'].split('/')[4]
        author = entry['title'].split()[0]
        g.db.cursor().execute('INSERT INTO github VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                (None, 
                entry['link'], 
                "static/cog.png",
                entry['title'], 
                datetime.strptime(entry['updated'][:-1], '%Y-%m-%dT%H:%M:%S'), 
                datetime.now(),
                title,
                author))
 
    g.db.commit()

def getFromSource(source, limit=20):
    return query_db("select * from " + source + " order by updated desc limit " + str(limit))
 