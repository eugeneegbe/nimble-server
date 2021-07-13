from datetime import datetime

from flask_login import UserMixin

from nimble import db, login_manager


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    pref_lang = db.Column(db.String(10), default='en')
    role = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(40), unique=True, nullable=False)
    current_stage = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        # This is what is shown when object is printed
        return "User({}, {}, {}, {})".format(
                self.name,
                self.pref_lang,
                self.role,
                self.current_stage)


class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    p_username = db.Column(db.String(20), unique=True, nullable=False)
    p_email = db.Column(db.String(30), unique=True, nullable=False)
    status = db.Column(db.String(40), nullable=False, default="pending")

    def __repr__(self):
        # This is what is shown when object is printed
        return "Account({}, {}, {})".format(
                self.p_username,
                self.p_email,
                self.status)


class Article(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(1000), nullable=False)
    created = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))

    def __repr__(self):
        # This is what is shown when object is printed
        return "Article({}, {})".format(
                self.name,
                self.url)


class Contribution(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    edit_mode = db.Column(db.String(20), nullable=False)
    action = db.Column(db.String(20), default='edit')
    timestamp = db.Column(db.Date, nullable=False,
                    default=datetime.now().strftime('%Y-%m-%d'))

    def __repr__(self):
        # This is what is shown when object is printed
        return "Contribution({}, {}, {})".format(
                self.username,
                self.edit_mode,
                self.timestamp)


class Topic(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(70), unique=True, nullable=False)

    def __repr__(self):
        # This is what is shown when object is printed
        return "Category({})".format(self.name)


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    title = db.Column(db.String(70), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))
    text = db.Column(db.String(3000), nullable=True)
    tags = db.Column(db.String(200))

    def __repr__(self):
        # This is what is shown when object is printed
        return "Message({}, {}, {})".format(
                self.title,
                self.username,
                self.text)


class Reply(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    text = db.Column(db.String(2000), nullable=False)
    post_id =db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))

    def __repr__(self):
        # This is what is shown when object is printed
        return "Reply({}, {}, {})".format(
                self.username,
                self.post_id,
                self.text)


class Tag(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        # This is what is shown when object is printed
        return "Tag({})".format(self.name)
