from views import db2

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(80000))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Twitter(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(160))
    image_url = db.Column(db.String(140))
    excerpt = db.Column(db.String(160))
    timestamp = db.Column(db.DateTime)
    last_refresh = db.Column(db.DateTime)
    title = db.Column(db.String(140))

    def __repr__(self):
        return '<Tweet %r>' % (self.excerpt)

class Github(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(160))
    image_url = db.Column(db.String(140))
    excerpt = db.Column(db.String(160))
    timestamp = db.Column(db.DateTime)
    last_refresh = db.Column(db.DateTime)
    title = db.Column(db.String(140))
    author = db.Column(db.String(140))

    def __repr__(self):
        return '<Git %r>' % (self.excerpt)
