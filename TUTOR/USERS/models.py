from flask import current_app
from SPORT import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from datetime import datetime




@login_manager.user_loader
def  load_user(user_id):
    return UserModel.query.get(int(user_id))

class UserModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_image_name = db.Column(db.String(45), nullable=False, default='default.png')
    date_of_birth = db.Column(db.DateTime, nullable=False)
    biography = db.Column(db.String(170), nullable=True)
    email_confirmation_code = db.Column(db.String(5), nullable=True)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    physical_data_model = db.relationship('UserPhysicalDataModel', backref='user', uselist=False)
    following = db.relationship('FollowingModel', backref='user')
    followers = db.relationship('FollowersModel', backref='user')
    # add a location/country/city attribute

    # The Default Expire Time is Equal to 30 Mins

    def full_name(self):
        return self.first_name + " " + self.last_name

    def age(self):
        return int((datetime.date(datetime.utcnow()) - datetime.date(self.date_of_birth)).days / 365)

    def all_followers(self):
        return [UserModel.query.get(follower.follower_user_id) for follower in self.followers]

    def all_followed(self):
        return [UserModel.query.get(following.followed_user_id) for following in self.following]

    def get_reset_token(self, expire_seconds=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expire_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return UserModel.query.get(user_id)

    def get_email_change_token(self, new_email, expire_seconds=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expire_seconds)
        return s.dumps({'user_id': self.id, 'user_email': new_email}).decode('utf-8')

    @staticmethod
    def verify_email_change_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        try:
            user_email = s.loads(token)['user_email']
        except:
            return None
        
        return UserModel.query.get(user_id), user_email


    def follow(self, user):
        going_to_follow = FollowingModel(user=self, followed_user_id=user.id)
        going_to_be_followed = FollowersModel(user=user, follower_user_id=self.id)
        db.session.add(going_to_follow)
        db.session.add(going_to_be_followed)
        db.session.commit()

    def unfollow(self, user):
        delete_from_following = FollowingModel.query.filter_by(followed_user_id=user.id, user=self).first()
        delete_me_from_followers = FollowersModel.query.filter_by(user=user, follower_user_id=self.id).first()
        db.session.delete(delete_from_following)
        db.session.delete(delete_me_from_followers)
        db.session.commit()

    def is_following(self, user_id):
        following_ids = [following.followed_user_id for following in self.following]
        return user_id in following_ids

    def __repr__(self):
        return f"{self.full_name()}"


class UserPhysicalDataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float, nullable=True) # centimeters
    speed = db.Column(db.Float, nullable=True) # km/hour
    highest_jump = db.Column(db.Integer, nullable=True) # centimeters && how high can your hand reach whil jumping
    weight = db.Column(db.Float, nullable=True) # killograms
    stamina = db.Column(db.Integer, nullable=True) # how many seconds can you jogg before stopping
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"), unique=True)


    def __repr__(self):
        return "height:{}, weight:{}, speed:{}, highest jump:{}, stamina:{}".format(
            self.height, self.weight, self.speed, self.highest_jump, self.stamina)




class FollowingModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))
    followed_user_id = db.Column(db.Integer, nullable=False)

class FollowersModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))
    follower_user_id = db.Column(db.Integer, nullable=False)

    

# class UserSportDataModel(db.Model): # 
#     id = db.Column(db.Integer, primary_key=True)
#     user_model = db.Column(db.String(128), nullable=False)
#     sport_model = db.Column(db.String(128), nullable=False)
#     level = db.Column(db.Float, nullable=False) # this is a float by design so that so that some one can have a 10.95 level for example which means they're almost 11 just like video games
#     prestige = db.Column(db.Integer, nullable=False) # eacho number of levels this goes up
#     number_of_matches = db.Column(db.Integer, unique=True, nullable=False) # this can be pulled from the MatchModel where we query for the matchces that this players played or just increment this field each time he playes a match
#     number_of_matches_won = db.Column(db.Integer, unique=True, nullable=False) 
#     number_of_matches_lost = db.Column(db.Integer, nullable=False) 
#     awrds_model = db.Column(db.String(128), nullable=False) # many to many relation with AwardModel


#     def __repr__(self):
#         return f"{self.level}"


