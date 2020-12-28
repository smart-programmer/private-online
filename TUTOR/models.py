# from SPORT import db, login_manager, app
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from flask_login import UserMixin
# from datetime import datetime


# partners = db.Table('partners',
#     db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
# )
# tags = db.Table('tags',
#     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
#     db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
# )


# @login_manager.user_loader
# def  load_user(user_id):
#     return User.query.get(int(user_id))


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(128), nullable=False)
#     last_name = db.Column(db.String(128), nullable=False)
#     username = db.Column(db.String(256), unique=True, nullable=False)
#     email = db.Column(db.String(256), unique=True, nullable=False)
#     password = db.Column(db.String(512), nullable=False)
#     projects = db.relationship('Project', backref='owner') # a user has projects and a projects has owner
#     image_file = db.Column(db.String(20), nullable=False, default='default.png')
#     is_confermed = db.Column(db.String(10), nullable=False, default='False') # To Confirm User With Emails Like big Websites

#     # The Default Expire Time is Equal to 30 Mins
#     def get_reset_token(self, expire_seconds=1800):
#         s = Serializer(app.config["SECRET_KEY"], expire_seconds)
#         return s.dump({'user_id': self.id}).decode('utf-8')

#     @staticmethod
#     def verify_reset_token(token):
#         s = Serializer(app.config["SECRET_KEY"])
#         try:
#             user_id = s.load(token)['user_id']
#         except:
#             return None
#         return User.query.get(user_id)

#     def full_name(self):
#         return self.first_name + " " + self.last_name

#     def __repr__(self):
#         return f"{self.full_name()}"


# # Model For project contains all its data
# # add github repo link
# class Project(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     title = db.Column(db.String(128), nullable=False)
#     description = db.Column(db.String(1024), nullable=False)
#     allowed_number_of_partners = db.Column(db.Integer, nullable=False, default=1)
#     private = db.Column(db.Boolean, default=False)
#     tags = db.relationship('Tag', secondary=tags, lazy='subquery',
#         backref=db.backref('projects', lazy=True)) # a project has tags and a tag has projects
#     team = db.relationship('Team', backref='project', uselist=False) # prject has a team and a team has a project

    
    
#     def __repr__(self):
#         return f"{self.title}"


# class Tag(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)


# # add team name
# class Team(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     project_id = db.Column(db.Integer, db.ForeignKey("project.id"), unique=True)
#     partners = db.relationship('User', secondary=partners, lazy='subquery',
#         backref=db.backref('joined_projects', lazy=True)) # team has users and user has teams


# class Visitors(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     count =  db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         return f"number of visitors is: {self.count}"
